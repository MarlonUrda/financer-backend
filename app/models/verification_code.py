from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, TIMESTAMP, Integer
import datetime

class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1)