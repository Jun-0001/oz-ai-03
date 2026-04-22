from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.security import HTTPBearer
from sqlalchemy import select

from auth.password import hash_password, verify_password
from database.connection import get_session
from user.request import SignUpRequest, LoginRequest, HealthProfileRequest
from user.models import User, HealthProfile
from user.response import UserResponse
from auth.jwt import create_access_token, verify_user

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
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token}

@router.post(
    "/health-profiles",
    summary="건강 프로필 생성 API",
    status_code=status.HTTP_201_CREATED,
)

# 1) 건강 데이터 입력
# 가장 먼저 request에 형식 지정해야함
async def create_health_profile_handler(
    # 클라이언트가 보낸 Authorization Header를 읽어줌
    user_id = Depends(verify_user),
    body: HealthProfileRequest = Body(...),
    session = Depends(get_session), # 중복 확인은 db에서 해야하니 이거 추가.
):
    
    # 토큰 검증
    # 토큰 형식 검사 / 만료 시간 체크 / 서명키(secret) 확인
    # 토큰 검증 끝났으니 payload안 user_id를 믿고 사용

    # 2) 건강 프로필 중복 검사
    stmt = (
        select(HealthProfile)
        .where(HealthProfile.user_id == user_id)
    )
    result = await session.execute(stmt)
    existing_profile = result.scalar()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "이미 건강 프로필이 존재합니다.",
        ) 

    # 3) 건강 프로필 생성 & 저장
    # dump()로 한번에 dict 형태로 끄낼 수 있음
    profile_data: dict = body.model_dump()
    new_profile = HealthProfile(
        user_id=user_id, **profile_data
    )
    # **profile_data 안 쓰면 아래처럼 다 써야함
    # user_id = user_id
    ## ...
    # 생성된 new_profile db에 추가
    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)

    return new_profile
    
    
    
    # 4) 응답 

    return payload