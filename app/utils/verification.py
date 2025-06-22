from datetime import datetime, timezone, timedelta
from sqlalchemy import update, select
from models import VerificationCode
import secrets

async def deactivate_expired_codes(db) -> bool:
    now = datetime.utcnow() #Hasta encontrar una alternativa viable
    stmt = (
        update(VerificationCode)
        .where(VerificationCode.expires_at < now)
        .where(VerificationCode.is_active == 1)
        .values(is_active=0)
    )
    await db.execute(stmt)
    await db.commit()
    return True

async def generate_unique_code(db, user_id, max_attempts=10) -> str:
    for _ in range(max_attempts):
        code = str(secrets.randbelow(900000) + 100000).zfill(6)
        stmt = (
            select(VerificationCode)
            .where(VerificationCode.code == code)
            .where(VerificationCode.user_id == user_id)
        )
        result = await db.execute(stmt)
        if not result.scalars().first():
            expires_at = datetime.utcnow() + timedelta(minutes=5)
            new_code = VerificationCode(code=code, user_id=user_id, expires_at=expires_at, is_active=1)
            db.add(new_code)
            await db.commit()
            return code
    raise Exception("No se pudo generar un código único después de varios intentos.")

async def verify_code(db, user_id, code) -> bool:
    stmt = (
        select(VerificationCode)
        .where(VerificationCode.user_id == user_id)
        .where(VerificationCode.code == code)
        .where(VerificationCode.is_active == 1)
    )
    result = await db.execute(stmt)
    verification_code = result.scalars().first()
    if not verification_code:
        return False
    if verification_code.expires_at < datetime.utcnow():
        return False
    return True