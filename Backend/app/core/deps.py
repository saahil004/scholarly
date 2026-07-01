from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import verify_token

auth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : str = Depends(auth_scheme), db : Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
    userid = payload['sub']
    user = db.query(User).filter(int(userid) == User.id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user

# def get_admin_user(token : str = Depends(auth_scheme), db : Session = Depends(get_db)):
#         payload = verify_token(token)
#         if payload is None:
#             raise HTTPException(status_code=404, detail="Invalid or expired token.")
        
#         userid = payload['sub']
#         user = db.query(User).filter(int(userid) == User.id).first()
        
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found.")
#         if user.is_admin == False:
#             raise HTTPException(status_code=401, detail="User not an admin.")
            
        
#         return user

def get_admin_user(current_user : User = Depends(get_current_user)):
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="User not an admin.")
    
    return current_user