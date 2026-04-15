# 동기식 
# 1) 함수 정의: def foo(): 
# 2) 함수 호출: foo() => 함수 실행 

# 비동기식 
# 코루틴 -> 나눠서 협력. 너 한번. 나 한번. 
# 1) 함수 정의: async def boo():
# 2) 코루틴 함수 호출: boo() => 코루틴 객체 생성 , coro(코루틴 객체) = boo() 
# 3) 코루틴 실행 -> import asyncio 라이브러리 필요

import asyncio

async def hello():
    print("hello")

coro1 = hello()
coro2 = hello()

async def main():
    await asyncio.gather(coro1, coro2)

# 보통 이렇게 하는게 맞음 
main_coro = main()
# run은 무조건 하나의 객체만 넘겨줄 수 있음
asyncio.run(coro1)