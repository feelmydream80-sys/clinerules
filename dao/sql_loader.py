import os
import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def load_sql(file_path: str) -> str:
    """
    SQL 파일을 읽어와서 쿼리 문자열을 반환합니다.
    결과는 캐시되어 반복적인 파일 I/O를 방지합니다.
    """
    # 프로젝트 루트를 찾는 여러 방법 시도
    possible_base_dirs = []

    # 방법 1: 현재 파일 위치 기준 (개발 환경)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dev_base = os.path.join(current_dir, '..')
    possible_base_dirs.append(dev_base)

    # 방법 2: 환경변수에서 프로젝트 루트 찾기
    # 리눅스 배포 환경에서 자주 사용되는 환경변수들
    env_vars = ['PROJECT_ROOT', 'APP_ROOT', 'BASE_DIR']
    for env_var in env_vars:
        env_path = os.environ.get(env_var)
        if env_path and os.path.exists(os.path.join(env_path, 'sql')):
            possible_base_dirs.append(env_path)
            break

    # 방법 3: PYTHONPATH에서 찾기
    python_path = os.environ.get('PYTHONPATH')
    if python_path:
        for path in python_path.split(':'):
            if path and os.path.exists(os.path.join(path, 'sql')):
                possible_base_dirs.append(path)
                break

    # 방법 4: 현재 작업 디렉토리 기준
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, 'sql')):
        possible_base_dirs.append(cwd)

    # 방법 5: 여러 레벨 상위 디렉토리 탐색
    current = current_dir
    for _ in range(5):  # 최대 5레벨 상위 탐색
        current = os.path.dirname(current)
        if os.path.exists(os.path.join(current, 'sql')):
            possible_base_dirs.append(current)
            break

    # 각 가능한 경로에서 SQL 파일 찾기
    sql_file_path = None
    for base_dir in possible_base_dirs:
        candidate_path = os.path.join(base_dir, 'sql', file_path)
        if os.path.exists(candidate_path):
            sql_file_path = candidate_path
            break

    if sql_file_path is None:
        # 디버깅 정보 제공
        debug_info = f"Tried paths: {[os.path.join(base, 'sql', file_path) for base in possible_base_dirs]}"
        raise FileNotFoundError(f"SQL file not found. File: {file_path}, {debug_info}")

    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found at: {sql_file_path}")
    except UnicodeDecodeError as e:
        # 다른 인코딩 시도
        try:
            with open(sql_file_path, 'r', encoding='cp949') as f:
                return f.read()
        except:
            raise e
    except Exception as e:
        raise e
