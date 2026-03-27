from sqlalchemy import String,Integer,Boolean,Float,Column,ForeignKey
from database import Base

from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__="doctor_data"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100))
    email=Column(String(100),unique=True,nullable=False)
    pwd=Column(String(100),nullable=False)

    patients=relationship("Patient",back_populates="doctor")


class Patient(Base):
    __tablename__="patient_data"
    id=Column(String,primary_key=True)
    name=Column(String(50))
    age=Column(Integer)
    height=Column(Float,nullable=False)
    weight=Column(Float,nullable=False)
    gender=Column(String(10))
    bmi=Column(Float)
    verdict=Column(String)
    doctor_id=Column(Integer,ForeignKey("doctor_data.id"),nullable=False)

    doctor=relationship("Doctor",back_populates="patients")

    
