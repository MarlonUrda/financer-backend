from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.security import hash_pwd, generate_token, verify_pwd, decode_token
from db import get_db
import schemas.auth as auth
from models.user import User
from utils import get_user_by_email, generate_unique_code, verify_code, deactivate_expired_codes
from services.mailer import send_email

router = APIRouter()

@router.post("/register", response_model=auth.UserRegisterResponse)
async def register(request: auth.UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == request.email)
    user_result = await db.execute(stmt)
    user = user_result.scalar_one_or_none()
    if user:
       raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail="Email already registered"
       )
    
    new_user = User(
       fname=request.fname,
       lname=request.lname,
       phone=request.phone,
       email=request.email,
       password=hash_pwd(request.password),
       role_id=request.role_id
    )

    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError as er: 
        await db.rollback()
        print(er)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo registrar el usuario. El correo electrónico o teléfono ya podría existir.",
        )
    except Exception as e:
        await db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al registrar el usuario.",
        )
    return auth.UserRegisterResponse(success=True, message="User registered successfully", code=201)

@router.post("/login", response_model=auth.UserLoginResponse)
async def login(request: auth.UserLoginRequest, db: AsyncSession = Depends(get_db)):
  stmt = select(User).where(User.email == request.email)
  result = await db.execute(stmt)
  user = result.scalar_one_or_none()
  if not user or not verify_pwd(request.password, user.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
  token = generate_token(user.id)
  return auth.UserLoginResponse(success=True, message="User logged in successfully", code=200, token=token)

@router.post("/send", response_model=auth.SendRecoverEmailResponse)
async def sendEmail(request: auth.SendRecoverEmail, db: AsyncSession = Depends(get_db)):

   await deactivate_expired_codes(db)

   user = await get_user_by_email(db, request.email)
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

   user_email = user.email
   user_id = user.id

   code = await generate_unique_code(db, user_id)

   mail = send_email(
      subject="Recover your Password",
      body=f"Please use the following code to recover your password: {code}",
      to_email=user_email,
   )
   if not mail:
       return auth.SendRecoverEmailResponse(success=False, message="Error sending email", code=500)
       
   return auth.SendRecoverEmailResponse(success=True, message="Recovery email sent", code=200)

@router.post("/verify", response_model=auth.VerifyCodeResponse)
async def verify(request: auth.VerifyCode, db: AsyncSession = Depends(get_db)):
   user = await get_user_by_email(db, request.email)
   if not user:
      return auth.VerifyCodeResponse(success=False, message="User not found", code=404)

   is_valid = await verify_code(db=db, user_id=user.id, code=request.code)

   if not is_valid:
      return auth.VerifyCodeResponse(success=False, message="Invalid or expired verification code", code=400)

   return auth.VerifyCodeResponse(success=True, message="Verification code is valid", code=200)

@router.post("/change-password", response_model=auth.NewPasswordResponse)
async def change_password(request: auth.NewPasswordRequest, db: AsyncSession = Depends(get_db)):
   user = await get_user_by_email(db, request.email)
   if not user:
      return auth.NewPasswordResponse(success=False, message="User not found", code=404)

   user.password = hash_pwd(request.new_password)
   db.add(user)
   await db.commit()
   return auth.NewPasswordResponse(success=True, message="Password changed successfully", code=200)
