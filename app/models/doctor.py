from sqlalchemy import String,Integer,Boolean,Float,Column,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__="doctor_data"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    password=Column(String(100),nullable=False)

    patients=relationship("Patient",back_populates="doctor")