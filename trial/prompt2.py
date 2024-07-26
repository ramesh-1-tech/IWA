from datetime import datetime
import os
import ast
from operator import itemgetter

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI LLM
llm = OpenAI(api_key=OPENAI_API_KEY)


# Create a function to fetch details and handle missing information
def fetch_appointment_details(user_prompt, current_datetime):
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
    chain = ({"user_prompt": itemgetter("user_prompt"), "current_datetime": itemgetter("current_datetime")}
             | prompt_template | llm | StrOutputParser())

    result_json = chain.invoke({"user_prompt": user_prompt, "current_datetime": current_datetime})

    # Remove leading newline character
    data_string = result_json.strip()

    # Use ast.literal_eval to convert the string to a list
    result_list = ast.literal_eval(data_string)
    return result_list

# def

# Main chat function
def chat():
    st.title("Healthcare AI Assistant")
    user_prompt = st.chat_input("Enter your request:")
    if user_prompt:
        current_datetime = datetime.utcnow().isoformat() + 'Z'
        result_list = fetch_appointment_details(user_prompt, current_datetime)

        # Check for missing details and prompt user for them
        missing_details = []
        details = ['user1', 'user2', 'description', 'schedule_time', 'intention']
        for i, detail in enumerate(details):
            if result_list[i] is None:
                missing_details.append(detail)
        # while missing_details:
        #     for detail in missing_details:
        #         additional_detail = st.chat_input(f"Please provide {detail}:")
        #         if additional_detail:
        #             index = details.index(detail)
        #             result_list[index] = additional_detail
        #     missing_details = [detail for i, detail in enumerate(details) if result_list[i] is None]

        # Output the final details
        if current_details := st.session_state.get("current_details"):
            input_body = {
                "user1": result_list[0] if result_list[0] else current_details.get("user1"),
                "user2": result_list[1] if result_list[1] else current_details.get("user2"),
                "description": result_list[2] if result_list[2] else current_details.get("description"),
                "schedule_time": result_list[3] if result_list[3] else current_details.get("schedule_time"),
            }
        else:
            input_body = {
                "user1": result_list[0],
                "user2": result_list[1],
                "description": result_list[2],
                "schedule_time": result_list[3]
            }
        st.session_state["missing_details"] = missing_details
        intention = result_list[4]
        input_body.update({"intention": intention})
        st.session_state["current_details"] = input_body
        breakpoint()

        st.write("Appointment Details:")
        st.json(input_body)
        st.write(f"Intention: {intention}")
        st.write(f"missing details: {missing_details}")


# Run the chat function
if __name__ == "__main__":
    chat()
