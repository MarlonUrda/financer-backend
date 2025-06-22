from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy import select, update, delete
from schemas import user

async def get_user_info(db: AsyncSession, user_id: int):
  stmt = select(User).where(User.id == user_id)
  res = await db.execute(stmt)

  return res.scalars().first()

async def get_all_users(db: AsyncSession):
  res = await db.execute(select(User))

  return res.scalars().all()

async def update_user(db: AsyncSession, user_id: int, data: user.UpdateUserRequest):
  user_data = data.model_dump(exclude_unset=True)

  stmt = update(User).where(User.id == user_id).values(**user_data)
  await db.execute(stmt)
  await db.commit()

async def delete_user(db: AsyncSession, user_id: int):
  stmt = delete(User).where(User.id == user_id)
  res = await db.execute(stmt)

  return res.scalars().first()
  