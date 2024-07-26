from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .schemas import AppointmentDetails, AppointmentSchema, LeaveDetails, LeaveCreateSchema, UserListSchema
from .database import get_db
from .models import Appointments, Leaves, User

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello to Hospital System"}

@app.post("/create_appointments", response_model=AppointmentDetails, status_code=201)
async def create_appointments(appointment_data: AppointmentSchema, db: Session = Depends(get_db)):
    appointment = Appointments(**appointment_data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@app.put("/update_appointments", response_model=AppointmentDetails, status_code=201)
async def update_appointments(appointment_data: AppointmentDetails, db: Session = Depends(get_db)):
    # appointment = Appointments(**appointment_data.model_dump())
    appointment_query = db.query(Appointments).filter(appointment_data.id == Appointments.id)
    if appointment_query.first() is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    # db.add(appointment)
    appointment_query.update(appointment_data.model_dump(), synchronize_session=False)
    db.commit()
    # db.refresh(appointment)
    return appointment_data


@app.post("/add_leave", response_model=LeaveDetails, status_code=201)
async def create_leave(leave_details: LeaveCreateSchema, db: Session = Depends(get_db)):
    db_leave = Leaves(**leave_details.model_dump())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


@app.get("/users", response_model=UserListSchema, status_code=200)
async def get_user_list(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}
