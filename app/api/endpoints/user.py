from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas import user
from crud import crud_users

router = APIRouter()

@router.get("/get", response_model=user.GetAllUsersResponse)
async def get_users(db: AsyncSession = Depends(get_db)):
  try:
    all_users = await crud_users.get_all_users(db=db)
    if not all_users:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        details = "Users not found on db."
      )
    
  except:
    raise HTTPException (
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong."
    )
  
  return user.GetAllUsersResponse(users=all_users)

@router.get("/get/{user_id}", response_model=user.GetUserResponse)
async def get_single_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
  try:
    my_user = await crud_users.get_user_info(db=db, user_id=user_id)
    if not my_user:
      return user.GetUserResponse(user=None)
  except:
    raise HTTPException (
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong in the server."
    )
  
  return user.GetUserResponse(user=my_user)
  
@router.put("/update/{user_id}", response_model=user.UpdateUserResponse)
async def update(request: user.UpdateUserRequest, user_id: int, db: AsyncSession = Depends(get_db)):
  try:
    updated_user = await crud_users.update_user(db=db, user_id=user_id, data=request)
    if len(updated_user) == 0 or not updated_user:
      return user.UpdateUserResponse(success=False, code=304, message="Error updating your user.", id=None)
  except:
    raise HTTPException (
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Something went wrong."
    )
  
  return user.UpdateUserResponse(success=True, code=200, message="User updated successfully!", id=updated_user.id)

@router.delete("/delete/{user_id}", response_model=user.DeleteUserResponse)
async def delete_the_user(user_id: int, db: AsyncSession = Depends(get_db)):
  try:
    res = await crud_users.delete_user(db=db, user_id=user_id)
    if not res:
      return user.DeleteUserResponse(success=False, code=400, message="We cant do that right now.", id=None)
  except:
    raise HTTPException (
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Somthing went wrong."
    )
  
  return user.DeleteUserResponse(success=True, code=200, message="User deleted succesfully!", id=res.id)