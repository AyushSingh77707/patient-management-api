from fastapi import FastAPI,HTTPException,Depends,Path,Query
from sqlalchemy.orm import Session
from database import engine,Base,get_session
import models
from schemas import Patient




app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/create")
def create_patient(info:Patient,db : Session=Depends(get_session)):
    new_patient=models.Patient(**info.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@app.get("/view")
def view_all(db:Session=Depends(get_session)):
    data=db.query(models.Patient).all()
    return data

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

