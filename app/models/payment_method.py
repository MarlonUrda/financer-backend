from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    method: Mapped[str] = mapped_column(String(100), unique=True)
