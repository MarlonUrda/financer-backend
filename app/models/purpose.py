from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Purpose(Base):
    __tablename__ = "purpose"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)