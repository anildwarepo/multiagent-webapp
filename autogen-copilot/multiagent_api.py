from flask import Flask, jsonify, request
from flask_cors import CORS
import openai_helper
import autogen_bot
import slm_api
import docintelligence_helper
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/chat/conversation', methods=['OPTIONS'])
def options():
    return jsonify({'message': 'Options request allowed'}), 200

@app.route('/status')
def status():
    return {'message': 'Hello, World!', 'status': 'Running'}


@app.route('/chat/greeting', methods=['GET'])
def greeting():
    return """Hello, I am a multi-agent chatbot. 
            I can answer questions about companies, perform data analysis, 
            create plots for visualization and answer questions about product usage and know-how.
            \nTERMINATE"""



@app.route('/chat/doclist', methods=['GET'])
def getDocList():
    # read file names from folder
    docDirectory = "document_classification/demodocs"
    docList = []

    #for filename in os.listdir(docDirectory): with index
    for index, filename in enumerate(os.listdir(docDirectory)):
        doc_name = filename.split(".")
        doc = {"key": f'd10{index}', "text": doc_name[0], "category": "Document Analysis"}
        docList.append(doc)
    return jsonify(docList)

@app.route('/chart')
def get_chart():
    return """
    [
        {
          "x": [5, 2, 3],
          "y": [2, 6, 3],
          "type": "scatter",
          "mode": "lines+markers",
          "marker": {"color": "red"}
        },
        {"type": "bar", "x": [1, 2, 10], "y": [2, 5, 3]}
    ]
"""


@app.route('/chat/conversation2', methods=['POST'])
def post2():
    print("Received POST request...")
    data = request.get_json()
    content_queue = "test1" #content_queues[data['queue_name']]
    return openai_helper.get_chatgpt_response(data['userMessage'], service_bus_session_id=None, queue=None)


@app.route('/chat/conversation', methods=['POST'])
async def post():
    """
    Read JSON data from the request body
    """
    print("Received POST request...")
    data = request.get_json()

    query_cateory = data['query_category']
    if(query_cateory == "Small Language Model"):
        print("SLM API")
        response = await slm_api.get_slm_response(data['userMessage'])
    if(query_cateory == "Document Analysis"):
        print("Document Analysis")
        url = f"https://github.com/anildwarepo/multiagent-webapp/raw/main/autogen-copilot/document_classification/demodocs/{data['userMessage']}.docx"
        doc_content = docintelligence_helper.submit_document_for_analysis(url)
        response = openai_helper.get_chatgpt_base_response(doc_content, os.environ['SYSTEM_MESSAGE'], service_bus_session_id=None, queue=None)
        #response = await autogen_bot.start_multiagent_chat( doc_content)
    else:
        print("autogen API")
        response = await autogen_bot.start_multiagent_chat(data['userMessage'])
    return response



if __name__ == '__main__':
    app.run(threaded=True)
