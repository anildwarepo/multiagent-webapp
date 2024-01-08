import autogen
import search_helper
import sql_helper
#from autogen import AssistantAgent
from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent
import random
from typing import List, Dict

class CustomGroupChat(GroupChat):
    def __init__(self, agents, messages, max_round=10):
        super().__init__(agents, messages, max_round)
        self.previous_speaker = None  # Keep track of the previous speaker
    
    def select_speaker(self, last_speaker: Agent, selector: AssistantAgent):
        # Check if last message suggests a next speaker or termination
        last_message = self.messages[-1] if self.messages else None
        if last_message:
            if 'NEXT:' in last_message['content']:
                suggested_next = last_message['content'].split('NEXT: ')[-1].strip()
                print(f'Extracted suggested_next = {suggested_next}')
                try:
                    return self.agent_by_name(suggested_next)
                except ValueError:
                    pass  # If agent name is not valid, continue with normal selection
            elif 'TERMINATE' in last_message['content']:
                try:
                    return self.agent_by_name('userProxyAgent')
                except ValueError:
                    pass  # If 'User_proxy' is not a valid name, continue with normal selection
        
        team_leader_names = [agent.name for agent in self.agents if agent.name.endswith('1')]

        if last_speaker.name in team_leader_names:
            team_letter = last_speaker.name[0]
            possible_next_speakers = [
                agent for agent in self.agents if (agent.name.startswith(team_letter) or agent.name in team_leader_names) 
                and agent != last_speaker and agent != self.previous_speaker
            ]
        else:
            team_letter = last_speaker.name[0]
            possible_next_speakers = [
                agent for agent in self.agents if agent.name.startswith(team_letter) 
                and agent != last_speaker and agent != self.previous_speaker
            ]

        self.previous_speaker = last_speaker

        if possible_next_speakers:
            next_speaker = random.choice(possible_next_speakers)
            return next_speaker
        else:
            return None

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

default_llm_config = {
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

communicationsExpert_llm_config = {
    "config_list": config_list,
    "cache_seed": cache_seed
}


termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
dataAnalysisTeamLeader = AssistantAgent(name="A1",
                                        system_message="""You are the team leader A1,
                                        your team consists of A2 and A3.
                                        """,
                                        llm_config=default_llm_config)


sqlExpert = AssistantAgent(
    name="A2",
    is_termination_msg=termination_msg,
    system_message=f"""
            You are a team member A2 who can help answer business questions based on quering and analyzing data from database.
            You can plan solving the question with one more multiple thought step. 
            At each thought step, you can write sql query to analyze data to assist you. 
            Observe what you get at each step to plan for the next step.
            Do not write python code to analyze data.
            You are given following utilities to help you retrieve data.
            1. execute_sql(sql_query: str): A Python function can query data from the <<data_sources>> given a query which you need to create. The query has to be syntactically correct for sql_engine and only use tables and columns under <<data_sources>>. The execute_sql function returns a Python pandas dataframe contain the results of the query.
            2. Don't forget to deal with data quality problem. You should apply data imputation technique to deal with missing data or NAN data.
            3. Always follow the flow of Thought: , Observation:, Action: and Answer: as in template below strictly. 
            4. For coding tasks, only use the functions you have been provided with
            5. You are limited to 2 SQL queries for your analysis.

            <<Table Schema>>{sql_helper.select_sql_table_schema()}<<Table Schema>>
            
            <<Template>>
            Question: User Question
            Thought 1: Your thought here.
            Action: 
            Generate SQL for the User question so that function can call execute_sql() 

            Observation: 
            step1_df is displayed here
            Answer: Your final answer and comment for the question. Also use SQL for computation, never compute result youself.
            Format the result into markdown table and display it here.
            <</Template>>
            Tell others about your analysis to cooperate.
            """,
    llm_config=dataanalysis_llm_config,
)


codeExecutionAgent = autogen.UserProxyAgent(
    name="A3",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="You are team member A3 and you can execute code in python only.",
    code_execution_config={"work_dir": "coding"},  # we don't want to execute code in this case.
    default_auto_reply= None #"Reply `TERMINATE` if the task is done.",
)

analysisExpert = AssistantAgent(
    name="A3",    
    is_termination_msg=termination_msg,
    system_message="""
                You are a team member A3 who can provide expert analysis of data provided to you. 
                Data is provided to you by team member A2.
                Use markdown formatting to format your analysis that can be rendered on HTML page.
                Do not use ``` to write your analysis.
                Once you have the analysis, say out the analysis and append a new line with TERMINATE.
            """,
    llm_config= communicationsExpert_llm_config
)


communicationsExpert = AssistantAgent(
    name="A4",    
    is_termination_msg=termination_msg,
    system_message="""
                You are a team member A4 who is an email communications expert. 
                You can write email on behalf of communications officer or marketing officer.
                You can generate email to customer based on data provided to you.
                Data is provided to you by team member A2. 
                Use markdown formatting to format your email that can be rendered on HTML page.
                Do not use ``` to write your email.
                Use business vocubulary and be polite in your email. 
                Once you have written the email, say out the email and append a new line with TERMINATE.
            """,
    llm_config= communicationsExpert_llm_config
)

agents_A = [dataAnalysisTeamLeader, sqlExpert, codeExecutionAgent] #analysisExpert, communicationsExpert]


visTeamLeader = AssistantAgent(name="B1",
                                        system_message="""You are the team leader B1,
                                        your team consists of B2.                                        
                                        You can talk to the other team leader A1, whose team member is A2, A3. 
                                        Use NEXT: A1 to suggest talking to A1.
                                        """,
                                        llm_config=default_llm_config)

plotlyExpert = AssistantAgent(
    name="B2",
    is_termination_msg=termination_msg,
    system_message="""
            You are a team member B2 who is a plotly expert. You need to acquire data from database and 
            generate plotly chart for the user query.
            Your task is to generate plotly chart in JSON format for the user query. 
            For the plotly chart, use appropriate chart type and color to explain the data to the user. 
            Do not use ```json...``` to write your plotly chart.
            JSON schema is:

            { "plotly_data": "true", "data": [], "dataAnalysis": "data analysis here."}

            example of data field:
            {
                "plotly_data": "true",
                "data": [
                    {
                    "x": ["2016-07-04", "2016-07-05", "2016-07-08", "2016-07-09", "2018-05-04", "2018-05-05", "2018-05-06"],
                    "y": [3080.000, 9317.000, 4657.800, 10793.700, 8108.320, 30132.825, 4889.691],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Eastern",
                    "marker": {"color": "#1f77b4"}
                    },
                    {
                    "x": ["2016-07-04", "2016-07-05", "2016-07-08", "2016-07-09", "2018-05-04", "2018-05-05", "2018-05-06"],
                    "y": ["NaN", "NaN", "NaN", "NaN", "NaN", "NaN", 2320.850],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Westerns",
                    "marker": {"color": "#ff7f0e"}
                    },
                    {
                    "x": ["2016-07-04", "2016-07-05", "2016-07-08", "2016-07-09", "2018-05-04", "2018-05-05", "2018-05-06"],
                    "y": ["NaN", "NaN", "2616.240", "NaN", "NaN", "NaN", 1992.400],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Southern",
                    "marker": {"color": "#2ca02c"}
                    },
                    {
                    "x": ["2016-07-04", "2016-07-05", "2016-07-08", "2016-07-09", "2018-05-04", "2018-05-05", "2018-05-06"],
                    "y": ["NaN", "NaN", "NaN", "NaN", 8108.320, "NaN", "NaN"],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Northern",
                    "marker": {"color": "#d62728"}
                    }
                ],
                "dataAnalysis": "The chart shows the daily revenue trends for different regions over time. Each line represents a region and how its daily revenue fluctuates. Eastern region tends to have higher peaks suggesting significant sales, visible especially on 2018-05-05. Other regions show less fluctuation and lower overall revenue figures. Note: 'NaN' represents days with no data for the particular region."
            }
            Once you have the generated the above data node, say out the answer and append a new line with TERMINATE.
            """,
    llm_config=plotly_llm_config,
)


agents_B = [visTeamLeader, plotlyExpert]



qnaTeamLeader = AssistantAgent(name="C1",
                                        system_message="""You are the team leader C1,
                                        your team consists of C2 and C3. 
                                        You need to retrieve content from search database to answer the user questions.                                                                               
                                        """,
                                        llm_config=default_llm_config)

expertAgent = AssistantAgent(
    name="C2",
    is_termination_msg=termination_msg,
    system_message="""
        You are a team member C2 who helps users with answers to the questions about companies and products.\n 
        You need to retrieve content from search database to answer the user questions.
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
        
    """,
    llm_config=llm_config,
)


retrieverAgent = autogen.UserProxyAgent(
    name="C3",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="You are team member C3 and you can execute code in python only.",
    code_execution_config={"work_dir": "coding"},  # we don't want to execute code in this case.
    default_auto_reply= None #"Reply `TERMINATE` if the task is done.",
)

agents_C = [qnaTeamLeader, expertAgent, retrieverAgent]


# autogen.ChatCompletion.start_logging()

def is_termination_msg(content) -> bool:
    have_content = content.get("content", None) is not None
    if have_content and "TERMINATE" in content["content"]:
        return True
    return False

userProxyAgent = autogen.UserProxyAgent(
    name="userProxyAgent",
    is_termination_msg=is_termination_msg,
    human_input_mode="NEVER",
    system_message="Terminator admin.",
    code_execution_config={"work_dir": "coding"},  # we don't want to execute code in this case.
    default_auto_reply= None #"Reply `TERMINATE` if the task is done.",
)

def _reset_agents():
    userProxyAgent.reset()
    expertAgent.reset()
    sqlExpert.reset()
    communicationsExpert.reset()
    plotlyExpert.reset()



async def start_multiagent_chat(userQuery):   
    #_reset_agents()
    
    #autogen.ChatCompletion.start_logging()

    retrieverAgent.register_function(
        function_map= { 
                        "retrieve_content": search_helper.retrieve_content
                    }
    )   

    codeExecutionAgent.register_function(
        function_map= { 
                        "execute_sql": sql_helper.execute_sql 
                    }
    )   
    
    list_of_agents = agents_A + agents_B + agents_C 
    list_of_agents.append(userProxyAgent)
    
    group_chat = CustomGroupChat(
    agents=list_of_agents,  # Include all agents
    messages=["""Everyone cooperate and help agent to acomplish his task. Team A has A1, A2, A3. Team C has C1, C2 and C3.
              Team B has B1, B2. Only members of the same team can talk to one another. Only team leaders (names ending with 1) can talk amongst themselves. You must use "NEXT: B1" to suggest talking to B1 for example; 
              You can suggest only one person, you cannot suggest yourself or the previous speaker; 
              You can also dont suggest anyone."""],
    #messages=["""Everyone cooperate and help agent B2 in his taskto acomplish the task. Team A has A1, A2, A3. Team C has C1, C2 and C3.
    #          Team B has B1, B2. Only members of the same team can talk to one another. Only team leaders (names ending with 1) can talk amongst themselves. You must use "NEXT: B1" to suggest talking to B1 for example; 
    #          You can suggest only one person, you cannot suggest yourself or the previous speaker; 
    #          You can also dont suggest anyone."""],
    max_round=100)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=default_llm_config)
    agents_C[1].initiate_chat(manager, message=userQuery)
    #userProxyAgent.initiate_chat(manager, message=userQuery)

    print(userProxyAgent.last_message())
    return userProxyAgent.last_message()['content']