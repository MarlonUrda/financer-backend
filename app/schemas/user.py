from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    fname: str = Field(..., max_length=20, min_length=1, description="First name of the user")
    lname: str = Field(..., max_length=20, min_length=1, description="Last name of the user")
    phone: str = Field(..., max_length=15, min_length=1, description="Phone number of the user")
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

    class Config:
        from_attributes = True

class GetUserResponse(BaseModel):
    user: User = Field(..., description="User details")

    class Config:
        from_attributes = True

class GetAllUsersResponse(BaseModel):
    users: List[User] = Field(..., description="List of user details")

class UpdateUserRequest(BaseModel):
    fname: Optional[str] = Field(None, description="Changes the first name of the User")
    lname: Optional[str] = Field(None, description="Changes the last name of the User")
    phone: Optional[str] = Field(None, description="Changes the User phone number")

class UpdateUserResponse(BaseModel):
    success: bool
    code: int
    message: str
    id: int

class DeleteUserResponse(BaseModel):
    success: bool
    code: int
    message: str
    id: int