from pydantic import BaseModel, Field
from typing import List, Optional

class Transaction(BaseModel):
  id: int
  amount: float
  description: Optional[str] = None
  date: str
  user_id: int
  type_id: int
  purpose_id: int
  coin_id: int 
  method_id: int

  class Config:
    from_attributes = True

class NewTransactionRequest(BaseModel):
  description: str = Field(..., max_length=200, description="Deatiled info about the transaction.")
  amount: int = Field(..., description="The amount of the treansaction.")
  date: str = Field(..., description="When the user made the transaction.")
  created_at: str = Field(..., description="Indicates the moment when the transaction was made.")
  user_id: int = Field(..., description="User Identifier.")
  type_id: int = Field(..., description="Stablish the type of the transaction.")
  purpose_id: int = Field(..., description="Stablish the purpose of the transaction.")
  coin_id: int = Field(..., description="Coin denomination identifier.")
  method_id: int = Field(..., description="Indicates how the transaction was done.")

class NewTransactionResponse(BaseModel):
  success: bool = Field(..., description="State that tells you if the request was successfull.")
  code: int = Field(..., description="Code of the request response"),
  message: str = Field(..., description="More info about the response.")
  transaction_id: int = Field(..., description="Identifier of the new Transaction")

class GetTransactions(BaseModel):
  success: bool = Field(..., description="State that tells you if the request was successfull.")
  code: int = Field(..., description="Code of the request response"),
  message: str = Field(..., description="More info about the response.")
  transactions: List[Transaction] = Field(..., description="List of transactions returned in the response.")

class GetSingleTransaction(BaseModel):
  success: bool = Field(..., description="State that tells you if the request was successfull.")
  code: int = Field(..., description="Code of the request response"),
  message: str = Field(..., description="More info about the response.")
  transactions: Transaction = Field(..., description="Transaction returned in the response.")

class UpdateTransactionRequest(BaseModel):
  description: Optional[str] = Field(..., max_length=200, description="Deatiled info about the transaction.")
  amount: Optional[int] = Field(..., description="The amount of the treansaction.")
  date: Optional[str] = Field(..., description="When the user made the transaction.")
  updated_at: Optional[str] = Field(..., description="Indicates the moment when the transaction was made.")
  user_id: Optional[int] = Field(..., description="User Identifier.")
  type_id: Optional[int] = Field(..., description="Stablish the type of the transaction.")
  purpose_id: Optional[int] = Field(..., description="Stablish the purpose of the transaction.")
  coin_id: Optional[int] = Field(..., description="Coin denomination identifier.")
  method_id: Optional[int] = Field(..., description="Indicates how the transaction was done.")

class UpdateTransactionResponse(NewTransactionResponse):
  pass

class DeleteTransactionResponse(NewTransactionResponse):
  pass