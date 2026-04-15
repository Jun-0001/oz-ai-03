import asyncio
import time

# 1) await는 반드시 비동기 함수안에서 사용 가능하다
# def hello(): ❌
#     await asyncio.sleep(3)

# 2) await 할 수 있는 코드앞에만 await를 쓸 수있다
async def hi():
    # await time.sleep(2)
    print("start hello...")
    await asyncio.sleep(2)
    print("end hello...")

async def main():
    print("start main...")
    coro = hi()
    await coro # hi()가 종료될때까지 대기
    print("end main...")

asyncio.run(main())
