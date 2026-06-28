from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse, UserLogin, TokenResponse
import bcrypt
from app.core.security import create_access_token, verify_token
from sqlalchemy import or_

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(data : UserRegister, db : Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(User).filter(or_(User.email == data.email, User.phone == data.phone)).first()
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

@router.post("/login", response_model=TokenResponse)
def login(data : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email not reigstered.")
    
    pw = bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8"))
    if not pw:
        raise HTTPException(status_code=401, detail="Password incorrect.")
    token = create_access_token({"sub" : str(user.id), "is_admin" : user.is_admin}) # sub should always be a string
    return TokenResponse(access_token=token)