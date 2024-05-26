import os
from dotenv import load_dotenv
from Tool.agent_tools import get_up_to_date_answer_tavily
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub


def answer_query(query):
    load_dotenv()
    
    """ Given a query, return the answer to the query """
    
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    prompt = "Given a query{Question_from_user}, return the answer to the query"
    
    prompt_template = PromptTemplate(input_variables=["Question_from_user"], template=prompt)
    
    tools_for_agent = [
        Tool(name="Crawl Google for the answer", 
             func=get_up_to_date_answer_tavily, 
             description="useful for when you need to get the answer to current data queries")
        ]
    
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})
    
    url_to_Scrape = result["output"]
    
    return url_to_Scrape

    
    
    
    