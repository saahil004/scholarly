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
     
class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"
    
    # class Config: we dont need its not an SQLAlchemy object
    
class VerifyOTP(BaseModel):
    email: EmailStr
    otpcode : str   
    
class ResendOTP(BaseModel):
    email : EmailStr     
              