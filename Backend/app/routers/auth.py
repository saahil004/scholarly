from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.otp import OTP
from app.schemas.user import UserRegister, UserResponse, UserLogin, TokenResponse, VerifyOTP, ResendOTP
import bcrypt
from app.core.security import create_access_token, verify_token
from sqlalchemy import or_
from app.core.otp_utils import generate_otp
from app.core.email import send_otp_email
from datetime import datetime, timedelta, timezone

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
    
    # opt generation
    otpcode = generate_otp()
    otp = OTP(
        user_id=new_user.id,
        code=otpcode,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(otp)
    db.commit()
    
    try:
        send_otp_email(new_user.email, otpcode)
    except Exception as e:
        # rollback everything if email fails
        db.delete(otp)
        db.delete(new_user)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")
    
    return new_user

@router.post("/verifyotp")
def verifyOTP(data : VerifyOTP, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email not found.")
    
    otp = db.query(OTP).filter(user.id == OTP.user_id, OTP.code == data.otpcode).first()
    if not otp:
        raise HTTPException(status_code=400, detail='No OTP found.')
    if otp.expires_at < datetime.now(timezone.utc):
        db.delete(otp)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired. Deleting OTP...")

    user.is_verified = True
    db.delete(otp)
    db.commit()   
    return {"message" : "OTP verified"} 

@router.post("/resendotp")
def resendOTP(data : ResendOTP, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found.")
    
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email is already verified.")
    
    prevotp = db.query(OTP).filter(user.id == OTP.user_id).first()
    
    newotp = OTP(
        code=generate_otp(),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )    
    
    if prevotp:
        db.delete(prevotp)
        db.commit()
    
    db.add(newotp)
    db.commit()
    try:
        send_otp_email(user.email, newotp.code)
        # db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))            
    
    return {"message" : "OTP resent."} 

@router.post("/login", response_model=TokenResponse)
def login(data : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered.")
    
    if user.is_verified == False:
        raise HTTPException(status_code=400, detail="Email not verified.")
    
    pw = bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8"))
    if not pw:
        raise HTTPException(status_code=401, detail="Password incorrect.")
    token = create_access_token({"sub" : str(user.id), "is_admin" : user.is_admin}) # sub should always be a string
    return TokenResponse(access_token=token)