# 경량화 버전으로 기초 베이스 깔기
FROM python:3.13-slim
# 폴더 생성: 만약 컨테이너 안에 /app이라는 폴더가 없다면, 자동 생성
# 위치 이동: 이후에 나오는 모든 명령어(COPY, RUN, CMD, ENTRYPOINT 등)를 해당 폴더 안에서 실행하도록 고정
WORKDIR /app 
# 현재 내가 가지고 있는 main.py를 Docker 안(/app)으로 이동
COPY . .
# Docker안에 fastapi 라이브러리 설치 
RUN pip install "fastapi[standard]"
# RUN...
# RUN...
# RUN... 은 복수 설정 가능
# ----------RUN: 이미지 만드는 과정에서 실행--------------
# ----------CMD: 이미지 만든 후 컨테이너 띄울 때 실행--------------

# 컨테이너 실행 될 때 fastapi 실행. CMD는 1개만 지정 가능 
# fastapi dev는 로컬 호스트 127.0.0.1
# CMD ["fastapi", "dev"]
# 만든 Dockerfile가지고 이미지 만들어야함

# fastapi가 모든 웹 요청 및 외부에서도 요청받을 수 있게 열어주겠다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
