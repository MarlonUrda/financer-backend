from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from crud import crud_transaction
from schemas import transaction

router = APIRouter()

@router.get("/get/{user_id}", response_model=transaction.GetTransactions)
async def get_transaction(user_id: int, db: AsyncSession = Depends(get_db)):
  try:
    result = await crud_transaction.get_user_transaction(db=db, user_id=user_id)
    if not result:
      return transaction.GetTransactions(success=True, code=200, message="The user doesn't have transactions registered", transactions=[])
  except:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong in the server.")
  return transaction.GetTransactions(success=True, code=200, message="Transactions collectred!", transactions=result)

@router.post("/new", response_model=transaction.NewTransactionResponse)
async def create_transaction(request: transaction.NewTransactionRequest, db: AsyncSession = Depends(get_db)):
  try:
    new_tr = await crud_transaction.insert_new_transaction(db=db, transaction=request)
    if not new_tr:
      return transaction.NewTransactionResponse(success=False, code=400, message="Error creating transaction")
  except:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong with the server."
    )
  
  return transaction.NewTransactionResponse(success=True, code=201, message="Transaction created!")

@router.get("/single/{transaction_id}", response_model=transaction.GetSingleTransaction)
async def get_my_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
  try:
    res = await crud_transaction.get_single_transaction(db=db, transaction_id=transaction_id)
    if not res:
      return transaction.GetSingleTransaction(success=False, code=404, message="Transaction not found in db!", transactions=None)  
  except:
    raise HTTPException (
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong inside of the server."
    )
  
  return transaction.GetSingleTransaction(success=True, code=200, message="Transaction retrieved succesfully", transactions=res)

@router.post("/update/{transaction_id}", response_model=transaction.UpdateTransactionResponse)
async def update_an_transaction(id:int, data: transaction.UpdateTransactionRequest, db: AsyncSession = Depends(get_db)):
  try:
    res = await crud_transaction.update_transaction(db=db, transaction_id=id, data=data)
    if not res:
      return transaction.UpdateTransactionResponse(success=False, code=400, message="Error updating transaction")
  except:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong."
    )
  
  return transaction.UpdateTransactionResponse(success=True, code=300, message="Transaction updated succesfully!", transaction_id=res.id)