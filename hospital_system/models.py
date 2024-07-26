from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, DATE
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    role = Column(Integer, ForeignKey("roles.id"), nullable=False, default=1)

# Role model
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    # permissions = relationship("Permission", back_populates="roles")
    # users = relationship("User", back_populates="roles")

# Permission model
# class Permission(Base):
#     __tablename__ = "permissions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True)
#     roles = relationship("Role", back_populates="permissions")

class Appointments(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    schedule_time = Column(DateTime, nullable=False)
    user1 = Column(String, nullable=False)
    user2 = Column(String, nullable=False)


# class AppointmentUserDetails(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     users = relationship('User', foreign_keys=("users.id"), back_populates="appointment")
#     appointments = relationship('Appointments', foreign_keys=("appointments.id"), back_populates="users")


class Leaves(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_date = Column(DATE, nullable=False)
