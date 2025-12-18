#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSYS 시스템 자동 설치 및 체크 스크립트
Python 버전과 필요한 모듈들을 자동으로 확인하고 설치합니다.
"""

import sys
import subprocess
import pkg_resources
import platform
import os
from pathlib import Path

# 필요한 패키지와 버전
REQUIRED_PACKAGES = {
    'Flask': '2.3.3',
    'Flask-CORS': '4.0.0',
    'psycopg2-binary': '2.9.7',
    'python-dotenv': '1.0.0',
    'requests': '2.31.0'
}

# 최소 Python 버전
MIN_PYTHON_VERSION = (3, 8)

def check_python_version():
    """Python 버전을 확인합니다."""
    print("🐍 Python 버전 확인 중...")
    current_version = sys.version_info[:2]
    
    if current_version < MIN_PYTHON_VERSION:
        print(f"❌ Python 버전이 너무 낮습니다!")
        print(f"   현재 버전: {sys.version}")
        print(f"   필요 버전: {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} 이상")
        print("\n📥 Python을 업데이트하세요:")
        print("   https://www.python.org/downloads/")
        return False
    else:
        print(f"✅ Python 버전 확인 완료: {sys.version}")
        return True

def get_installed_packages():
    """설치된 패키지 목록을 가져옵니다."""
    installed = {}
    for dist in pkg_resources.working_set:
        installed[dist.project_name] = dist.version
    return installed

def check_package_version(package_name, required_version):
    """특정 패키지의 버전을 확인합니다."""
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        return pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version(required_version)
    except pkg_resources.DistributionNotFound:
        return False

def install_package(package_name, version):
    """패키지를 설치합니다."""
    print(f"📦 {package_name} 설치 중...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            f"{package_name}=={version}"
        ])
        print(f"✅ {package_name} 설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} 설치 실패: {e}")
        return False

def check_and_install_packages():
    """필요한 패키지들을 확인하고 설치합니다."""
    print("\n📦 패키지 확인 및 설치 중...")
    
    installed_packages = get_installed_packages()
    missing_packages = []
    outdated_packages = []
    
    for package, required_version in REQUIRED_PACKAGES.items():
        if package not in installed_packages:
            missing_packages.append((package, required_version))
            print(f"❌ {package} 미설치")
        elif not check_package_version(package, required_version):
            outdated_packages.append((package, required_version))
            print(f"⚠️  {package} 버전이 낮음 (현재: {installed_packages[package]}, 필요: {required_version})")
        else:
            print(f"✅ {package} 확인 완료 (버전: {installed_packages[package]})")
    
    # 설치가 필요한 패키지들
    packages_to_install = missing_packages + outdated_packages
    
    if packages_to_install:
        print(f"\n🔧 {len(packages_to_install)}개 패키지 설치 필요")
        response = input("자동으로 설치하시겠습니까? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            success_count = 0
            for package, version in packages_to_install:
                if install_package(package, version):
                    success_count += 1
            
            print(f"\n📊 설치 결과: {success_count}/{len(packages_to_install)} 성공")
            
            if success_count < len(packages_to_install):
                print("\n⚠️  일부 패키지 설치에 실패했습니다.")
                print("수동으로 설치해주세요:")
                for package, version in packages_to_install:
                    print(f"   pip install {package}=={version}")
        else:
            print("\n📋 수동 설치 명령어:")
            for package, version in packages_to_install:
                print(f"   pip install {package}=={version}")
    else:
        print("\n✅ 모든 패키지가 설치되어 있습니다!")

def check_postgresql():
    """PostgreSQL 설치 여부를 확인합니다."""
    print("\n🐘 PostgreSQL 확인 중...")
    
    # Windows에서 PostgreSQL 확인
    if platform.system() == "Windows":
        pg_paths = [
            r"C:\Program Files\PostgreSQL",
            r"C:\Program Files (x86)\PostgreSQL"
        ]
        
        for path in pg_paths:
            if os.path.exists(path):
                print(f"✅ PostgreSQL 발견: {path}")
                return True
        
        print("❌ PostgreSQL이 설치되지 않았습니다.")
        print("📥 PostgreSQL을 설치하세요:")
        print("   https://www.postgresql.org/download/windows/")
        return False
    
    # Linux/macOS에서 PostgreSQL 확인
    else:
        try:
            result = subprocess.run(['which', 'psql'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PostgreSQL 발견: {result.stdout.strip()}")
                return True
            else:
                print("❌ PostgreSQL이 설치되지 않았습니다.")
                if platform.system() == "Darwin":  # macOS
                    print("📥 설치 명령어: brew install postgresql")
                else:  # Linux
                    print("📥 설치 명령어: sudo apt install postgresql postgresql-contrib")
                return False
        except FileNotFoundError:
            print("❌ PostgreSQL이 설치되지 않았습니다.")
            return False

def create_env_template():
    """환경변수 템플릿 파일을 생성합니다."""
    env_file = Path(".env")
    if not env_file.exists():
        print("\n📝 .env 파일 생성 중...")
        env_content = """# 데이터베이스 설정
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
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env 파일 생성 완료")
        print("⚠️  데이터베이스 설정을 수정해주세요!")
    else:
        print("\n✅ .env 파일이 이미 존재합니다.")

def main():
    """메인 함수"""
    print("🚀 MSYS 시스템 설치 체크 시작")
    print("=" * 50)
    
    # Python 버전 확인
    if not check_python_version():
        sys.exit(1)
    
    # 패키지 확인 및 설치
    check_and_install_packages()
    
    # PostgreSQL 확인
    check_postgresql()
    
    # 환경변수 파일 생성
    create_env_template()
    
    print("\n" + "=" * 50)
    print("🎉 설치 체크 완료!")
    print("\n📋 다음 단계:")
    print("1. PostgreSQL 설치 및 데이터베이스 생성")
    print("2. .env 파일에서 데이터베이스 설정 수정")
    print("3. python msys_app.py로 애플리케이션 실행")
    print("\n📖 자세한 내용은 INSTALLATION_GUIDE.md를 참조하세요.")

if __name__ == "__main__":
    main() 