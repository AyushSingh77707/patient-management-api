'''auth.py me 4 kam honge
1.password hashing
2.password verify
3.token generate
4.token verification'''

from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from app.core.config import settings


#password hashing
   
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")  #hashing setup
def hash_pwd(pwd:str):                                             #function to hash password
    return pwd_context.hash(pwd)

def verify_pwd(plain:str,hashed:str):                             #function to verify hashed password with normal password
    return pwd_context.verify(plain,hashed)      #returns t/f

#token generation and verification

def create_token(data:dict):
    to_encode=data.copy()   #copy of original data
    expire=datetime.now(timezone.utc)+timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTE)     #abhi ka time+time diff abhi se
    to_encode["exp"]=expire    #expire token me add kro
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)

def verify_token(token:str):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)      #token kholo aur data nikalo
        return payload                 #dict
    except JWTError as e:                  #token galat ya expired
        raise HTTPException(status_code=401,detail="invalid or expired token!")
    



        
        




