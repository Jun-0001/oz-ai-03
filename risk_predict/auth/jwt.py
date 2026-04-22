# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzY4MzU2MDEsInN1YiI6MSwiaGVsbG8iOiJ3b3JsZCJ9.3xeOsizsCEaiIj1TBatxfJQayjdmi6Bzy98vWCEcEL8'
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from config import settings
# openssl rand -hex 16 -> 16글자 짜리 랜덤 숫자 생성


# access_token 발급
def create_access_token(user_id: int) -> str:
    payload = {
        # 사용자 id
        "sub": str(user_id),
        # 만료기간 설정
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    # 어떤 데이터를 코드화(토큰화)
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm="HS256"
    )

# access_token의 위변조 여부 확인 및 payload를 읽는 함수
def verify_access_token(access_token: str):
    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET, algorithms=["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "잘못된 토큰 형식입니다.",

        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료된 토큰입니다.",
        )

    return payload

def verify_user(
        # 자동으로 API가 Swagger UI(문서)에 'Authorize' 버튼을 만들고, 
        # 모든 요청 헤더에 인증 칸을 생성
        auth_header=Depends(HTTPBearer())
):
    access_token = auth_header.credentials
    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="sub값이 없습니다."
        )
    return user_id