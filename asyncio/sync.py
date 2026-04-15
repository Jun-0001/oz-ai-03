# 동기 (Syncronous)
# A 작업 -> B 작업 
import time 

# 1. 위 에서 아래로 진행. def 보자마자 파이썬의 마음 속 한 구석에 hello() 저장
# 피호출자
def hello():
    # 3. 3초 대기
    time.sleep(3)
    # 4. hello 출력. 이후 끝
    print("Hello")
    return "이게 진짜 return값임"
    # return : None

# 2. 호출자(caller) 어? 아까 만든 hello()를 실행해야겠다. 위로 다시 가자! 
hello()
# 4. return 값은 none, hello는 출력
print(hello())

