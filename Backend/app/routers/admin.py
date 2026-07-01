from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.deps import get_admin_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/admin", tags=["admins"])

@router.put("/assign-admin", response_model=UserResponse)
def assign_admin(user_id : int, current_admin : User = Depends(get_admin_user), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    
    if user.is_admin == True:
        raise HTTPException(status_code=409, detail="This user is already an admin.")
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user