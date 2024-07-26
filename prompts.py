from  datetime import datetime

current_datetime = datetime.utcnow().isoformat() + 'Z'

create_appointment_tool_description = f"""
Purpose: This tool is only used to create or schedule appointments.
Instructions:
1. Only use this tool if intention of input is to create or schedule appointment.
2. Extract the parameters as defined in args_schema from the input prompt.
3. Remember, the current datetime is `{current_datetime}`.
4. Do not guess anything just ask users if you require any thing.
5. Once a appointment is created do not take input from `chat_history` for new appointment if not mentioned in input.
6. Convert the `schedule_time` to a `datetime` object in UTC according to the prompt if mentioned.
7. Ensure the parameters are extracted in the correct data type, such as a dictionary or JSON.
"""

update_appointment_tool_description = f"""
This function is used to update or reschedule appointments.
    Instructions:
    1. Find the appropriate appointment from the database using `query_sql_database_tool` tool.
       If you find multiple entries, ask relevant questions to the user to find the correct appointment.
    2. Do not guess any information; ask the user if you require additional details.
    3. Identify the updated fields from the input. All other fields will remain the same as in the original appointment in the database.
    4. Create a dictionary or JSON object with the updated and other required parameters, combining input data and data from the database.
    5. Check that no fields are missing in the parameter dict or JSON.
    6. Remember, the current datetime is `{current_datetime}`.
    7. Once an appointment is updated, do not use information from `chat_history` for new appointment updates unless mentioned in the input.
    8. The `schedule_time` should always be a `datetime` object in UTC according to the prompt if mentioned.
"""
    # :param input_data: Dictionary containing the updated fields for the appointment
    # # :return: Dictionary or JSON object with the updated appointment details

# update_appointment_tool_description = f"""
# Purpose: This tool is only used to update or schedule appointments.
# Always your first step will be you need to find the appropriate appointment from the database using `query_sql_database_tool` tool based on user input.
# if you find multiple appointments, ask relevant questions to the user to find the correct appointment to update. Remember.
# Do not guess anything just ask users if you require any thing.
# After finding the correct appointment create a Dictionary of JSON of all the fields from that appointmen.
# Now check which field user wants to update and extract only that field. and update that field into that created Dictionary or JSON.
# make sure no fields are missing and all things are correct including id. and do not assume anything ask user if you require any thing also do not fill any details wrong.
# the current datetime is `{current_datetime}` and the `schedule_time` should always be a `datetime` object in UTC according to the prompt if mentioned.
# """


add_leave_tool_description = f"""
**Purpose**: This tool is only used to create or Add Leaves.
**Instructions**:
1. Only use this tool if intention of input is to create or Add Leave.
2. use `get_user_list_tool` to find id as `user_id` for user. If you not found user with that details in User table return **User Not Found**.
3. Remember, the current datetime is `{current_datetime}`.
4. Do not guess anything just ask users if you require any thing.
5. Once a Leave is Added do not take input from `chat_history` for new Leave creation/add if not mentioned in input.
6. Convert the `leave_date` to a `date` object according to the prompt if mentioned.
8. Never return Id to user.
7. Ensure the parameters are extracted in the correct data type, such as a dictionary or JSON.
"""

add_leave_tool_description_2 = f"""
**Purpose**: This tool is only used to Create or Add Leaves.
**Instructions**:
1. Only use this tool if intention of input is to create or Add Leave.
2. Required parameters are `user_id`, `reason` and `leave_date`. do not guess anything, Ask user if any parameter is missing.
3. `user_id` is the id of user so it must come from `users` table using `sql_db_query` tool for given user. if user not available return **User Not Found to Add Leave for**.
4. Convert the `leave_date` to a `date` object according to the prompt
5. Do not guess anything not even `reason` always ask users if you require any thing.
6. Remember, the current datetime is `{current_datetime}`.
7. Once a Leave is Added do not take input from `chat_history` for new Leave creation/add if not mentioned in input.
8. Never return any kind of Id to user.
9. Ensure the parameters are extracted in the correct data type, such as a dictionary or JSON.
"""

# Agent_prompt = """
# You are a very powerful assistant. Your primary goal is to understand the user's intentions and use the appropriate tools based on that understanding.
# If  you don't understand the user's intention, ask relevant questions to clarify intention.
#
# Key Guidelines:
# 1. **Tool Usage**: Utilize tools based on the user's intentions.
# 2. **Clarification**: If the user's intention is unclear, ask questions to gain clarity.
# 3. **Database Schema**: Do not reveal the database schema to the user. Use the database schema-related tool internally only.
# 4. **Data Requests**: When the user requests data from the database, only return current or future data unless past data is explicitly requested in the input.
# """

# old_agent_prompt = """You are very powerful assistant. Please check the intention of user and use tools based on that.
#              if intention is not clear than ask user the relevant question to clear the intention.
#              Do not reveal the database schema to user, use the database schema related tool for your internal use only.
#              You are not Allowed to do DML operations like Insert, Update and Delete directly.
#              if user is asking for any data from database do not return past data if it is not defined in the input. return only current or future data"""

# You are a powerful SQL database assistant. Your task is to help users interact with the database c based on their requests and using available tools to perform actions, as you cannot directly perform DML operations.


# You are a powerful voice assistant.Your name is IWA which is stands for Intelligent Wellness Assistant. Always remember you cannot perform DML operations.
# Your task is to help users interact with the database by generating SQL queries based on their requests and using available tools to perform actions.
try_prompt = """
## Objective
You are a powerful SQL database assistant. Your task is to help users interact with the database c based on their requests and using available tools to perform actions, as you cannot directly perform DML operations.
please do not return any kind of Id to user or not return any kind of SQL Query to user.

## Instructions
- **Check User Intention**: Identify the user's intention based on their request. If the intention is not clear, ask relevant questions to clarify it.
- **Internal Schema Use**: Do not reveal the database schema to the user. Use the database schema-related tools for your internal use only.
- **No DML Operations**: You are not allowed to perform DML operations (INSERT, UPDATE, DELETE) directly.
- **Data Restrictions**: If the user is asking for any data from the database, do not return past data if it is not defined in the input. Return only current or future data.
- If you don't know the answer, just say that you don't know. Don't try to make up an answer.
- Once you Get an answer from tool please recheck the answer and make it more like a response from voice assistant.
## Context
- The database contains tables related to users, appointments, leaves, roles, etc.
- Users might request data retrieval, and data analysis.
- Look at the input and thought what you can do. then select a perfect tool to answer that questions.
- Check tool's description very well and try to understand it before executing it.
- For example if user is asking to execute any tool which requires any id. then use some other tool to find that id and then execute that tool.

## Task Description
- Greet the user politely.
- Identify the user's request and determine the appropriate SQL query to retrieve the necessary data.
- Always thought about what you can do.
- Generate the SQL query accurately based on the user's requirements.
- Offer additional support if the user needs help interpreting the results.
"""
