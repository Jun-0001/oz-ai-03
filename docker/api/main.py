from fastapi import FastAPI
from sqlalchemy import text
from connection import SessionFactory

app = FastAPI()

@app.get("/health-check")
def health_check_handler():
    with SessionFactory() as session:
        stmt = text("SELECT * FROM user LIMIT 1;")
        result = session.execute(stmt)
        row = result.fetchone()
    
    # 데이터가 없을 때를 대비한 예외 처리
    if row is None:
        return {"user": "None"}

    # row._mapping
    return {"result": dict(row._mapping)}