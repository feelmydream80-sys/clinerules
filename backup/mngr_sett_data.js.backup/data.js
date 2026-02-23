import { showMessage } from '../common/utils.js';
import { fetchAllMngrSett, fetchAllIcons } from '../common/api/mngr_sett.js';

// @DOC: 이 파일은 서버로부터 관리자 설정 관련 데이터를 가져오고 관리하는 역할을 합니다.
// 데이터 캐싱을 통해 중복 API 호출을 방지하고 애플리케이션의 성능을 향상시킵니다.

let allIcons = null;
let allMngrSett = null;

/**
 * @DOC: 서버에서 모든 관리자 설정 데이터를 비동기적으로 가져옵니다.
 * 이미 데이터가 캐시되어 있는 경우, 캐시된 데이터의 깊은 복사본을 반환합니다.
 * 그렇지 않은 경우, 서버에서 데이터를 가져와 캐싱하고 깊은 복사본을 반환합니다.
 * @returns {Promise<Array<Object>>} 성공 시 관리자 설정 데이터 배열을, 실패 시 에러를 반환합니다.
 */
export function getAdminSettings() {
    return fetchAllMngrSett().then(data => {
        allMngrSett = JSON.parse(JSON.stringify(data));
        return JSON.parse(JSON.stringify(allMngrSett));
    }).catch(error => {
        console.error("Failed to load manager settings:", error);
        showMessage('관리자 설정 로드 실패: ' + error.message, 'error');
        throw error;
    });
}

/**
 * @DOC: 서버에서 모든 아이콘 데이터를 비동기적으로 가져옵니다.
 * 이미 데이터가 캐시되어 있는 경우, 캐시된 데이터의 깊은 복사본을 반환합니다.
 * 그렇지 않은 경우, 서버에서 데이터를 가져와 캐싱하고 깊은 복사본을 반환합니다.
 * @returns {Promise<Array<Object>>} 성공 시 아이콘 데이터 배열을, 실패 시 에러를 반환합니다.
 */
export function getIcons() {
    return fetchAllIcons().then(data => {
        allIcons = JSON.parse(JSON.stringify(data));
        return JSON.parse(JSON.stringify(allIcons));
    }).catch(error => {
        console.error("Failed to load icons:", error);
        showMessage('아이콘 목록 로드 실패: ' + error.message, 'error');
        throw error;
    });
}
