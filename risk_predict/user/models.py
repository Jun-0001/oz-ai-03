from datetime import datetime
from database.orm import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import MappedColumn, mapped_column

class User(Base):
    __tablename__ = "user"

    id: MappedColumn[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: MappedColumn[str] = mapped_column(String(256), unique=True)
    password_hash: MappedColumn[str] = mapped_column(String(256))
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime, server_default=func.now()

    )
