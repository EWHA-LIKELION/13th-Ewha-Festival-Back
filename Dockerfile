FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성 및 설정
RUN mkdir /app
WORKDIR /app

# 필수 패키지 설치 (MySQL, S3, cryptography 관련 패키지 포함)
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    libffi-dev \
    libressl-dev \
    musl-dev \
    gcc \
    g++ \
    make \
    openssl-dev \
    jpeg-dev \        
    zlib-dev \      
    libjpeg \  
    freetype-dev \
    lcms2-dev \   
    libwebp-dev \ 
    tiff-dev \   
    harfbuzz-dev \  
    fribidi-dev \  
    libpq \
    mariadb-dev \
    python3 \
    python3-dev \
    build-base

# 최신 pip 설치 및 cryptography 바이너리 설치 (Rust 없이)
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --only-binary cryptography cryptography

# MySQL 관련 패키지 설치
RUN pip install mysqlclient

# Django S3 관련 패키지 설치
RUN pip install django-storages boto3

# requirements.txt 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ✅ Pillow 명시적으로 설치 (libjpeg.so.8 문제 해결)
RUN pip install --no-cache-dir Pillow

# 불필요한 패키지 삭제 (컨테이너 크기 최적화)
RUN apk del python3-dev mariadb-dev build-base

# 컨테이너 내부 환경 변수 설정 (S3용)
ENV AWS_ACCESS_KEY_ID=your-access-key
ENV AWS_SECRET_ACCESS_KEY=your-secret-key
ENV AWS_STORAGE_BUCKET_NAME=your-bucket-name

# 컨테이너로 소스 코드 복사
COPY . /app/
