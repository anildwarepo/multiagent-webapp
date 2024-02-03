from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient  
import os  
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential 
import openai_helper
from azure.search.documents.indexes.models import SearchFieldDataType 
import load_env


load_env.load_env()

service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") 
#index_name = os.getenv("AZURE_SEARCH_INDEX_NAME") 
key = os.getenv("AZURE_SEARCH_ADMIN_KEY") 

credential = AzureKeyCredential(key)

query = "What industries does paypal operate in?"  

def retrieve_content(message, index_name):
    return search(message, index_name, num_results=3)


def get_index_fields(index_name):
    index_client = SearchIndexClient(
        endpoint=service_endpoint, credential=credential)
    idx = index_client.get_index(index_name)
    select_fields = []
    vector_fields =  ""
    for field in idx.fields:
        print(field.name)
        if(field.type == SearchFieldDataType.String):
            select_fields.append(field.name)
        if(str.find(field.name, "Vector") > 0):
            vector_fields += field.name + ","

    #print(select_fields)
    # strip trailing comma
    vector_fields = vector_fields[:-1]
    return select_fields, vector_fields
    #print(vector_fields)

def search(query, index_name, num_results=3, vectorField="contentVector"): 
    select_fields, vector_fields = get_index_fields(index_name)    
    search_client = SearchClient(service_endpoint, index_name, credential=credential)
    vector_query = VectorizedQuery(vector=openai_helper.generate_embeddings(query), k_nearest_neighbors=num_results, fields=vector_fields)    
    results = search_client.search(  
        search_text=None,  
        vector_queries= [vector_query],
        select= select_fields #["title", "content", "filepath"]
    )  
    
    json_results = []
    for result in results:
        field_results = []
        for field in select_fields:
            result_dict = {
                field: result[field]
            }
            field_results.append(result_dict)
        #result_dict = {
        #    "Title": result['title'],
        #    "Score": result['@search.score'],
        #    "Content": result['content'],
        #    "filepath": result['filepath'],
        #}
        json_results.append(field_results)
    print(json_results)
    return json_results


#results = search(query)
#print(results)