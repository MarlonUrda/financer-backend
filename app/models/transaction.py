from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, String, Text, ForeignKey
from typing import Optional
from datetime import datetime, timezone

class Transaction(Base):
  __tablename__ = "transactions"

  id: Mapped[int] = mapped_column(primary_key=True)
  description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
  created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  type_id: Mapped[int] = mapped_column(ForeignKey("payment_types.id"))
  purpose_id: Mapped[int] = mapped_column(ForeignKey("purpose.id"))
  coin_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
  method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"))