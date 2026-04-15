import time

def factorial(n):
    ans = 1
    for i in range(1, n+1):
        ans *= i
        yield ans

start = time.time()


for r in factorial(1000):
    print(r)

end = time.time()
print(f"실행 시간: {(end - start)*1000}ms")