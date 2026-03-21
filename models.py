from sqlalchemy import String,Integer,Boolean,Float,Column
from database import Base

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

    
