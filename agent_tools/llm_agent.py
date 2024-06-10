import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_response(query, conversation_history):
    client = OpenAI()
    
    if conversation_history is None:
        conversation_history = []
    
    full_prompt = "\n".join(conversation_history) + "\n" + query + "\n answer in 1 sentence"
    
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=full_prompt
    )
    return response.choices[0].text.strip()


if __name__ == "__main__":
    query = "who is the president of the United States?"
    response = get_response(query)
    print(response)
