# 요청 본문의 데이터 형식을 관리하는 파일
from pydantic import BaseModel, Field

# 사용자를 추가할 때, 클라이언트가 서버로 보내는데이터 형식
class userCreateRequest(BaseModel):
    # id: int -> 자동 생성이라 굳이 설정할 필요 없음
    name: str = Field(..., min_length=2, max_length=10)
    job: str 

# 타입 힌트 형식으로 표현 가능
# 클래스 -> 설계도이자 요구조건. 요구 조건을 타입으로 지정한거임

# 사용자 데이터(일단 여기서는 직업만)를 수정할 때, 데이터 형식
class UserUpdateRequest(BaseModel):
    job: str
