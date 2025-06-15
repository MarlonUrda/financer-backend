from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, String, Text, ForeignKey
from typing import Optional
from datetime import datetime, timezone

class PaymentType(Base):
    __tablename__ = "payment_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(100), unique=True)
