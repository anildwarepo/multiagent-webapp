import os
import openai  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.indexes.models import (  
    ExhaustiveKnnAlgorithmConfiguration,
    ExhaustiveKnnParameters,
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    SemanticPrioritizedFields,
    SemanticField,  
    SearchField,  
    SemanticSearch,
    VectorSearch,  
    HnswAlgorithmConfiguration,
    HnswParameters,  
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    ExhaustiveKnnParameters,
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    SemanticField,  
    SearchField,  
    VectorSearch,  
    HnswParameters,  
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)   
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import requests
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
from openai import AzureOpenAI


env_path = Path('.') / 'secrets.env'
load_dotenv(dotenv_path=env_path)



SEARCH_ENDPOINT = os.environ["AZSEARCH_EP"]
SEARCH_API_KEY = os.environ["AZSEARCH_KEY"]
SEARCH_INDEX = os.environ["INDEX_NAME"]

api_version = '?api-version=2021-04-30-Preview'
headers = {'Content-Type': 'application/json',
        'api-key': SEARCH_API_KEY }

endpoint = os.environ["AFR_ENDPOINT"]
key = os.environ["AFR_API_KEY"]
credential = AzureKeyCredential(SEARCH_API_KEY)
openai.api_type = "azure"  
openai.api_key = os.getenv("OPENAI_API_KEY")  
openai.api_base = os.getenv("OPENAI_API_BASE")  
openai.api_version = "2023-05-15",


client = AzureOpenAI(
  api_key = os.getenv("OPENAI_API_KEY"),  
  api_version = "2023-05-15",
  azure_endpoint = os.getenv("OPENAI_API_BASE")
)

formUrl = os.environ["FILE_URL"]
localFolderPath = os.environ["LOCAL_FOLDER_PATH"]

if (formUrl == "" and localFolderPath == ""):
    print("Please provide a valid FILE_URL or LOCAL_FOLDER_PATH in secrets.env file.")
    exit()



document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


def create_vector_index(index_name=SEARCH_INDEX):
    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT, credential=credential)
    
    try:
        idx = index_client.get_index(index_name)
        return
    except Exception as e:
        if e.status_code == 404:
            pass
        else:
            raise e


    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String,
                        searchable=True, retrievable=True),
        SearchableField(name="title", type=SearchFieldDataType.String,
                        searchable=True, retrievable=True),
        SearchableField(name="filepath", type=SearchFieldDataType.String,
                        searchable=False, retrievable=True),
        SearchableField(name="pagenumber", type=SearchFieldDataType.String,
                        filterable=False, searchable=False, retrievable=True),
        SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile")
    ]

    # Configure the vector search configuration  
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="myHnsw",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE
                )
            ),
            ExhaustiveKnnAlgorithmConfiguration(
                name="myExhaustiveKnn",
                kind=VectorSearchAlgorithmKind.EXHAUSTIVE_KNN,
                parameters=ExhaustiveKnnParameters(
                    metric=VectorSearchAlgorithmMetric.COSINE
                )
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="myHnswProfile",
                algorithm_configuration_name="myHnsw",
            ),
            VectorSearchProfile(
                name="myExhaustiveKnnProfile",
                algorithm_configuration_name="myExhaustiveKnn",
            )
        ]
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")]
        )
    )

    # Create the semantic settings with the configuration
    semantic_search = SemanticSearch(configurations=[semantic_config])

    # Create the search index with the semantic settings
    index = SearchIndex(name=index_name, fields=fields,
                        vector_search=vector_search, semantic_search=semantic_search)
    result = index_client.create_or_update_index(index)
    print(f' {result.name} created')

def delete_search_index(index_name=SEARCH_INDEX):
    try:
        url = SEARCH_ENDPOINT + "indexes/" + index_name + api_version 
        response  = requests.delete(url, headers=headers)
        return("Index deleted")
    except Exception as e:
        return(e)
    

def add_document_to_index(page_idx, documents, index_name=SEARCH_INDEX):
    try:
        url = SEARCH_ENDPOINT + "indexes/" + index_name + "/docs/index" + api_version
        response  = requests.post(url, headers=headers, json=documents)
        print(f"page_idx is {page_idx} - {len(documents['value'])} Documents added")
    except Exception as e:
        print(e)

def process_afr_result(result, filename):
    print(f"Processing {filename } with {len(result.pages)} pages into Azure Search....this might take a few minutes depending on number of pages...")
    for page_idx in range(len(result.pages)):
        docs = []
        content_chunk = ""
        for line_idx, line in enumerate(result.pages[page_idx].lines):
            #print("...Line # {} has text content '{}'".format(line_idx,line.content.encode("utf-8")))
            content_chunk += str(line.content.encode("utf-8")).replace('b','') + "\n"

            if line_idx != 0 and line_idx % 20 == 0:
              search_doc = {
                    "id":  f"page-number-{page_idx + 1}-line-number-{line_idx}",
                    "text": content_chunk,
                    "textVector": generate_embeddings(content_chunk),
                    "fileName": filename,
                    "pageNumber": str(page_idx+1)
              }
              docs.append(search_doc)
              content_chunk = ""
        search_doc = {
                    "id":  f"page-number-{page_idx + 1}-line-number-{line_idx}",
                    "text": content_chunk,
                    "textVector": generate_embeddings(content_chunk),
                    "fileName": filename,
                    "pageNumber": str(page_idx + 1)
        }
        docs.append(search_doc)   
        add_document_to_index(page_idx, {"value": docs})

model: str = "text-embedding-ada-002" 
# Function to generate embeddings for title and content fields, also used for query embeddings
def generate_embeddings(text, model=model):
    if text == "":
        return []
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def main():
    create_vector_index()
    if(formUrl != ""):
      print(f"Analyzing form from URL {formUrl}...")
      poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", formUrl)
      result = poller.result()
      print(f"Processing result...this might take a few minutes...")
      process_afr_result(result, "aml-api-v2.pdf")

    if(localFolderPath != ""):
      for filename in os.listdir(localFolderPath):
        file = os.path.join(localFolderPath, filename)    
        with open(file, "rb") as f:
          print(f"Analyzing file {filename} from directory {localFolderPath}...")
          poller = document_analysis_client.begin_analyze_document(
              "prebuilt-layout", document=f
          )
          result = poller.result()
          print(f"{filename}Processing result...this might take a few minutes...")
          process_afr_result(result, filename)
      print(f"done")

if __name__ == "__main__":
    main()