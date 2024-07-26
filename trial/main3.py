import os
import pandas as pd
import requests
import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine


from langchain_openai import OpenAI, ChatOpenAI
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, SystemMessage
from prompt import fetch_appointment_details
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import create_openai_tools_agent, create_tool_calling_agent
from langchain.agents.agent import AgentExecutor
from langchain.tools import StructuredTool

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
# Load env data and read keys
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Read CSV file and convert into database (One time operation)
df = pd.read_csv("../data/admin_data.csv")
db_path = "../data/sql_app.db"
new_db_path = f"sqlite:///{db_path}"

def create_appointment_api(human_message):
    """Call the FastAPI endpoint to create an appointment"""

    # get intention and appointment info
    appointment_info, intention = fetch_appointment_details(human_message)
    # based on intention call the APIs
    if intention.lower() == 'create':
        response = requests.post("http://127.0.0.1:8000/create_appointments", json=appointment_info)
        if response.status_code == 201:
            return response.json()
    elif intention.lower() == 'update':
        response = requests.post("http://127.0.0.1:8000/update_appointments", json=appointment_info)
        if response.status_code == 200:
            return response.json()
    elif intention.lower() == 'delete':
        response = requests.post("http://127.0.0.1:8000/delete_appointments", json=appointment_info)
        if response.status_code == 200:
            return response.json()
engine = create_engine(
    new_db_path, connect_args={"check_same_thread": False}
)

db = SQLDatabase(engine=engine)

# prompt = """You are an Assistant designed to interact with a SQL database.
# Given an input question, first check all the table schemas and then create a syntactically correct SQLite query to run. Then, look at the results of the query and return the answer.
# You can order the results by a relevant column to return the most interesting examples in the database.
# Your answer should be detailed and sometimes funny, just like a human assistant.
#
# You are not allowed to perform any DML (Data Manipulation Language) operations such as INSERT, UPDATE, DELETE, or DROP on the database, if you asked to do any DML Operation then please return the answer that 'I am afraid i am not allowed to do such operations':
#
# input question:
# """

# Initialize the OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()


create_appointment_tool = StructuredTool.from_function(
    func=create_appointment_api,
    name="CreateAppointment",
    description="useful for when you need to create or schedule an appointment.",
)
all_tools = toolkit.get_tools()
all_tools.append(create_appointment_tool)

# SQL_FUNCTIONS_SUFFIX = """I should look at the tables in the database to see what I can query. Then I should query the schema of the most relevant tables. If i don't find the answer then i will give response 'I am sorry i can't help you in this'"""
# prompt = ChatPromptTemplate.from_messages([
#         SystemMessagePromptTemplate.from_template(
#             input_variables=['tool_names', 'tools'],
#             template=SQL_FUNCTIONS_SUFFIX
#         ),
#         MessagesPlaceholder(variable_name='chat_history', optional=True),
#         HumanMessagePromptTemplate.from_template(
#             input_variables=["input", "chat_history", "agent_scratchpad"],
#             template=HUMAN_PROMPT_TEMPLATE
#         )
#     ])

SQL_FUNCTIONS_SUFFIX = """I am a smart agent who will look into the query and decide what to do with that. 
i will understand the intention of the query and use a correct tool to fulfill the request i can use multiple tools at same time as well. 
for example if query is asking for some details from database then I should look at the tables in the database to see what I can query. Then I should query the schema of the most relevant tables. I am not allowed to do any DML operations directly."""
# messages = [
#     MessagesPlaceholder(variable_name="history", optional=True),
#     HumanMessagePromptTemplate.from_template("{input}"),
#     AIMessage(content=SQL_FUNCTIONS_SUFFIX),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ]

# store = {}

#
# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

# messages = [
#     SystemMessage(content="You are an Assistant designed to interact with a SQL database."),
#     MessagesPlaceholder(variable_name="history"),  # Include history placeholder
#     HumanMessagePromptTemplate.from_template("{input}"),
#     AIMessage(content=SQL_FUNCTIONS_SUFFIX),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ]
# chat_prompt = ChatPromptTemplate.from_messages(messages)
# prompt = chat_prompt.partial(**context)

# SQL_FUNCTIONS_SUFFIX = """I should review the chat history to understand the context and requirements.
# if requires I should look at the tables in the database to see what I can query. I will use perfect tool to query the schema of the most relevant tables.
# I will use the tools"""
# SQL_FUNCTIONS_SUFFIX = """I should review the chat history to understand the context and requirements.
# Then, I will examine the tables in the database and identify relevant queries.
# I will query the schema of the most relevant tables to gather necessary information. I am not allowed to perform any DML operations directly."""
# AIMessage(content=SQL_FUNCTIONS_SUFFIX),
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are very powerful agent using tools to perform actions.
            You should have to follow some instructions.
            - You are not allowed to do any DML operations like INSERT, UPDATE, DELETE directly.
            - you will look at the input and decide what to do.
            - You are not allowed to return schema of tables.
            - If there are any tools to do some task than use only that tool to do that operations.
            """,
        ),

        # MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the memory buffer
# memory = ConversationBufferMemory(memory_key="history", max_token_limit=1024)

# memory = ChatMessageHistory(session_id="test-session")
# breakpoint()
# Define the conversation chain
# conversation = ConversationChain(
#     llm=llm,
#     memory=memory,
#     prompt=chat_prompt,  # Fill in context if needed
#     input_variables=["input", "history", "agent_scratchpad"]
# )
# breakpoint()
# agent = create_openai_tools_agent(llm, all_tools, prompt)
agent = create_openai_tools_agent(llm, all_tools, prompt)

# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=all_tools,
#     verbose=True,
# )


agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    verbose=True,
)

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     # This is needed because in most real world scenarios, a session id is needed
#     # It isn't really used here because we are using a simple in memory ChatMessageHistory
#     lambda session_id: memory,
#     input_messages_key="input",
#     history_messages_key="history",
# )

# with_message_history = RunnableWithMessageHistory(
#     agent_executor,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="history"
# )

# schedule an appointment of maan and geet at 6 PM today.
# res = agent_executor.invoke({"input": "Give me details of all appointment of dhara and also give me count of that"})
if input_prompt := st.chat_input("Enter your input"):
    # res = with_message_history.invoke(
    #     {"input": input_prompt},
    #     config={"configurable": {"session_id": "abc123"}},
    # )
    # res = agent_with_chat_history.invoke(
    #     {"input": input_prompt},
    #     config={"configurable": {"session_id": "<foo>"}},
    # )
    res = agent_executor.invoke({"input": input_prompt})
    output = res["output"]
    st.write(output)
