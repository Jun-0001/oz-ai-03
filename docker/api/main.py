import uuid
import json

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from redis import asyncio as aredis


# # redis://redis -> redis 프로토콜 사용:// IP 주소
redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()

@app.post("/chats")
async def generate_chat_handler(
    user_input: str = Body(..., embed=True),
):
    
    # 2) Subscribe 채널 설정 (결과 받을 준비 중... 대기...)
    # 비동기 작업. redis한테 나 지금 pubsub했다 알려줌
    channel = str(uuid.uuid4())
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    # 3) Queue를 통해 Worker에 Task를 전달 (enqueue)
    # channel: 추론 결과 여기로 보내 / user_input: 요청 내용
    # 파이썬과 redis는 다른 형식임. redis는 문자열로만 처리
    # 데이터를 JSON으로 만들어야함
    task = {"channel": channel, "user_input": user_input}
    await redis_client.lpush("queue", json.dumps(task))

    # 4) 채널 메시지 읽고 토큰 반환
    # listen() -> 대기중... -> 언제 끊김? -> 강제로 끊어야함
    async def event_generator():
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            
            # DONE이라는 메시지 보내오면 강제로 멈춤
            token = message["data"]
            if token == "[DONE]":
                break
            yield token
        
        await pubsub.unsubscribe(channel)
        await pubsub.close()

    # 5) 추론 결과 수신
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )