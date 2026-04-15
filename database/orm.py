# database/orm.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Base 선언 (models.py에서 상속받을 용도)
class Base(DeclarativeBase):
    pass

# 2. engine 정의 (이 줄이 없으면 에러가 납니다!)
# SQLite를 사용할 경우 파일 경로를 지정합니다.
engine = create_engine("sqlite:///./local.db", echo=True)

# 3. SessionFactory 정의
SessionFactory = sessionmaker(bind=engine)