# MSYS 시스템 설치 가이드

## 시스템 요구사항

### 필수 소프트웨어
- **Python 3.8 이상** (3.9, 3.10, 3.11 권장)
- **PostgreSQL 12 이상** (13, 14, 15 권장)

### 권장 사양
- **RAM**: 4GB 이상
- **Storage**: 10GB 이상의 여유 공간
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+

## 설치 단계

### 1. Python 환경 설정

#### Windows
```bash
# Python 다운로드 및 설치 (python.org에서)
# 가상환경 생성
python -m venv msys_venv

# 가상환경 활성화
msys_venv\Scripts\activate
```

#### Linux/macOS
```bash
# Python 설치 (패키지 매니저 사용)
sudo apt update && sudo apt install python3 python3-venv  # Ubuntu
brew install python3  # macOS

# 가상환경 생성
python3 -m venv msys_venv

# 가상환경 활성화
source msys_venv/bin/activate
```

### 2. 의존성 패키지 설치

```bash
# 프로젝트 디렉토리로 이동
cd msys

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 3. 데이터베이스 설정

#### PostgreSQL 설치
- **Windows**: https://www.postgresql.org/download/windows/
- **Linux**: `sudo apt install postgresql postgresql-contrib` (Ubuntu)
- **macOS**: `brew install postgresql`

#### 데이터베이스 생성
```sql
-- PostgreSQL에 접속
psql -U postgres

-- 데이터베이스 생성
CREATE DATABASE msys_db;

-- 사용자 생성 (선택사항)
CREATE USER msys_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE msys_db TO msys_user;

-- 종료
\q
```

### 4. 환경변수 설정

`.env` 파일을 프로젝트 루트에 생성:

```env
# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=5432
DB_NAME=msys_db
DB_USER=postgres
DB_PASSWORD=your_password

# Gemini API 설정 (AI 분석 기능용)
GEMINI_API_KEY=your_gemini_api_key_here

# Flask 설정
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. 데이터베이스 스키마 설정

```bash
# PostgreSQL에 접속하여 테이블 생성
psql -U postgres -d msys_db -f database_schema.sql
```

### 6. 애플리케이션 실행

```bash
# 가상환경 활성화 확인
# Windows: msys_venv\Scripts\activate
# Linux/macOS: source msys_venv/bin/activate

# Flask 애플리케이션 실행
python msys_app.py
```

### 7. 웹 브라우저 접속

```
http://localhost:5000
```

## 문제 해결

### 일반적인 문제들

#### 1. psycopg2 설치 오류
```bash
# Windows에서 발생할 수 있는 문제
pip install --only-binary :all: psycopg2-binary

# 또는 Visual C++ Build Tools 설치 후
pip install psycopg2
```

#### 2. 포트 충돌
```bash
# 다른 포트 사용
python msys_app.py --port 5001
```

#### 3. 데이터베이스 연결 오류
- PostgreSQL 서비스가 실행 중인지 확인
- `.env` 파일의 데이터베이스 설정 확인
- 방화벽 설정 확인

#### 4. 권한 오류
```bash
# Linux/macOS에서 발생할 수 있는 문제
chmod +x msys_app.py
```

## 개발 환경 설정

### IDE 설정 (VS Code 권장)
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./msys_venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### 디버깅 설정
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "msys_app.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

## 배포 환경

### 프로덕션 환경 설정
```env
# .env.production
FLASK_ENV=production
FLASK_DEBUG=False
DB_HOST=your_production_db_host
DB_PASSWORD=your_secure_password
```

### Gunicorn 사용 (Linux/macOS)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 msys_app:app
```

### Docker 사용 (선택사항)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "msys_app.py"]
```

## 지원 및 문의

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.8 이상)
2. PostgreSQL 연결 상태
3. 환경변수 설정
4. 로그 파일 확인

## 라이선스

이 프로젝트는 내부 사용을 위한 시스템입니다. 