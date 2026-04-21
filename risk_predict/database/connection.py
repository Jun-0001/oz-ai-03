from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# 비동기 방식으로 진행 + sqlite라는 별도의 데이터 베이스 사용 예정
DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite"

engine = create_async_engine(DATABASE_URL)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# 의존성 주입을 위한 제너레이터 함수 -> 세션 관리
async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()