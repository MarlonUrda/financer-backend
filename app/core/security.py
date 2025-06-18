import jwt
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION = os.getenv("JWT_EXPIRATION")

ph = PasswordHasher()

def generate_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": JWT_EXPIRATION})
    jwt_token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return jwt_token

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
def hash_pwd(password: str) -> str:
    hashed = ph.hash(password)
    return hashed

def verify_pwd(plain: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, plain)
        return True
    except Exception:
        return False