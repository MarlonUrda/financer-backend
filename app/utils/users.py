from sqlalchemy import select
from models import User

async def get_user_by_id(db, user_id):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_email(db, email):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()