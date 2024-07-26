from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
import os
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load env data and read keys
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Read CSV file and convert into database (One time operation)
df = pd.read_csv("../data/admin_data.csv")
db_path = "../data/test_sqldb.db"
new_db_path = f"sqlite:///{db_path}"

#

engine = create_engine(
    new_db_path, connect_args={"check_same_thread": False}
)
# breakpoint()
# Create database from dataframe to sql
# if not os.path.exists(db_path):
# df.to_sql("admin_data", engine, index=False)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

db = SQLDatabase(engine=engine)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
generate_query = create_sql_query_chain(llm, db)
query = generate_query.invoke({"question": "what is billing amount of Enna"})
execute_query = QuerySQLDataBaseTool(db=db)
execute_query.invoke(query)

# "what is price of `1968 Ford Mustang`"
print(query)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

rephrase_answer = answer_prompt | llm | StrOutputParser()

chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
)

chain.invoke({"question": "How many customers have an order count greater than 500"})
breakpoint()