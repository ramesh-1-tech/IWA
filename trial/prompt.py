from datetime import datetime
from operator import itemgetter

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

import ast
import streamlit as st
import json
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI LLM
llm = OpenAI(api_key=OPENAI_API_KEY)

# Create a function to fetch details and handle missing information
def fetch_appointment_details(user_prompt):

    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["user_prompt", "current_datetime"],
        template="""
        Extract the following information from the user_prompt and do not change them: 
        - Two names
        - Description 
        - Schedule time in UTC.
        - Intention.
        
        Remember below things:
        - current date time is {current_datetime}.
        - If any details are missing, respond with the None keyword.
        - Convert the Schedule_time into datetime utc according to prompt if mentioned into prompt.
        - Find the intention of the user from Create, Update, or Delete.
        - return a list.
        User Prompt: {user_prompt}
        Output format should be: 
        '["user1", "user2", "description", "schedule_time", "intention"]'
        """
    )

    current_datetime = datetime.utcnow().isoformat() + 'Z'
    chain = ({"user_prompt": itemgetter("user_prompt"), "current_datetime": itemgetter("current_datetime")}
             | prompt_template | llm | StrOutputParser())

    result_json = chain.invoke({"user_prompt": user_prompt, "current_datetime": current_datetime})
    breakpoint()
    # Remove leading newline character
    data_string = result_json.strip()

    # Use ast.literal_eval to convert the string to a list
    result_json = ast.literal_eval(data_string)
    # breakpoint()
    try:
        if len(result_json) == 5:
            missing_details = []
            user1 = result_json[0] if result_json[0] else missing_details.append("user1")
            user2 = result_json[1] if result_json[1] else missing_details.append("user2")
            description = result_json[2] if result_json[2] else missing_details.append("description")
            schedule_time = result_json[3] if result_json[3] else missing_details.append("schedule_time")
            if missing_details:
                # missing_prompt = f"Please provide the following details: {', '.join(missing_details)}"
                # missing_response = input(missing_prompt + "\n")
                st.write(f"Please provide the following details: {', '.join(missing_details)}")
                additional = "Additional details: \n"
                # for detail in missing_details:
                #     additional += f'- {detail}: {st.chat_input(f"{detail}: ")}'
                # user_prompt += f". Additional details: {missing_response}"
                return fetch_appointment_details(user_prompt)

            intention = result_json[4]
            input_body = {"user1": user1, "user2": user2, "description": description, "schedule_time": schedule_time}
            return input_body, intention
    except Exception as e:
        return e
    # try:
    #     result_json = json.loads(result)
    #     if "user1" not in result_json or "user2" not in result_json or "description" not in result_json or "schedule_time" not in result_json:
    #         missing_details = []
    #         if "user1" not in result_json:
    #             missing_details.append("user1 name")
    #         if "user2" not in result_json:
    #             missing_details.append("user2 name")
    #         if "description" not in result_json:
    #             missing_details.append("description")
    #         if "schedule_time" not in result_json:
    #             missing_details.append("schedule time in UTC")
    #
    #         missing_prompt = f"Please provide the following details: {', '.join(missing_details)}"
    #         missing_response = input(missing_prompt + "\n")
    #         user_prompt += f". Additional details: {missing_response}"
    #         return fetch_appointment_details(user_prompt)

    #     return result_json
    # except json.JSONDecodeError:
    #     return {"error": "Could not parse JSON response from LLM"}


# Example usage

if user_prompt := st.chat_input():
    appointment_details = fetch_appointment_details(user_prompt)
    st.write(appointment_details)
    print(appointment_details)
# breakpoint()