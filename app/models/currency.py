from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(10), unique=True)