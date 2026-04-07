from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.core.security import hash_pwd,create_token,verify_pwd,verify_token
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.doctor import DoctorLogin,DoctorRegister
from app.schemas.patient import PatientCreate

router=APIRouter(prefix="/auth",tags=["Authentication"])

#register endpoint
@router.post("/register")
def register_doctor(info:DoctorRegister,db:Session=Depends(get_session)):
    existing=db.query(Doctor)\
    .filter(Doctor.email==info.email)\
    .first()

    if existing:
        raise HTTPException(status_code=400,detail='email already exists!')
    
    new_doctor=Doctor(              
        name=info.name,
        email=info.email,
        password=hash_pwd(info.pwd)             #password hash krke save
    )
    db.add(new_doctor)
    db.commit()
    return {"message":"doctor registered successfully!"}

@router.post("/login")
def login_doctor(info:DoctorLogin,db:Session=Depends(get_session)):
    doctor=db.query(Doctor)\
    .filter(Doctor.email==info.email)\
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