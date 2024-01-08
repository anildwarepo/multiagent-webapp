from flask import Flask, jsonify, request
from flask_cors import CORS
import openai_helper
import autogen_bot

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
    response = await autogen_bot.start_multiagent_chat(data['userMessage'])
    return response



if __name__ == '__main__':
    app.run(threaded=True)
