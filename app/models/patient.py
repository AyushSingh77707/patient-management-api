from sqlalchemy import String,Integer,Boolean,Float,Column,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__="patient_data"
    id=Column(String,primary_key=True,index=True)
    name=Column(String(50),nullable=False)
    age=Column(Integer,nullable=False)
    height=Column(Float,nullable=False)
    weight=Column(Float,nullable=False)
    gender=Column(String(10))
    bmi=Column(Float)
    verdict=Column(String)
    doctor_id=Column(Integer,ForeignKey("doctor_data.id"))   #pointing doctor id of doctor table

    doctor=relationship("Doctor",back_populates="patients")