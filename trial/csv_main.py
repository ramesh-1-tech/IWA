import os

from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI


"""
This may be harmful as it generates LLM python code to convert CSV to dataframe check security in doc: https://python.langchain.com/v0.2/docs/integrations/toolkits/csv/
"""

# Load env data and read keys
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    "../data/admin_data.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)


res = agent.run("how many rows are there?")

breakpoint()