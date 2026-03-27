'''auth.py me 4 kam honge
1.password hashing
2.password verify
3.token generate
4.token verification'''
from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext

#creating get_current_user
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_session
import models

#setting environment
from dotenv import load_dotenv
import os
load_dotenv()


#password hashing
   
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")  #hashing setup
def hash_pwd(pwd:str):                                             #function to hash password
    return pwd_context.hash(pwd)

def verify_pwd(plain:str,hashed:str):                             #function to verify hashed password with normal password
    return pwd_context.verify(plain,hashed)      #returns t/f

#token generation and verification


# SK=os.getenv("as010107")    #secret key=> used to sign the token
SK="as010107"
ALGO="HS256"
EXP=30            #expire in minutes

def create_token(data:dict):
    to_encode=data.copy()   #copy of original data
    expire=datetime.utcnow()+timedelta(minutes=EXP)     #abhi ka time+time diff abhi se
    to_encode["exp"]=expire    #expire token me add kro
    return jwt.encode(to_encode,SK,ALGO)

def verify_token(token:str):
    try:
        payload=jwt.decode(token,SK,ALGO)      #token kholo aur data nikalo
        return payload                 #dict
    except JWTError:                  #token galat ya expired
        return None
    


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(
        token:str=Depends(oauth2_scheme),   #request se token nikalo
        db:Session=Depends(get_session)
):
    payload=verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="invalid or expired token!")
    
    user_id=payload.get("user_id")
    doctor=db.query(models.Doctor)\
    .filter(models.Doctor.id==user_id)\
    .first()

    if not doctor:
        raise HTTPException(status_code=401,detail="doctor not found!")
    
    return doctor

#now we can protect routes by adding current_user=depends(get_current_user) in each endpoints
        
        




