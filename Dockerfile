FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성·설정
RUN mkdir /app
WORKDIR /app

# 필수 패키지 설치 (libffi-dev, gcc, build-essential, Rust)
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    libffi-dev \
    gcc \
    g++ \
    make \
    rust \
    cargo \
    openssl-dev

# Python 및 MySQL 관련 패키지 설치
RUN apk update && apk add python3 python3-dev mariadb-dev build-base \
    && pip3 install mysqlclient \
    && apk del python3-dev mariadb-dev build-base

# Python 종속성 설치 (requirements.txt)
RUN apk update && apk add libpq
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache jpeg-dev zlib-dev mariadb-dev
COPY requirements.txt /app/requirements.txt

# pip 최신화 및 패키지 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 빌드 패키지 정리하여 컨테이너 크기 줄이기
RUN apk del jpeg-dev zlib-dev build-deps

# 컨테이너로 소스 코드 복사
COPY . /app/
