

import os
import base64
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent,Tool,AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import HumanMessage
from langchain.vectorstores import FAISS

from tools1 import tools


# Logging setup
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Set up API key
load_dotenv()
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
if not OPEN_AI_KEY:
    raise ValueError("Missing OpenAI API key. Ensure it is set in your environment.")


# Initialize LLM
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    openai_api_key=OPEN_AI_KEY,  # Replace with your actual key
    max_tokens=2000
)

# Add Memory to Store Context
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

def custom_error_handler(e):
    return f"Parsing error: {str(e)}"

# Initialize agent (assuming tools is defined elsewhere)
agent = initialize_agent(
    tools=tools,  # Replace with actual tools if needed
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=custom_error_handler,
    memory=memory,
)

# Function to generate dynamic suggestions
def generate_dynamic_suggestions(user_input):
    """Generates dynamic suggestions based on the user's last message using the LLM."""
    prompt = f"""
    Based on the user's input: '{user_input}', generate 4 relevant follow-up questions that the user might want to ask next.
    Provide the suggestions as a list of strings, focusing on real estate-related queries.
    Ensure the suggestions are concise, specific, and contextually appropriate.
    """
    try:
        response = llm.predict_messages([HumanMessage(content=prompt)])
        suggestions = response.content.strip().split("\n")
        # Clean up suggestions (remove numbering or extra formatting if present)
        suggestions = [s.strip().lstrip("1234. -") for s in suggestions if s.strip()]
        return suggestions[:4]  # Ensure we return exactly 4 suggestions
    except Exception as e:
        # Fallback in case of errors
        return [
            "What are the properties near this location?",
            "Can you show me price trends in this area?",
            "Are there any RERA-approved projects here?",
            "What’s the EMI for a property in this range?"
        ]

