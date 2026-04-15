# SQLAlchemy를 이용해서 DB와 연결하는 코드
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 데이터 베이스 접속 정보
# 외부에서 가져옴. 내가 어떤 DB 엔진을 쓰냐에 따라 URL 바뀜
DATABASE_URL = "sqlite:///./local.db"
# /./local.db -> 파일 형태로 현재 경로에 만들어라

# Engine: DB와 접속을 관리하는 객체. 엔진은 MySQL, SQLite 등
# echo=True -> 출력시 실제 발생되는 쿼리 다 출력해라
# SQLAlchemy가 내부적으로 생성하여 데이터베이스에 보내는 모든 SQL 쿼리문을 터미널(콘솔)에 실시간으로 출력해 주는 '로깅(Logging)' 기능입니다.
engine = create_engine(DATABASE_URL, echo=True)

# Session: 한 번의 DB 요청-응답 단위
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지를 조정하는 옵션
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,

)

# SQLAlchemy 세션을 관리하는 함수
def get_session():
    session = SessionFactory()
    
    # 일시 정지? 반환은 하는데 종료는 안함. 제너레이터?
    try:
        yield session 
    finally:
        session.close()

