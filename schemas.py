from typing import Annotated,Literal,Optional
from pydantic import Field,BaseModel,computed_field

class Patient(BaseModel):
    id:Annotated[Optional[str],Field(...,description='enter id of patient',example='P7')]=None
    name:Annotated[Optional[str],Field(...,description='Enter name of the patient here',min_length=3,max_length=50)]=None
    age:Annotated[Optional[int],Field(...,description='Enter age of the patient',gt=0,le=100)]=None
    height:Annotated[Optional[float],Field(...,description='Enter height of patient in cm',gt=0)]=None
    weight:Annotated[Optional[float],Field(...,description='Enter weight of patient in kg',gt=0)]=None
    gender:Annotated[Optional[Literal['male','female','other']],Field(...,description='Enter gender of your patient')]=None
    
    @computed_field
    def bmi(model)->float:
        bmi=round((model.weight)/((model.height)/100)**2,2)
        return bmi
    
    @computed_field
    def verdict(model)->str:
        if model.bmi<18.5:
            return "underweight"
        elif model.bmi<30 and model.bmi>18.5:
            return "healthy"
        else:
            return "obese"

    class config:
        from_attributes=True #pydantic sirf dictionary smjhta h thats y pydantic ko sqlalchemy model smjhane k liye
        
