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
from google_calendar import list_upcoming_events
from general_llm_tool import get_response
from langchain_core.memory import ConversationBufferMemory
import json

# File to persist memory
MEMORY_FILE = "memory.json"

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory.load_memory_variables(), f)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            memory_variables = json.load(f)
        return ConversationBufferMemory.from_memory_variables(memory_variables)
    else:
        return ConversationBufferMemory()

def answer_query(query, conversation_history=None):
    load_dotenv()
    
    """ Given a query, return the answer to the query """
    
    memory = load_memory()
    
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    prompt_template = PromptTemplate(input_variables=["Question_from_user"], template="Given a query {Question_from_user}, return the answer to the query")
    
    tools_for_agent = [
        Tool(name="Get Recent Emails",
             func=get_email_messages,
             description="useful for when you need to read recent emails"),
        Tool(name="List Upcoming Events",
             func=lambda _: list_upcoming_events(),  # Ensure the function is called without passing the query string
             description="useful for fetching upcoming Google Calendar events"),
        Tool(name="General Knowledge",
             func=lambda query: get_response(query, conversation_history),
             description="useful for answering general knowledge questions using GPT-3.5")
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
        memory=memory
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(Question_from_user=query)})
    
    final_output = result["output"]
    print(result)
    
    # Update memory with the new interaction
    memory.add_memory(result["input"]["input"], final_output)
    save_memory(memory)
    
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
