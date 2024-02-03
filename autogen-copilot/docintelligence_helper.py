import json
import os
from azure.core.credentials import AzureKeyCredential
import time
import requests
import load_env
load_env.load_env()
doc_intell_endpoint = os.environ["AZURE_DOC_INTELLIGENCE_ENDPOINT"]
doc_intell_endpoint_key = os.environ["AZURE_DOC_INTELLIGENCE_KEY"]


def submit_document_for_analysis(url):

    # sample document
    # Operation-location URL from the 'curl' response
    operation_url = ""
 
    # Define the API URL for submitting the document
    submit_url = f"{doc_intell_endpoint}documentintelligence/documentModels/prebuilt-layout:analyze?api-version=2023-10-31-preview"

    # Set the headers including the Content-Type and the Ocp-Apim-Subscription-Key
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": doc_intell_endpoint_key,
    }

    # Define the data to be sent in the POST request, specifying the URL of the document
    data = {
        "urlSource": url
    }

    while True:
        # Make the POST request to submit the document for analysis
        response = requests.post(submit_url, headers=headers, json=data)

        if response.status_code == 202:
            # The operation was successful, get the operation URL and break the loop
            operation_url = response.headers["Operation-Location"]
            break
        # Print the response to check if it was successful and to get the operation URL or ID
        print(response.json())



    # Poll the operation URL until the analysis is complete
    while True:
        response = requests.get(operation_url, headers=headers)
        if response.status_code == 200:
            # Processing is complete, print the results and break the loop
            #print(response.json())
            return f"""
            Classify the below document:
            {response.json()['analyzeResult']['content']}
            """        
        elif response.status_code == 202:
            # Processing is still ongoing, wait a bit and then try again
            print("Processing ongoing, waiting before retrying...")
            time.sleep(10)  # Wait for 10 seconds before polling again
        else:
            # An error occurred, print the status code and response, then break the loop
            print(f"Error occurred, status code: {response.status_code}")
            print(response.text)
            break


#formUrl = "https://github.com/anildwarepo/multiagent-webapp/raw/main/autogen-copilot/document_classification/HR%20Documents/HR_Policies/Company%20Data%20Protection%20Policy.docx"
#result = submit_document_for_analysis(formUrl)
