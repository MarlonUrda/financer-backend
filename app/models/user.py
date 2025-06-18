from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from datetime import datetime, timezone

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  fname: Mapped[str] = mapped_column(String(100))
  lname: Mapped[str] = mapped_column(String(100))
  phone: Mapped[str] = mapped_column(String(15), unique=True)
  email: Mapped[str] = mapped_column(String(100), unique=True)
  password: Mapped[str] = mapped_column(String(300))
  created_at: Mapped[datetime] = mapped_column(
      default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
  )
  role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))