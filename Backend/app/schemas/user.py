from pydantic import BaseModel, EmailStr, field_validator

class UserRegister(BaseModel):
    full_name : str
    email : EmailStr
    password : str
    phone : str
    
    @field_validator("phone")
    def validate_phone(cls, p):
        if not p.startswith("03") or len(p) != 11 or not p.isdigit():
            raise ValueError("Phone must be in Pakistani format")
        return p
    
class UserResponse(BaseModel):
    id : int
    full_name : str
    email : str
    phone : str
    is_admin : bool
        
    class Config:
        from_attributes = True    