# from langchain.agents import AgentType, create_sql_agent
# from sqlalchemy.ext.declarative import declarative_base
# from langchain_community.agent_toolkits.sql.base import create_sql_agent
from sqlalchemy.orm import sessionmaker

from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
# Create database from dataframe to sql
# if not os.path.exists(db_path):
# df.to_sql("admin_data", engine, index=False)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# schema = db.get_table_info()

# query = "INSERT INTO appointments (doctor_id, nurse_id, appointment_time, date) VALUES ('doctor Aman', 'nurse anna', '6 PM', 'Today');"
# print(db.dialect)
# print(db.get_usable_table_names())
# res = db.run("SELECT * FROM admin_data WHERE Age < 2;")
# prompt = """You are an Assistant designed to interact with a SQL database.
# Given an input question, first check all the table schemas and then create a syntactically correct SQLite query to run. Then, look at the results of the query and return the answer.
# You can order the results by a relevant column to return the most interesting examples in the database.
# Your answer should be detailed and sometimes funny, just like a human assistant.
#
# When performing any DML (Data Manipulation Language) operations such as INSERT, UPDATE, DELETE, or DROP on the database, please follow these guidelines:
#
#     1. You are not allowed to Create or Alter the table.
#     2. Ensure that you execute the operation in a single transaction. If the operation fails, roll back the changes to maintain database integrity.
#     3. Always validate the Data type of all columns in the table.
#     4. If any foreign key constraints fail, roll back the changes and return a "no data found" message.
#     5. If the term "today" is mentioned, it refers to the current date.
#     6. When adding data to any table that contains a foreign key, check if the foreign key value exists in the referenced primary table. If the foreign key value is not present:
#        - return 'Data not found'.
#
# input question:
# """



# agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
# agent_executor.invoke({"input": "How many customers have an order count greater than 500"})
