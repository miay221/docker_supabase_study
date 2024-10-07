# Python 3.11을 사용하여 컨테이너를 빌드
FROM python:3.11-slim

# 작업 디렉터리를 설정
WORKDIR /app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt /app/

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드를 컨테이너로 복사
COPY . /app

# Flask 애플리케이션 실행을 위한 포트 개방
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "app.py"]
