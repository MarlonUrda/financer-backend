from sqlalchemy import select
from sqlalchemy.orm import undefer
from models import User

async def get_user_by_id(db, user_id):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_email(db, email):
    stmt = select(User).where(User.email == email).options(undefer("*"))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()