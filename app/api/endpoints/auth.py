from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()

@router.post("/login")
def login(db: Session = Depends(get_db)):
  return {"message": "User logged in successfully"}