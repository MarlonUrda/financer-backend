from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    fname: str = Field(..., max_length=20, min_length=1, description="First name of the user")
    lname: str = Field(..., max_length=20, min_length=1, description="Last name of the user")
    phone: str = Field(..., max_length=15, min_length=1, description="Phone number of the user")
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

class GetUserResponse(BaseModel):
    user: User = Field(..., description="User details")

class GetAllUsersResponse(BaseModel):
    users: list[User] = Field(..., description="List of user details")
