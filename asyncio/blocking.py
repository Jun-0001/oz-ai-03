# eventloop -> 함수 관리하는 중간 관리자
# eventloop blocking? -> coroutine에서 양보 안하는거 
# 비동기 함수 안에서 
import asyncio
import time

async def request1():
    print("[1] 새로운 웹 요청...")
    await asyncio.sleep(2) # 비동기
    print("[1] 응답...")

async def request2():
    print("[2] 새로운 웹 요청...")
    # await asyncio.sleep(5)
    time.sleep(5) # 동기. 그냥 마이웨이 내 갈길 간다. 난 이기적이니까. 나 끝날때가지 기다려
    print("[2] 응답...")

async def main():
    coro1 = request1()
    coro2 = request2()
    await asyncio.gather(coro1, coro2)

start = time.time()
asyncio.run(main())
end = time.time()
print(f"{end - start:.2f}")