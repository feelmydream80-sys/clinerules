# update_password.py
import sys
from getpass import getpass
from service.password_service import PasswordService
from mapper.user_mapper import UserMapper

def update_user_password():
    """
    특정 사용자의 비밀번호를 업데이트하는 스크립트.
    """
    if len(sys.argv) != 2:
        print("사용법: python update_password.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    
    print(f"'{user_id}' 사용자의 새 비밀번호를 입력합니다.")
    password = getpass("새 비밀번호: ")
    password_confirm = getpass("새 비밀번호 확인: ")

    if password != password_confirm:
        print("오류: 비밀번호가 일치하지 않습니다.")
        sys.exit(1)
        
    if not password:
        print("오류: 비밀번호는 비워둘 수 없습니다.")
        sys.exit(1)

    try:
        hashed_password = PasswordService.hash_password(password)
        
        user_mapper = UserMapper()
        user = user_mapper.find_by_id(user_id)
        if not user:
            print(f"오류: '{user_id}' 사용자를 찾을 수 없습니다.")
            sys.exit(1)
            
        user_mapper.update_password(user_id, hashed_password)
        print(f"'{user_id}' 사용자의 비밀번호가 성공적으로 업데이트되었습니다.")

    except Exception as e:
        print(f"비밀번호 업데이트 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == '__main__':
    update_user_password()
