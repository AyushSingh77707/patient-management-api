from fastapi import APIRouter,HTTPException,Depends,Query
from app.database import get_session
from app.core.dependencies import get_current_user
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from sqlalchemy.orm import Session
from math import math


router=APIRouter(prefix="/patients",tags=["Patients Manipulation"])

@router.post("/create")
def create_patient(info:PatientCreate,db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    patient_data = info.model_dump()
    patient_data["doctor_id"] = current_user.id
    new_patient=Patient(**patient_data)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

#normal view
@router.get("/view")
def view_all(db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    data=db.query(Patient).all()
    return data

#view_using pagination feature and sorting together
@router.get("/view_once")
def view_once(
    page:int=Query(default=1,ge=1,description="Enter the page number here!"),
    limit:int=Query(default=10,ge=1,le=50),
    sort_by:str=Query(default="id"),
    order:str=Query(default="asc"),
    db:Session=Depends(get_session),
    current_user=Depends(get_current_user)
):
    offset=(page-1)*limit
    total=db.query(Patient).count()
    total_page=math.ceil(total/limit)

    column=getattr(Patient,sort_by,Patient.id)
    if order=="desc":
        column=column.desc()

    data=db.query(Patient)\
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


@router.get("/{patient_id}")
def view_one(patient_id:int,db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    data=db.query(Patient).filter(Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    return data

@router.delete("/{patient_id}")
def del_patient(patient_id:int,db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    data=db.query(Patient).filter(Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    db.delete(data)
    db.commit()
    return {'message':'patient deleted successfully!'}


@router.patch("/{patient_id}")
def update_patient(patient_id:int,info:Patient,db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    data=db.query(Patient).filter(Patient.id==patient_id).first()
    if not data:
        raise HTTPException(status_code=404,detail='patient not found!')
    
    if info.age is not None: data.age=info.age
    if info.name is not None: data.name=info.name
    if info.height is not None: data.height=info.height
    if info.weight is not None: data.weight=info.weight

    if info.gender is not None: data.gender=info.gender 
    if info.doctor_id is not None: data.doctor_id = info.doctor_id 

    db.commit()
    db.refresh(data)
    return {'message':'patient updated succesfully!'}


@router.get("/{doctor_id}/patients")
def get_doctor_patients(doctor_id:int,db:Session=Depends(get_session),current_user=Depends(get_current_user)):
    doctor=db.query(Doctor).filter(Doctor.id==doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404,detail="doctor not found!")    
    
    return{
        "doctor":doctor.name,
        "total_patients":len(doctor.patients),
        "Patient_data":doctor.patients
    }
