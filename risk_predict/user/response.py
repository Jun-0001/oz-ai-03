from datetime import datetime
from pydantic import BaseModel

# 회원가입 응답에 사용하는 데이터 구조
class UserResponse(BaseModel):
    id: int 
    email: str
    created_at: datetime