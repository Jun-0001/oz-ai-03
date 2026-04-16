# 이미지를 직접 빌드할려고 
# 추론만 하는 프로그램
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "-u", "main.py" ]