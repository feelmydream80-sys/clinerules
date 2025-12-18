#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from msys_app import create_app
from msys.database import get_db_connection
from service.mngr_sett_service import MngrSettService
import json
import logging

logging.basicConfig(level=logging.INFO)

try:
    app = create_app()
    with app.app_context():
        conn = get_db_connection()
        service = MngrSettService(conn)

        print('=== Service 직접 테스트 ===')

        # 서비스 메소드 직접 호출
        result = service.get_schedule_settings_service()

        print(f'결과 타입: {type(result)}')
        if result:
            print(f'결과 필드 수: {len(result)}')

            # JSON 직렬화 테스트
            try:
                json_str = json.dumps(result, ensure_ascii=False, indent=2)
                print('✅ JSON 직렬화 성공!')
                print(f'JSON 길이: {len(json_str)} 문자')

                # 일부 내용 확인
                sample_keys = list(result.keys())[:5]
                print(f'샘플 키들: {sample_keys}')

            except Exception as json_error:
                print(f'❌ JSON 직렬화 실패: {json_error}')
                print(f'에러 타입: {type(json_error)}')
        else:
            print('❌ 결과가 None입니다')

except Exception as e:
    print(f'에러: {e}')
    import traceback
    traceback.print_exc()
