from typing import Annotated,Literal,Optional
from pydantic import Field,BaseModel,EmailStr

class DoctorRegister(BaseModel):
    name:Annotated[str,Field(min_length=3)]
    email:EmailStr
    password:str

class DoctorLogin(BaseModel):
    email:EmailStr
    password:str

    class config:
        from_attributes=True

