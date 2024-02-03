import aiohttp
import json
import sql_helper

url = f"http://10.0.0.43:28080/mii/phi2-deployment"



async def get_slm_response(query):
    
    
    user_prompt = f"""
    
    Generate a SQL query to answer the following question:
    {query}
    <<Table Schema>>{sql_helper.select_sql_table_schema()}<<Table Schema>>

    SQL Query:
    
    """
    
    params = {"prompts": [user_prompt], "max_length": 500}
    json_params = json.dumps(params)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, 
                                data=json_params, 
                                headers={'Content-Type': 'application/json'}) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                # Handle error here (e.g., log it, raise an exception, etc.)
                return None
    #output = requests.post(
    #    url, data=json_params, headers={"Content-Type": "application/json"}
    #)
    #return output.json()[0]["generated_text"].split("\n")[0]
    #return ""