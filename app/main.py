from fastapi import FastAPI,HTTPException,Depends,Path,Query
from sqlalchemy.orm import Session
from app.database import engine,Base,get_session
from schemas import Patient
from app.core import auth


Base.metadata.create_all(bind=engine)

app=FastAPI(title="Patient Management API",description="API for managing patients",version="1.0.0")
app.include_router(auth.router)



@app.get("/home")
def greet():
    return{
        "Message":"Patient management system api is live!"
    }

