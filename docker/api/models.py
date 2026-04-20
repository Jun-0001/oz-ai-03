import uuid
import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Integer, ForeignKey, Text


class Base(DeclarativeBase):
    pass

# 1개의 Conversation랑 n개의 메시지랑 대응
class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default = uuid.uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(),
    )

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # 위에 id를 [str]로 매핑했기 때문에
    conversation_id : Mapped[str] = mapped_column(
        ForeignKey("conversation.id")
    )
    # 저장되는 글자수 제한
    role: Mapped[str] = mapped_column(String(10)) # user / assistant
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(),
    )