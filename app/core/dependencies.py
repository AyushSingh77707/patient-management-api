#creating get_current_user
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.doctor import Doctor
from app.core.security import verify_token


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(
        token:str=Depends(oauth2_scheme),   #request se token nikalo
        db:Session=Depends(get_session)
):
    payload=verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="invalid or expired token!")
    
    user_id=payload.get("user_id")
    doctor=db.query(Doctor)\
    .filter(Doctor.id==user_id)\
    .first()

    if not doctor:
        raise HTTPException(status_code=401,detail="doctor not found!")
    
    return doctor

#now we can protect routes by adding current_user=depends(get_current_user) in each endpoints