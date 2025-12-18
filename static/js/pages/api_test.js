/**
 * API 테스트 페이지 메인 로직
 * 
 * [기능 개요]
 * 이 파일은 API 테스트 페이지의 모든 상호작용을 관리합니다.
 * 페이지 로드 시 다음 작업을 수행합니다:
 * 1. 기본 날짜 범위 설정 (오늘로부터 한 달 전 ~ 오늘)
 * 2. 탭 기반 UI 초기화 (Dashboard, Analytics, Data Analysis 등)
 * 3. API 호출 기능 설정 (GET/POST 메소드 지원)
 * 4. 요청/응답 처리 및 화면 표시
 */
import { setDefaultDates } from '../modules/common/dateUtils.js';
import { initializeTabs } from '../modules/common/ui.js';

// ===== [초기화 함수] =====
export function init() {
    // 1. 날짜 입력 필드에 기본값 설정
    setDefaultDates();
    
    // 2. 탭 UI 초기화 및 API 섹션 생성
    initializeTabs();
}

/**
 * API 테스트 실행 (전역 함수로 노출)
 * 
 * [기능]
 * - API 호출 버튼 클릭 시 실행되는 핵심 함수
 * - 입력된 요청 데이터 파싱 및 유효성 검사
 * - RESTful 스타일 URL 파라미터 자동 치환 (예: /api/users/{userId} → /api/users/123)
 * - GET/POST 메소드에 따른 요청 처리 분기
 * - JSON 응답 포맷팅 및 하이라이팅
 * - 오류 처리 및 사용자 피드백 제공
 */
window.testApi = async function(button, endpoint, method, id) {
    const dataElement = document.getElementById(`data-${id}`);
    const responseArea = document.getElementById(`response-${id}`);
    const spinner = button.querySelector('.loading-spinner');
    const buttonText = button.querySelector('span:not(.loading-spinner)');
    let url = endpoint;

    try {
        // Show loading state
        button.disabled = true;
        spinner.classList.remove('hidden');
        buttonText.textContent = '처리 중...';
        responseArea.textContent = '요청을 처리 중입니다...';

        const minDisplayTime = new Promise(resolve => setTimeout(resolve, 200)); // 최소 1초 대기
        const apiCall = (async () => {
            let requestData = {};
            try {
                requestData = JSON.parse(dataElement.value);
            } catch (e) {
                throw new Error('유효한 JSON 형식이 아닙니다.');
            }

            const queryParams = new URLSearchParams();
            Object.keys(requestData).forEach(key => {
                const placeholder = `{${key}}`;
                if (url.includes(placeholder)) {
                    url = url.replace(placeholder, encodeURIComponent(requestData[key]));
                    delete requestData[key];
                } else if (method === 'GET') {
                    if (requestData[key] !== null && requestData[key] !== '') {
                        queryParams.append(key, requestData[key]);
                    }
                }
            });

            if (queryParams.toString() && method === 'GET') {
                url += (url.includes('?') ? '&' : '?') + queryParams.toString();
            }

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000);

            const options = {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                signal: controller.signal
            };

            if (method !== 'GET' && Object.keys(requestData).length > 0) {
                options.body = JSON.stringify(requestData);
            }

            const response = await fetch(url, options);
            clearTimeout(timeoutId);
            const responseData = await response.json();

            const urlDisplay = `Called URL: ${url}\n\n`;
            responseArea.textContent = urlDisplay + JSON.stringify(responseData, null, 2);
            responseArea.className = response.ok ? 'text-green-100' : 'text-red-100';
        })();

        await Promise.all([apiCall, minDisplayTime]);

    } catch (error) {
        console.error('API 호출 중 오류 발생:', error);
        if (error.name === 'AbortError') {
            responseArea.textContent = `오류 발생: 요청 시간이 15초를 초과했습니다.`;
        } else {
            const urlDisplay = `Called URL: ${url}\n\n`;
            responseArea.textContent = urlDisplay + `오류 발생: ${error.message}`;
        }
        responseArea.className = 'text-red-100';
    } finally {
        // Reset button state
        button.disabled = false;
        spinner.classList.add('hidden');
        buttonText.textContent = 'API 호출';
    }
};
