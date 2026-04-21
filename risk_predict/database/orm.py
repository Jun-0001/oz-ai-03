from database.connection import engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        # 동기 함수를 비동기 함수로 변환
        await conn.run_sync(Base.metadata.create_all)