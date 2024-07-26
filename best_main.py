import os
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from langchain_core.tools import StructuredTool

from sqlalchemy import create_engine
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, initialize_agent, AgentType
from langchain.agents import AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from best_tools import create_appointment_api, AppointmentSchema, add_leave_api, LeaveSchema, fetch_user_list, \
    update_appointment_api, UpdateAppointmentSchema
from prompts import (
    create_appointment_tool_description, try_prompt, add_leave_tool_description, add_leave_tool_description_2,
    update_appointment_tool_description
)

# Get the prompt to use - you can modify this!
# prompt = hub.pull("hwchase17/openai-functions-agent")
# prompt.messages

st.title("IWA")
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

db_path = "data/sql_app.db"
new_db_path = f"sqlite:///{db_path}"

engine = create_engine(
    new_db_path, connect_args={"check_same_thread": False}
)
db = SQLDatabase(engine=engine)

# try with 16K
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

MEMORY_KEY = "chat_history"

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            try_prompt,
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

create_appointment_tool = StructuredTool.from_function(
    func=create_appointment_api,
    name="CreateAppointmentTool",
    description=create_appointment_tool_description,
    args_schema=AppointmentSchema,
    handle_tool_error=True,
)

update_appointment_tool = StructuredTool.from_function(
    func=update_appointment_api,
    name="UpdateAppointmentTool",
    description=update_appointment_tool_description,
    args_schema=UpdateAppointmentSchema,
    handle_tool_error=True,
)

add_leave_tool = StructuredTool.from_function(
    func=add_leave_api,
    name="CreateLeaveTool",
    description=add_leave_tool_description_2,
    args_schema=LeaveSchema,
    handle_tool_error=True,
)

get_user_list_tool = StructuredTool.from_function(
    func=fetch_user_list,
    name="GetUserListTool",
    description="useful when you need a list of users",
    # args_schema=,
    handle_tool_error=True,
)


custom_tools = [create_appointment_tool, add_leave_tool, get_user_list_tool, update_appointment_tool]
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()
tools.extend(custom_tools)

# agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
prompt = prompt.partial(**context)
# if query:= st.chat_input():
agent = create_tool_calling_agent(llm, tools, prompt)
# ans = llm_with_tools.invoke("give me details of database schema")
# st.write(ans)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

if "history" not in st.session_state:
    st.session_state["history"] = {}
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "123"

session_id = st.session_state.get("session_id")


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state["history"]:
        st.session_state["history"][session_id] = ChatMessageHistory()
    return st.session_state["history"][session_id]


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key=MEMORY_KEY,
)

if user_input := st.chat_input("Enter your prompt"):
    res = agent_with_chat_history.invoke({"input": user_input}, config={"configurable": {"session_id": session_id}}, )
    # st.write(res["output"])
    history = st.session_state["history"]
    if "history" and "session_id" in st.session_state:
        history = st.session_state["history"]
        if history:
            for message in history.get(st.session_state["session_id"]).messages:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)

# res = agent_executor.invoke({"input": "hi!"})

print("here is ending")
