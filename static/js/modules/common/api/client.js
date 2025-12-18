// static/js/modules/common/api/client.js
import { showToast as showMessage } from '../../../utils/toast.js';

let globalDataFlowStatus = {};

export function setDataFlowStatus(statusObject) {
    globalDataFlowStatus = statusObject;
}

export function updateApiStatus(apiName, field, value) {
    if (!globalDataFlowStatus) {
        console.warn(`[API Module] globalDataFlowStatus has not been initialized. (API: ${apiName}, Field: ${field})`);
        return;
    }
    if (!globalDataFlowStatus[apiName]) {
        globalDataFlowStatus[apiName] = {
            apiCallAttempted: false,
            apiCallSuccess: false,
            apiResponseCount: 0,
            dataProcessedCount: 0,
            chartRendered: false,
            error: null
        };
    }
    globalDataFlowStatus[apiName][field] = value;
    if (field === "error" && value !== null) {
        globalDataFlowStatus.overallStatus = "error";
    }
}

/**
 * @DOC: 서버에 API 요청을 보내고 응답을 JSON으로 파싱하는 공통 래퍼 함수입니다.
 * @param {string} url - 요청을 보낼 API 엔드포인트입니다.
 * @param {object} [options={}] - fetch 함수에 전달될 옵션 객체입니다 (method, headers, body 등).
 * @returns {Promise<any>} - 성공 시 파싱된 JSON 데이터를, 실패 시 에러를 던집니다.
 */
export async function sendRequest(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            // 서버가 에러 응답을 반환한 경우 (e.g., 4xx, 5xx)
            const errorData = await response.json().catch(() => ({ message: response.statusText }));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        // 네트워크 오류 또는 JSON 파싱 오류
        console.error(`[API Client] Request failed for ${url}:`, error);
        showMessage(`데이터를 가져오는 데 실패했습니다: ${error.message}`, 'error');
        throw error; // 오류를 다시 던져 호출한 쪽에서 처리할 수 있도록 함
    }
}
