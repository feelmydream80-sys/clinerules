// @DOC_FILE: auth.js
// @DOC_DESC: 인증 관련 API 호출을 담당합니다.

import { sendRequest } from './client.js';

/**
 * @DOC: 서버에 현재 사용자 인증 상태를 요청하고, 사용자 정보를 반환합니다.
 * 로그인 여부, 사용자 ID, 권한, 데이터 접근 권한 등을 포함합니다.
 */
export async function getAuthStatus() {
    return await sendRequest('/api/auth/status');
}