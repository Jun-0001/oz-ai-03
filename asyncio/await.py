import time
import asyncio

async def a(): 
    print("A 작업 시작") # [1] a() 실행 시작 / [1]
    await asyncio.sleep(2) # [2] 2초 대기 -> 양보 / [2]
    print("A 작업 종료")    

async def b():
    print("B 작업 시작") # [3] b() 실행 시작 / [3]
    await asyncio.sleep(2) # [4] 2초 대기 -> 양보 / [4]
    print("B 작업 종료") # [5]

start = time.time()

async def main():
    coro1 = a()
    coro2 = b()
    await asyncio.gather(coro1, coro2)

start = time.time()
asyncio.run(main())
end = time.time()
print(f"실행시간: {end - start:.2f}")

async def a():
    print("A 작업 시작")
    time.sleep(2)
    print("A 작업 완료")

async def b():
    print("B 작업 시작")
    time.sleep(2)
    print("B 작업 완료")

async def main():
    coro_1 = a()
    coro_2 = b()
    await asyncio.gather(coro_1, coro_2)

start = time.time()
asyncio.run(main())
end = time.time()
print(f"총 소요 시간: {end-start:.2f}")
