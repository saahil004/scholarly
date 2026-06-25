from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class MakeSubject(BaseModel):
    name : str
    description: str

class ReturnSubject(BaseModel):
    name : str
    description : str
    
    class Config:
        form_attributes = True
        
class SubjectUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None       