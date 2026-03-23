from sqlalchemy import String,Integer,Boolean,Float,Column
from database import Base


class Doctor(Base):
    __tablename__="doctor_data"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100))
    email=Column(String(100),unique=True,nullable=False)
    pwd=Column(String(100),nullable=False)


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

    
