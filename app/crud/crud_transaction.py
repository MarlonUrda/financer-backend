from sqlalchemy.ext.asyncio import AsyncSession
from models import Transaction
from sqlalchemy import select, update
from schemas import transaction 

async def get_all_transactions_from_db(db: AsyncSession):
  result = await db.execute(select(Transaction))
  return result.scalars().all()

async def get_user_transaction(db: AsyncSession, user_id: int):
  query = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
  return query.scalars().all()

async def get_single_transaction(db: AsyncSession, transaction_id: int):
  query = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
  return query.scalars().first()

async def insert_new_transaction(db: AsyncSession, transaction: transaction.NewTransactionRequest):
  new_transaction = Transaction(**transaction.model_dump())

  db.add(new_transaction)
  await db.commit()
  await db.refresh(new_transaction)

  return new_transaction

async def update_transaction(db: AsyncSession, transaction_id: int, data: transaction.UpdateTransactionRequest):

  update_data = data.model_dump(exclude_unset=True)

  stmt = update(Transaction).where(Transaction.id == transaction_id).values(**update_data)
  await db.execute(stmt)
  await db.commit()