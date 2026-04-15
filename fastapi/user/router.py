from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete
from database.connection import get_session
from database.connection_async import get_async_session
from user.models import User
from user.request import userCreateRequest, UserUpdateRequest
from user.response import UserResponse

# router.py API 기능 묶음 단위

# 핸들러 함수를 관리하는 객체
# prefix="/users" -> 공통 경로 고정 : /users
# tags = ["User"] -> 제목?
router = APIRouter(tags=["User"])


# [전체 사용자 목록 조회 API]
# GET /users
@router.get("/users", 
            summary="전체 사용자 목록 조회 API",
            status_code=status.HTTP_200_OK,
            response_model=list[UserResponse], # 클래스를 list 형태로 
            )
# 이 함수는 get_session에 의존적이네? 
# 저거 호출해봐야지 -> 반환값을 session에 전달
async def get_users_handler(
    # Depends: FastAPI에서 의존성(get_session)을 자동으로 실행/주입/정리
    session = Depends(get_async_session),
):
    # session = SessionFactory() 이거대신 아래 contextmanager 문법 활용
    # SQLAlchemy에 의존적이다. 
    # with SessionFactory() as session:
        # SELECT * FROM user 이거랑 같음 아래
        # stmt = statement 구문 (명령문)
        stmt = select(User) # db에 있는 모든 사용자 데이터가져옴 2개
        # sqalchemy가 result를 우리가 원하는 형태로 바꿔준다?
        result = await session.execute(stmt) # 여기서 대기 발생
        users = result.scalars().all() # [user1, user2...] 
        # scalars-> 객체로 불러옴
        # mapping-> dict
        # 객체로 바뀐 users 리스트 확인 가능
        return users

# [사용자 정보 검색 API]
# FastAPI는 위에서 아래로 해석되기 때문에 /users/{user_id} 아래 있으면 에러뜸
# GET / users / search?name=alex
# GET / users / search?job=student
# 고정 선언
# None -> 기본값
@router.get("/users/search",
            summary="사용자 정보 검색 API",
            response_model=list[UserResponse],
            ) # 데이터 중복 다수일경우, 고려해서 list로
async def search_user_handler( # id는 중복 X , name,job은 중복 가능
    name: str | None = Query(None), 
    job: str | None = Query(None),
    session = Depends(get_async_session),

):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다"
        )
    # 경우의 수 많아짐 -> 새로운 방식 필요.
    # A) name O / job X
    # B) name X / job O
    # C) name X / job X
    # D) name O / job O

    stmt = select(User) # 그냥 객체임. 실행 전

    # Chaining 기법. 꼬리 물기. if문은 분기를 만든다.
    # 하나의 통로. 여러개의 터널. if는 여기서 터널임 
    if name:
        stmt = stmt.where(User.name == name)
        # stmt = select(User).where(User.name == name)
    
    if job:
        stmt = stmt.where(User.job == job)

        # 1) name을 거쳐온 경우
        # stmt = select(User).where(User.name == name).where(User.job == job)

        # 2) name을 거치지 않은 경우
        # stmt = select(User).where(User.job == job)
    
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users


    # if name is None and job is None:
    #     return {"msg": "조회에 사용할 QueryParam이 필요합니다."}

    # for user in users:
    #     # 1. 이름과 직업이 둘 다 들어왔을 때 (AND 조건)
    #     if name and job:
    #         if user["name"] == name and user["job"] == job:
    #             return user
    #     # 2. 둘 중 하나만 들어왔을 때 (OR 조건)
    #     else:
    #         if user["name"] == name or user["job"] == job:
    #             return user
    
    # # 💡 루프를 다 돌았는데도 여기까지 왔다면 "못 찾았다"는 뜻입니다.
    # return {"msg": "해당 조건의 유저를 찾을 수 없습니다."}


# [단일 사용자 데이터 조회 API]
# GET / users/{user_id} -> 1번 사용자 데이터 조회
# 데코레이터
# 함수. 함수 인자에 데코레이터의 {user_id}가 들어가아햠
# user_id는 반드시 숫자. path parameter라고 부름
# 동적 선언
@router.get("/users/{user_id}",
            summary="단일 사용자 데이터 조회 API",
            response_model=UserResponse,
            )
async def get_user_handler(
    # greater than or equal to 
    # 매개변수에 Path 저장
    # user_id가 1이상인지 확인하는 작업
    user_id: int = Path(..., ge=1),
    session = Depends(get_async_session),
):
    # for문 대신 with as로 변경
    # SELECT * FROM user Where id = 10; -> 존재 하지 않는 경우 0개
    stmt = select(User).where(User.id == user_id) # 존재하는 경우 1개만 가져옴
    result = await session.execute(stmt)

    # scalar() -> 첫번째 열의 첫번째 데이터만 가져옴
    # all() -> 리스트를 변환한다
    user = result.scalar() # 존재하면 user 객체 반환, 존재하지 않으면 None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    return user
        
# [회원추가 API]
# POST / users
@router.post(
        "/users", 
        status_code=status.HTTP_201_CREATED,
        summary="회원추가 API",
        response_model=UserResponse
)

async def create_user_handler(
    #1) 사용자 데이터를 넘겨 받는다 + 데이터 유효성 검사(전처리 같은거)
    body: userCreateRequest, # 어 얘는 조금 다르네? Pydantic이구나 찾아보자!
    # 찾아 보니 name이랑 job을 받는구나
    session = Depends(get_async_session)

):
    # with문. context manager을 벗어나는 순간 자동으로 close() 호출
    # 새로운 유저 데이터를 DB 표 선언
    new_user = User(name=body.name, job=body.job)
    # 새로운 유저 데이터 DB 표에 추가
    session.add(new_user)
    # 변경 사항 저장
    print(new_user.id, new_user.created_at) # None
    await session.commit() # 이 때 db에 저장해달라는 요청 보내는거 
    # id, created_at 읽어옴 -> 동기화(DB->FastAPI)
    await session.refresh(new_user) # new_user 새롭게 갱신해야함 
    print(new_user.id, new_user.created_at) # 3
    return new_user
     

# [회원 정보 수정 API]
# PUT: 전체 교체 (replace)
# PATCH: 일부 수정 (partial update) -> 이걸로 해라. 
# PATCH: /users/{user_id}
@router.patch("/users/{user_id}",
              summary="회원 정보 수정 API",
              response_model=UserResponse,
)
async def update_user_handler(
    # 1) 입력값 정의(클라이언트가 수정한 내용을 의미)
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_async_session),

):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    # 예외처리: user가 없는경우
    if not user:
            raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )
    
    user.job = body.job 
    # add() 안해도 되는 이유는 이미 user -> result -> session로 어떤 걸 수정할지 알기에
    await session.commit() # 현재 user 상태 (job 변경사항)를 DB에 반영
    return user


# [회원 삭제 API]
# DELETE / users/{user_id}
@router.delete("/users/{user_id}",
               summary= "회원 삭제 API",
               status_code=status.HTTP_204_NO_CONTENT,)
                #204 때문에 return 뭘 넣어도 응답 메시지는 반환 안됨 
                # code 바꾸면 return에 응답 추가가능

async def delete_user_handler(
     user_id: int,
     session = Depends(get_async_session),
):
    # with SessionFactory() as session:
    # # 1) get + delete (조회하고 삭제)
    # # user 정보 가져오고 delete
    #     stmt = select(User).where(User.id == user_id)
    #     result = session.execute(stmt)
    #     user = result.scalar()


    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User Not Found",
    #         )

    #     session.delete(user) # 삭제
    #     # session.expunge(user) 관심 끄라고
    #     session.commit() # 수정 사항 반영

    # 2) delete (곧바로 삭제하는 방식)
    # 아예 그냥 delete
    stmt = delete(User).where(User.id == user_id) 
    await session.execute(stmt) # 삭제 
    await session.commit() # 확정

    # 이건 1번 방법 아니면 따로 user를 정의할 수 없는건가...
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User Not Found",
    # )
