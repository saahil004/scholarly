from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse
import bcrypt

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(data : UserRegister, db : Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(User).filter(User.email == data.email or User.phone == data.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already in use.")
    
    # encrypt password
    hashed_pwd = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")
    
    # create a user object
    new_user = User(full_name=data.full_name, email=data.email, password=hashed_pwd, phone=data.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user