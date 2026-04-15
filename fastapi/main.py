import anyio
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI
from user.router import router 
# 라우터에서 가져옴


# 쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield


# 객체 생성 
# FastAPI: 프레임워크가 제공하는 **클래스(설계도)**
# app은 그 설계도로 만든 **집(실체)**
# main.py를 보면 대충 뭐하는 코드인지 전체를 알 수 있음
app = FastAPI(lifespan=lifespan)
app.include_router(router)

def aws_sync():
    # AWS 서버랑 통신 (예: 2초)
    return

from starlette.concurrency import run_in_threadpool

# 비동기 라이브러리를 지원하지 않은 경우
@app.get("/async")
async def async_handler():
    # 동기 함수를 비동기 방식으로 실행할 수 있게 해주는 유틸리티 함수
    await run_in_threadpool(aws_sync)
    return {"msg":"ok"}

# 동기함수인데 비동기로 처리됨
# @app.get("/sync")
# def sync_handler():
#     import time
#     time.sleep(5)
#     return {"msg": "ok"}

# # 비동기함수 -> 파국. 비동기로 명명했는데 동기씀
# @app.get("/sync")
# async def sync_handler():
#     import time
#     time.sleep(5)
#     return {"msg": "ok"}

