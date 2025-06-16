from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()

@router.get("/get")
def get_transaction(db: Session = Depends(get_db)):
  return {"message": "Transaction retrieved successfully"}