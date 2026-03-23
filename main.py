from fastapi import FastAPI,HTTPException,Depends,Path,Query
from sqlalchemy.orm import Session
from database import engine,Base,get_session
import models
from schemas import Patient
import math

from auth import hash_pwd,verify_pwd,verify_token,create_token
from fastapi.security import OAuth2PasswordBearer
outh2_scheme=OAuth2PasswordBearer(tokenUrl="Login")
from schemas import DoctorRegister,DoctorLogin

app=FastAPI()
Base.metadata.create_all(bind=engine)

#register endpoint
@app.post("/register")
def register_doctor(info:DoctorRegister,db:Session=Depends(get_session)):
    existing=db.query(models.Doctor)\
    .filter(models.Doctor.email==info.email)\
    .first()

    if existing:
        raise HTTPException(status_code=400,detail='email already exists!')
    
    new_doctor=models.Doctor(              
        name=info.name,
        email=info.email,
        pwd=hash_pwd(info.pwd)             #password hash krke save
    )
    db.add(new_doctor)
    db.commit()
    return {"message":"doctor returned successfully!"}

@app.post("/login")
def login_doctor(info:DoctorLogin,db:Session=Depends(get_session)):
    doctor=db.query(models.Doctor)\
    .filter(models.Doctor.email==info.email)\
    .first()

    if not doctor or not verify_pwd(info.pwd,doctor.pwd):
        raise HTTPException(status_code=401,detail='invaild email or password')
    
    token=create_token(
        {"user_id":doctor.id,
         "email":doctor.email}
    )
    return{
        "access_token":token,
        "token_type":"bearer"
    }











@app.post("/create")
def create_patient(info:Patient,db : Session=Depends(get_session)):
    new_patient=models.Patient(**info.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

#normal view
@app.get("/view")
def view_all(db:Session=Depends(get_session)):
    data=db.query(models.Patient).all()
    return data

#view_using pagination feature and sorting together
@app.get("/view_once")
def view_once(
    page:int=Query(default=1,ge=1,description="Enter the page number here!"),
    limit:int=Query(default=10,ge=1,le=50),
    sort_by:str=Query(default="id"),
    order:str=Query(default="asc"),
    db:Session=Depends(get_session)
):
    offset=(page-1)*limit
    total=db.query(models.Patient).count()
    total_page=math.ceil(total/limit)

    column=getattr(models.Patient,sort_by,models.Patient.id)
    if order=="desc":
        column=column.desc()

    data=db.query(models.Patient)\
    .order_by(column)\
    .offset(offset)\
    .limit(limit)\
    .all()

    return{
        "Total patients in database":total,
        "Total Pages":total_page,
        "current page":page,
        "has_next":page<total_page,
        "has_prev":page>1,
        "Patient data":data
    }




@app.get("/view/{patient_id}")
def view_one(patient_id:str,db:Session=Depends(get_session)):
    data=db.query(models.Patient).filter(models.Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    return data

@app.delete("/del/{patient_id}")
def del_patient(patient_id:str,db:Session=Depends(get_session)):
    data=db.query(models.Patient).filter(models.Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    db.delete(data)
    db.commit()
    return {'message':'patient deleted successfully!'}


@app.patch("/update/{patient_id}")
def update_patient(patient_id:str,info:Patient,db:Session=Depends(get_session)):
    data=db.query(models.Patient).filter(models.Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    
    if info.age is not None: data.age=info.age
    if info.name is not None: data.name=info.name
    if info.height is not None: data.height=info.height
    if info.weight is not None: data.weight=info.weight

    if info.gender is not None: data.gender=info.gender 

    db.commit()
    db.refresh(data)
    return {'message':'patient updated succesfully!'}

