from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import engine
from sqlalchemy import text
from app.routers import auth
from app.routers import users
from app.routers import subject
from app.routers import admin

load_dotenv()

app = FastAPI(
    title="Scholarly Academia API",
    description="Backend for Scholarly",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Scholarly Academia backend running"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subject.router)
app.include_router(admin.router)

@app.get("/testDB")
def test():
       try: 
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "Database connected"}
       except Exception as e:
           return {"Error" : str(e)} 