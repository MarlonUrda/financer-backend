from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    fname: str = Field(..., max_length=20, min_length=1, description="First name of the user")
    lname: str = Field(..., max_length=20, min_length=1, description="Last name of the user")
    phone: str = Field(..., max_length=15, min_length=1, description="Phone number of the user")
    email: str = Field(..., max_length=100, min_length=1, description="Email address of the user")
    password: str = Field(..., max_length=300, min_length=8, description="Password for user authentication")
    role_id: int = Field(..., description="Role ID of the user")

class UserRegister(UserAuth):
    pass

class UserLoginRequest(BaseModel):
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")
    password: str = Field(..., max_length=300, min_length=8, description="Password for user authentication")

class UserLoginResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the login was successful")
    message: str = Field(..., description="Response message")
    code: int = Field(..., description="Response code")
    token: str = Field(..., description="JWT access token")

class UserRegisterResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the registration was successful")
    message: str = Field(..., description="Response message")
    code: int = Field(..., description="Response code")

class UserRegisterRequest(UserAuth):
    pass

class SendRecoverEmail(BaseModel):
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

class SendRecoverEmailResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the email was sent successfully")
    message: str = Field(..., description="Response message")

class VerifyEmail(BaseModel):
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

class VerifyEmailResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the email verification was successful")
    message: str = Field(..., description="Response message")

class VerifyCode(BaseModel):
    code: str = Field(..., description="Verification code sent to the user's email")
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

class VerifyCodeResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the verification code is valid")
    message: str = Field(..., description="Response message")
    code: int = Field(..., description="Response code")

class NewPasswordRequest(BaseModel):
    new_password: str = Field(..., max_length=300, min_length=8, description="New password for user authentication")
    email: str = Field(..., max_length=100, min_length=5, description="Email address of the user")

class NewPasswordResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the password change was successful")
    message: str = Field(..., description="Response message")
    code: int = Field(..., description="Response code")
