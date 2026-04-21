from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select

from auth.password import hash_password, verify_password
from database.connection import get_session
from user.request import SignUpRequest, LoginRequest
from user.models import User
from user.response import UserResponse

router = APIRouter(tags=["User"])


# 1) 데이터 입력 (이메일, 비밀번호)
@router.post(
    "/users",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)

# 2) 이메일 중복 검사? -> 기존 DB에 저장된 이메일 중 중복되는거 있는지 확인
async def signup_handler(
    body: SignUpRequest,
    session = Depends(get_session),
):
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()

    if user: # 중복
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "이미 가입된 이메일입니다."
        )
    
    # 3) 비밀번호 해싱? (암호화)
    password_hash = hash_password(plain_password=body.password)

    # 4) 회원 데이터 저장
    new_user = User(
        email=body.email,
        password_hash = password_hash
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) #id, created_at 새로고침
    
    # 5) 응답
    return new_user

@router.post(
    "/users/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)

# 1) 데이터 입력 (email, password)
async def login_handler(
    body: LoginRequest,
    session = Depends(get_session),
):
    # 2) email로 사용자 조회
    stmt = select(User).where(User.email == body.email) 
    result = await session.execute(stmt)
    user = result.scalar()

    # 사용자 없는경우, 
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록되지 않은 이메일입니다."
        )

    # 3) 사용자가 입력한 body.password <> 사용자.password_hash 검증
    verified = verify_password(
        plain_password=body.password,
        password_hash=user.password_hash
    )

    if not verified:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="등록되지 않은 비밀번호입니다."

        )

    # 4) JWT(JSON Web Token) 토큰 발급
    return