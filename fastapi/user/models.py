from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database.orm import Base

# Base = DeclarativeBase
class User(Base):
    # 표이름은 user
    __tablename__ = "user"
    
    # (32) -> 자릿수 지정
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        ) # id를 기본키 지정
    
    name: Mapped[str] = mapped_column(String(32))
    job: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now() # 레코드가 생성된 시각이 DB에 의해서 자동 저장
    )