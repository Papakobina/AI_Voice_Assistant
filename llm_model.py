import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from handle_gmail import get_email_messages
from handle_calendar import list_upcoming_events
from llm_agent import get_response
import json

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# File to persist memory
MEMORY_FILE = "memory.json"


def answer_query(query, conversation_history=None):
    load_dotenv()
    
    """ Given a query, return the answer to the query """
        
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    prompt_template = PromptTemplate(input_variables=["Question_from_user"], template="Given a query {Question_from_user}, return the answer to the query")
    
    tools_for_agent = [
        Tool(name="Get Recent Emails",
             func=get_email_messages,
             description="useful for when you need to read recent emails"),
        Tool(name="List Upcoming Events",
             func=list_upcoming_events,
             description="useful for fetching upcoming Google Calendar events or fetching scheduled events"),
        Tool(name="General Knowledge",
             func=lambda query: get_response(query, conversation_history),
             description="useful for answering general knowledge questions using GPT-3.5")
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(Question_from_user=query)})
    
    final_output = result["output"]
    print(result)
    
    return final_output

if __name__ == '__main__':
    query = "what is quantum computing?"
    response = answer_query(query)
    print(response)
    
    query = "Fetch my recent emails"
    response = answer_query(query)
    print(response)
    
    query = "What are my upcoming events?"
    response = answer_query(query)
    print(response)
