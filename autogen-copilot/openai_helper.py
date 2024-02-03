import openai
import os
from werkzeug import Response
from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt 
import load_env


load_env.load_env()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
# set the deployment name for the model we want to use
deployment = "gpt-4"
model: str = "text-embedding-ada-002" 



@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
# Function to generate embeddings for title and content fields, also used for query embeddings
def generate_embeddings(text, model=model):
    try:
        openai_client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2023-05-15",
        )
        embedding = openai_client.embeddings.create(input = [text], model=model).data[0].embedding
        return embedding
    except Exception as e:
        print("Error calling OpenAI:" + openai_client.base_url)
        print(e)
        raise
    


def get_chatgpt_response(userQuery, service_bus_session_id, queue=None):
        
        gptPrompt = {
            "systemMessage": {"role": "system", "content": "You are an AI assistant. Always end your response with 'CONV_END' to end the conversation. Format response with appropriate HTML tags. "},
            "question": {"role": "user", "content": userQuery}
        }
        prompt = {"maxTokens": "500", "temperature": "0.5", "gptPrompt": gptPrompt}
        
        return Response(call_openai_base(prompt, None, None), mimetype='text/event-stream')

def call_openai_base(prompt, service_bus_session_id, queue=None):
    # Assume setup_byod("gpt-4") and other setup code here
    try:
        messages = [prompt['gptPrompt']['systemMessage']] + [prompt['gptPrompt']['question']]
        openai_client = AzureOpenAI(
            base_url = f"{endpoint}/openai/deployments/{deployment}/extensions",
            api_key=api_key,
            api_version="2023-09-01-preview",
        )
        response = openai_client.chat.completions.create(
            model=os.getenv('DEPLOYMENT_NAME'),
            messages=messages,
            temperature=float(prompt['temperature']),
            extra_body={
                "dataSources": [
                    {
                        "type": "AzureCognitiveSearch",
                        "parameters": {
                            "endpoint": os.environ["SEARCH_ENDPOINT"],
                            "key": os.environ["SEARCH_KEY"],
                            "indexName": os.environ["SEARCH_INDEX_NAME"],
                        }
                    }
                ]
            },
            max_tokens=int(prompt['maxTokens']),
            stream=True
        )

        for chunk in response:
            try:
                content = chunk.choices[0].delta.content
                #print(chunk.choices[0].end_turn)
                if content is not None:
                    
                    yield content
            except (KeyError, IndexError, TypeError) as e:
                print(f"An error occurred: {e}")
        yield "CONV_END"
    except Exception as e:
        print("Error calling OpenAI:" + openai.api_base)
        print(e)
        yield str(e)



def call_openai_base1(prompt, service_bus_session_id, queue = None):       
    
    try:
        messages = [prompt['gptPrompt']['systemMessage']] + [prompt['gptPrompt']['question']]
        response = openai.ChatCompletion.create(
                    engine=os.getenv('DEPLOYMENT_NAME'), 
                    messages = messages,
                    temperature= float(prompt['temperature']),
                    extra_body={
                        "dataSources": [
                            {
                                "type": "AzureCognitiveSearch",
                                "parameters": {
                                    "endpoint": os.environ["SEARCH_ENDPOINT"],
                                    "key": os.environ["SEARCH_KEY"],
                                    "indexName": os.environ["SEARCH_INDEX_NAME"],
                                }
                            }
                        ]
                    },
                    max_tokens=int(prompt['maxTokens']) ,
                    stream=True                    
                    )
        for chunk in response:
            try:
                content = chunk['choices'][0]['delta']['content']
                if content is not None:
                    queue.put(content)
            except (KeyError, IndexError, TypeError) as e:
                print(f"An error occurred: {e}")
           
    except Exception as e:
        print("Error calling OpenAI:" + openai.api_base)
        print(e)
        return str(e)