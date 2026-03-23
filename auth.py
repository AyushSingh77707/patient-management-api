'''auth.py me 4 kam honge
1.password hashing
2.password verify
3.token generate
4.token verification'''

#password hashing
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")    #hashing setup

def hash_pwd(pwd:str):                                             #function to hash password
    return pwd_context.hash(pwd)

def verify_pwd(plain:str,hashed:str):                             #function to verify hashed password with normal password
    return pwd_context.verify(plain,hashed)      #returns t/f

#token generation and verification
from datetime import datetime,timedelta
from jose import jwt,JWTError

SK="as010107"    #secret key=> used to sign the token
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

        
        




