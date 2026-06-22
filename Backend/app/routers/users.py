from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
# from app.schemas.user import UserRegister, UserResponse
from app.schemas.userlist import UserListResponse

router = APIRouter(prefix="/users", tags=["All users"])

@router.get("/all", response_model=list[UserListResponse])
def getAllUsers(db : Session = Depends(get_db)):
    all_users = db.query(User).filter(User.is_admin == False).all()
    
    # db.refresh(all_users) no need here
    return all_users