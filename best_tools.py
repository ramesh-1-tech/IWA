import json

import requests
from langchain.pydantic_v1 import BaseModel, Field
from datetime import datetime, date


class AppointmentSchema(BaseModel):
    user1: str = Field(description="first user")
    user2: str = Field(description="second user")
    description: str = Field(description="description of the appointment")
    schedule_time: datetime = Field(description="schedule datetime object")


def create_appointment_api(user1: str, user2: str, description: str, schedule_time) -> str:
    """Create an appointment."""

    appointment_info = {"user1": user1, "user2": user2, "description": description, "schedule_time": str(schedule_time)}

    # get parameters and call the api
    headers = {"content-type": "application/json",
               "content-length": str(len(appointment_info))}
    response = requests.post("http://127.0.0.1:8000/create_appointments", headers=headers, json=appointment_info)
    if response.status_code == 201:
        return response.json()
    else:
        return response.text


class LeaveSchema(BaseModel):
    user_id: int = Field(description="id of user from Users table if available for which the leave is adding.")
    reason: str = Field(description="reason of the leave")
    leave_date: date = Field(description="date of leave")


def add_leave_api(user_id: int, reason: str, leave_date) -> str:
    """Create or Add a Leave."""

    leave_info = {"user_id": user_id, "reason": reason, "leave_date": str(leave_date)}
    # get parameters and call the api
    headers = {"content-type": "application/json",
               "content-length": str(len(leave_info))}
    response = requests.post("http://127.0.0.1:8000/add_leave", headers=headers, json=leave_info)
    if response.status_code == 201:
        return response.json()
    else:
        return response.text


def fetch_user_list() -> str:
    """get users list."""
    # get parameters and call the api
    # headers = {"content-type": "application/json",
    #            "content-length": '0'}
    response = requests.get("http://127.0.0.1:8000/users")
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


class LeaveSchema(BaseModel):
    user_id: int = Field(description="id of user from Users table if available for which the leave is adding.")
    reason: str = Field(description="reason of the leave")
    leave_date: date = Field(description="date of leave")


def add_leave_api(user_id: int, reason: str, leave_date) -> str:
    """Create or Add a Leave."""

    leave_info = {"user_id": user_id, "reason": reason, "leave_date": str(leave_date)}
    # get parameters and call the api
    headers = {"content-type": "application/json",
               "content-length": str(len(leave_info))}
    response = requests.post("http://127.0.0.1:8000/add_leave", headers=headers, json=leave_info)
    if response.status_code == 201:
        return response.json()
    else:
        return response.text


class UpdateAppointmentSchema(AppointmentSchema):
    id: int = Field(description="id of the appointment.")


def update_appointment_api(id: int, user1: str, user2: str, description: str, schedule_time) -> str:
    """Create an appointment."""

    appointment_info = {"id": id, "user1": user1, "user2": user2, "description": description, "schedule_time": str(schedule_time)}
    print(appointment_info)
    # get parameters and call the api
    headers = {"content-type": "application/json",
               "content-length": str(len(appointment_info))}
    response = requests.put("http://127.0.0.1:8000/update_appointments", headers=headers, json=appointment_info)
    if response.status_code == 201:
        return response.json()
    else:
        return response.text
