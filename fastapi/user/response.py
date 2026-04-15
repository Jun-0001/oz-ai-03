# 응답 데이터의 형식 관리
# 1) 클라이언트에게 잘못된 데이터를 넘기지 않기 위해
# 2) 보내면 안되는 데이터 (개인 정보)를 실수로 유출하지 않기 위해
from pydantic import BaseModel, Field
from datetime import datetime
# Response에 정의한것만 반환
# 선별적 반환 가능
class UserResponse(BaseModel):
    id: int
    name: str
    job: str
    created_at: datetime