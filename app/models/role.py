from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, String, Text, ForeignKey
from typing import Optional
from datetime import datetime, timezone

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_desc: Mapped[str] = mapped_column(String(100), unique=True)
