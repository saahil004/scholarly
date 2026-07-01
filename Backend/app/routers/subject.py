from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.subject import Subject
from app.schemas.subject import ReturnSubject, MakeSubject, SubjectUpdate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.core.deps import get_admin_user, get_current_user
from app.models.user import User

router = APIRouter(prefix="/subject", tags=["subjects"])

@router.get('/all', response_model=list[ReturnSubject])
def getSubjects(db : Session = Depends(get_db)):
    all_subjects = db.query(Subject).all()
    return all_subjects

@router.post("/create", response_model=ReturnSubject)
def createSubject(data : MakeSubject, current_user : User = Depends(get_admin_user), db : Session = Depends(get_db)):
    if data.name == "" or data.name is None:
        raise HTTPException(status_code= 400, detail="Subject needs to have a name.")
    exist = db.query(Subject).filter(func.lower(data.name) == func.lower(Subject.name)).first()
    if exist:
        raise HTTPException(status_code= 409, detail="Subject already exists.")
    
    newSub = Subject(
        name=data.name,
        description=data.description
    )
    
    db.add(newSub)
    try:
      db.commit()
    except IntegrityError:
      db.rollback()
      raise HTTPException(status_code= 409, detail="Subject already exists.")
          
    db.refresh(newSub)
    
    return newSub

@router.put("/update/{subject_id}", response_model=ReturnSubject)
def updateSubject(subject_id : int, data : SubjectUpdate, current_user : User = Depends(get_admin_user), db : Session = Depends(get_db)):
    # if data.name is None or data.name == "":
        # raise HTTPException(status_code=400, detail="Name cant be NULL.")
    sub = db.query(Subject).filter(Subject.id == subject_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subject does not exist.")
    if data.name != None and data.name != "":
      exis = db.query(Subject).filter(func.lower(data.name) == func.lower(Subject.name), Subject.id != subject_id).first()
      if exis:
        raise HTTPException(status_code=409, detail="Subject already exists.")
      sub.name = data.name
    
    if data.description is not None:
        sub.description = data.description
    
    try:
      db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 409, detail="Subject already exists.")
    db.refresh(sub)
    return sub        

@router.delete("/delete/{subject_id}")
def deleteSubject(subject_id : int, current_user : User = Depends(get_admin_user), db : Session = Depends(get_db)):
    subtodel = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subtodel:
        raise HTTPException(status_code=404, detail="Subject does not exist.")
    
    message = "Subject deleted: " + subtodel.name
    
    db.delete(subtodel)
    db.commit()
    
    return {"message" : message}