import autogen
import search_helper
import sql_helper
from autogen import AssistantAgent
import random
from typing import List, Dict


cache_seed = None

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4-turbo"],
    },
)

dataanalysis_llm_config = {
    "functions": [
        {
            "name": "execute_sql",
            "description": "execute a sql query and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "valid sql query to execute.",
                    }                   
                },
                "required": ["sql_query"]
            }
        }
    ],
    "config_list": config_list,
    "timeout": 60,
    "cache_seed": cache_seed,
}


plotly_llm_config = {
    "config_list": config_list,
    "timeout": 60,
    "cache_seed": cache_seed,

}

llm_config = {
    "functions": [
        {
            "name": "retrieve_content",
            "description": "retrieve content for code generation and question answering.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
                    },
                    "index_name": {
                        "type": "string",
                        "description": "index name to search content from. Index name be either index-10k or product-guides.",
                    }
                },
                "required": ["message", "index_name"],
            },
        },
    ],
    "config_list": config_list,
    "timeout": 60,
    "cache_seed": cache_seed,
}

# autogen.ChatCompletion.start_logging()
termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

userProxyAgent = autogen.UserProxyAgent(
    name="userProxyAgent",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="User who ask questions about various topics. You can execute in python only. ",
    code_execution_config={"work_dir": "coding"},  # we don't want to execute code in this case.
    default_auto_reply= None #"Reply `TERMINATE` if the task is done.",
)

dataAnalysisExpert = AssistantAgent(
    name="dataAnalysisExpert",
    is_termination_msg=termination_msg,
    system_message=f"""
            You are a smart AI assistant to help answer business questions based on analyzing data. 
            You can plan solving the question with one more multiple thought step. 
            At each thought step, you can write sql query to analyze data to assist you. 
            Observe what you get at each step to plan for the next step.
            Do not write python code to analyze data.
            You are given following utilities to help you retrieve data.
            1. execute_sql(sql_query: str): A Python function can query data from the <<data_sources>> given a query which you need to create. The query has to be syntactically correct for sql_engine and only use tables and columns under <<data_sources>>. The execute_sql function returns a Python pandas dataframe contain the results of the query.
            2. Don't forget to deal with data quality problem. You should apply data imputation technique to deal with missing data or NAN data.
            3. Always follow the flow of Thought: , Observation:, Action: and Answer: as in template below strictly. 
            4. For coding tasks, only use the functions you have been provided with
            5. You are limited to 5 SQL queries for your analysis.

            <<Table Schema>>{sql_helper.select_sql_table_schema()}<<Table Schema>>
            
            <<Template>>
            Question: User Question
            Thought 1: Your thought here.
            Action: 
            Generate SQL for the User question so that function can call execute_sql() 

            Observation: 
            step1_df is displayed here
            Answer: Your final answer and comment for the question. 
            Also use SQL for computation, never compute result youself.
            Format the result into markdown table and display it here.
            <</Template>>
            Reply `TERMINATE` when the task is done.
            """,
    llm_config=dataanalysis_llm_config,
)


plotlyExpert = AssistantAgent(
    name="plotlyExpert",
    is_termination_msg=termination_msg,
    system_message="""
            You are a plotly expert. Write your analysis only in the json template below. 
            Do not write any other text outside of the json schema in your answer.
            Reply `TERMINATE` when the task is done.
            You can generate plotly chart in valid JSON format. 
            For the plotly chart, suggest appropriate chart title, chart type, size(width and height) and 
            dark theme colors( in proper format "rgba(222,45,38,0.8)") to explain the data to the user.             
            JSON schema is:
            { "plotly_data": "true", "data": [], "layout": { width: 500, height: 240, title: "Appropriate Chart Title" }, "dataAnalysis": "data analysis here."}
            
            example:
            user: what is the average price of the product in each category?
            Your answer:
            { "plotly_data": "true", "data": [], "layout": { width: 500, height: 240, title: "Appropriate Chart Title"}, "dataAnalysis": "data analysis here."}

            Your answer:
            { "plotly_data": "true", "data": [], "layout": { width: 500, height: 240, title: "Appropriate Chart Title"}, "dataAnalysis": "data analysis here."}
            Once you have the answer, say out the answer and append a new line with TERMINATE.


            """,
    llm_config=plotly_llm_config,
)

communicationsExpert_llm_config = {
    "config_list": config_list,
    "cache_seed": cache_seed
}

communicationsExpert = AssistantAgent(
    name="communicationsExpert",
    description="You are a email communications expert. You can write email on behalf of communications officer or marketing officer.",
    is_termination_msg=termination_msg,
    system_message="""
                You are a email communications expert. You can write email on behalf of communications officer or marketing officer.
                You can generate email to customer based on context provided to you. 
                Use markdown formatting to format your email that can be rendered on HTML page.
                Do not use ``` to write your email.
                Use business vocubulary and be polite in your email. Reply `TERMINATE` when the task is done.
            """,
    llm_config= communicationsExpert_llm_config
)

expertAgent = AssistantAgent(
    name="expertAgent",
    is_termination_msg=termination_msg,
    system_message="""
        Assistant helps users with answers to the questions.Reply `TERMINATE` in the end when everything is done. 
        Answer ONLY with the facts listed in the list of context below. 
        You will need identify the index name and pass ito the retrieve_content function.
        The index names are either index-10k and product-guides. 
                demo-index: Machine learning related questions
                aml-vector-index: networking and sdwan related questions. 
                index-10k: User question is about financial reports, about a company, about a stock etc.
        If there isn't enough information below, say you don't know. \n   
        Do not generate answers that don't use the context below. \n  Each source has a name followed by colon and the actual information, 
        always include the source name for each fact you use in the response.\n  
        Use square brakets to reference the source, e.g. [info1.txt]. 
        Format your response in markdown format and structure the response in paragraphs and bullets points as appropriate.
        Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].
        Once you have the answer, say out the answer and append a new line with TERMINATE.
    """,
    llm_config=llm_config,
)


def _reset_agents():
    userProxyAgent.reset()
    expertAgent.reset()
    dataAnalysisExpert.reset()
    communicationsExpert.reset()
    plotlyExpert.reset()



async def start_multiagent_chat(userQuery):   
    _reset_agents()
    
    #autogen.ChatCompletion.start_logging()

    userProxyAgent.register_function(
        function_map= { 
                        "retrieve_content": search_helper.retrieve_content,
                        "execute_sql": sql_helper.execute_sql 
                    }
    )    
    

    groupchat = autogen.GroupChat(
        agents=[userProxyAgent, expertAgent, dataAnalysisExpert, communicationsExpert, plotlyExpert],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )


    manager_llm_config = llm_config.copy()
    manager_llm_config.pop("functions")
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=manager_llm_config)
    #manager = autogen.GroupChatManager(groupchat=[userProxyAgent, expertAgent, dataAnalysisExpert, communicationsExpert, plotlyExpert], llm_config=manager_llm_config)
    await userProxyAgent.a_initiate_chat(
        manager,
        message=userQuery,
    )

    print(userProxyAgent.last_message())
    return userProxyAgent.last_message()['content']