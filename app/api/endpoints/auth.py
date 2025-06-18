from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.security import hash_pwd, generate_token, verify_pwd, decode_token
from db import get_db
import schemas.auth as auth
from models.user import User

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

@router.post("/send")
async def sendEmail():
   return { "message": "Send Email fetched" }