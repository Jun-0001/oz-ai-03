import asyncio
from contextlib import asynccontextmanager
from openai import OpenAI
from llama_cpp import Llama
from fastapi import FastAPI, Body, Request, Depends
from fastapi.responses import StreamingResponse

from config import settings
from schema import OpenAIResponse
SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 모델 경로와 설정을 app.state에 저장
    app.state.llm = Llama(
        model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=4, # M1 성능을 위해 스레드 수를 조금 높였습니다.
        verbose=False,
        chat_format="llama-3",
    )   
    app.state.openai_client = OpenAI(api_key=settings.openai_api_key)
    yield 

app = FastAPI(lifespan=lifespan)

def get_llm(request: Request):
    return request.app.state.llm

def get_openai_clinet(request: Request):
    return request.app.state.openai_client

@app.post("/chats")
async def generator_chat_handler(
    user_input: str = Body(..., embed=True),
    llm: Llama = Depends(get_llm),
):
    async def event_generator():
        # [수정 포인트 1] stream=True 옵션을 반드시 추가해야 chunk 단위로 읽어옵니다.
        result = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True, # 스트리밍 활성화
        )

        # [수정 포인트 2] 비동기 환경에서 동기 제너레이터를 안전하게 돌리기 위해 루프 구성
        for chunk in result:
            try:
                # 스트리밍 시 delta 안의 content를 추출
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    token = chunk["choices"][0].get("delta", {}).get("content")
                    if token: 
                        yield token
                        # 0.1은 너무 느릴 수 있어 0.01로 조정하거나 0으로 두어 제어권만 넘깁니다.
                        await asyncio.sleep(0.01) # 원래 이렇게 안함. Docker이용하면 편해짐
            except Exception as e:
                print(f"Error processing chunk: {e}")
                break
    
    return StreamingResponse(
        event_generator(),
        media_type="text/plain", # 일반 텍스트 스트리밍을 위해 변경
    )

@app.post("/openai")
# async로 하면 문제됨. 동기로 하면 쓰레드풀에서 처리
async def openai_handler(
    user_input: str = Body(..., embed=True),
    openai_client = Depends(get_openai_clinet),
):
    # create? parse? 
    async def event_generator():
        async with openai_client.responses.stream(
            model="gpt-4.1-mini",
            input = user_input,
            text_format = OpenAIResponse,
        ) as stream:
            async for event in stream:
                # 텍스트 토큰
                if event.type == "response.output_text.delta":
                    yield event.delta
                # 더 이상 보낼게 없어서 연결을 끊겠다
                elif event.type == "response.completed":
                    break     

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

    # if response.output_parsed.confidence <= 0.95:
    #     return # 재시도

    # return response.output_parsed