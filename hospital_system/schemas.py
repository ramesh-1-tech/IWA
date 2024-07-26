from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import date, datetime
from typing_extensions import Annotated


class AppointmentSchema(BaseModel):
    description: str
    schedule_time: datetime
    user1: str
    user2: str


class AppointmentDetails(AppointmentSchema):
    id: int

    class Config:
        from_attributes = True


class LeaveCreateSchema(BaseModel):
    reason: str
    user_id: int
    leave_date: date


class LeaveDetails(LeaveCreateSchema):
    id: int

    class Config:
        from_attributes = True


class UserDetailsSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    role: int

    class Config:
        from_attributes = True


class UserListSchema(BaseModel):
    users: list[UserDetailsSchema]

    class Config:
        from_attributes = True
