// @DOC_FILE: utils.js
// @DOC_DESC: 공통 유틸리티 함수 모음

/**
 * 디버그 로그 함수
 * @param {...any} args - 로그 메시지
 */
function debugLog(...args) {
    // 디버그 모드 설정 (프로덕션에서는 false로 변경)
    const DEBUG_MODE = true; // TODO: 프로덕션 배포 시 false로 변경
    if (DEBUG_MODE) {
        console.log('[MngrSett]', ...args);
    }
}

/**
 * 토스트 메시지 표시 함수
 * @param {string} message - 표시할 메시지
 * @param {string} category - 메시지 타입 (success, error, warning, info)
 */
function showToast(message, category = 'info') {
    // 직접 toast.js의 showToast 함수 구현을 호출 (동적 import 제거)
    const container = getOrCreateToastContainer();

    const toast = document.createElement('div');
    toast.textContent = message;

    // --- 기본 스타일 ---
    toast.style.padding = '12px 20px';
    toast.style.color = 'white';
    toast.style.borderRadius = '5px';
    toast.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.minWidth = '250px';
    toast.style.maxWidth = '400px';
    toast.style.wordBreak = 'break-all';

    // --- 카테고리별 스타일 ---
    let bgColor;
    switch (category) {
        case 'success':
            bgColor = '#28a745'; // Green
            break;
        case 'warning':
            bgColor = '#ffc107'; // Yellow
            toast.style.color = '#333';
            break;
        case 'error':
            bgColor = '#dc3545'; // Red
            break;
        default:
            bgColor = '#17a2b8'; // Blue (Info)
            break;
    }
    toast.style.backgroundColor = bgColor;

    container.appendChild(toast);

    // --- 나타나는 애니메이션 ---
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);

    // --- 자동으로 사라지는 로직 ---
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.addEventListener('transitionend', () => {
            toast.remove();
        });
    }, 5000);
}

/**
 * 토스트 알림 컨테이너를 가져오거나 생성합니다.
 * @returns {HTMLElement} 토스트 컨테이너 엘리먼트
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.top = '80px';
        container.style.right = '20px';
        container.style.zIndex = '2000';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.alignItems = 'flex-end';
        container.style.gap = '10px';
        document.body.appendChild(container);
    }
    return container;
}

/**
 * 색상 입력 활성화 함수
 * @param {HTMLElement} inputElement - 색상 입력 요소
 */
let activeColorInput = null;

function setActiveColorInput(inputElement) {
    // Remove highlight from previous active input's container
    if (activeColorInput && activeColorInput.parentElement.parentElement) {
        activeColorInput.parentElement.parentElement.classList.remove('ring-2', 'ring-blue-500', 'rounded-md');
    }
    
    activeColorInput = inputElement;

    // Add highlight to new active input's container
    if (activeColorInput && activeColorInput.parentElement.parentElement) {
        activeColorInput.parentElement.parentElement.classList.add('ring-2', 'ring-blue-500', 'rounded-md');
    }
}

/**
 * 상태 설정 로우 생성 함수
 * @param {string} prefix - 요소 ID 접두사
 * @param {string} label - 표시 레이블
 * @param {number|null} selectedIconId - 선택된 아이콘 ID
 * @param {string} bgColorValue - 배경색 값
 * @param {string} textColorValue - 텍스트 색상 값
 * @param {Array<Object>} allIcons - 전체 아이콘 목록
 * @param {boolean} isIconOnly - 아이콘만 표시 여부
 * @returns {string} - HTML 문자열
 */
function createStatusSettingRow(prefix, label, selectedIconId, bgColorValue, textColorValue, allIcons, isIconOnly = false) {
    const iconOptions = allIcons
        .filter(icon => icon.icon_dsp_yn === true)
        .map(icon => `<option value="${icon.icon_id}" ${icon.icon_id === selectedIconId ? 'selected' : ''}>${icon.icon_cd}</option>`)
        .join('');

    if (isIconOnly) {
        return `
            <div class="form-group">
                <label for="${prefix}_icon_id" class="block text-sm font-medium text-gray-700">${label}</label>
                <select id="${prefix}_icon_id" class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option value="">선택 안 함</option>
                    ${iconOptions}
                </select>
            </div>
        `;
    }

    return `
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-center p-3 rounded-md border bg-gray-50">
            <div class="font-medium text-gray-800">${label}</div>
            <div class="form-group">
                <label for="${prefix}_icon_id" class="block text-xs font-medium text-gray-600 mb-1">아이콘</label>
                <select id="${prefix}_icon_id" class="w-full p-2 border border-gray-300 rounded-md shadow-sm">
                    <option value="">선택 안 함</option>
                    ${iconOptions}
                </select>
            </div>
            <div class="form-group">
                <label for="${prefix}_bg_colr" class="block text-xs font-medium text-gray-600 mb-1">배경색</label>
                <div class="color-input-wrapper">
                     <span class="color-preview"></span>
                    <input type="color" id="${prefix}_bg_colr" value="${bgColorValue || '#FFFFFF'}" class="w-full h-10 p-1 border border-gray-300 rounded-md shadow-sm">
                </div>
            </div>
            <div class="form-group">
                <label for="${prefix}_txt_colr" class="block text-xs font-medium text-gray-600 mb-1">글자색</label>
                 <div class="color-input-wrapper">
                    <span class="color-preview"></span>
                    <input type="color" id="${prefix}_txt_colr" value="${textColorValue || '#000000'}" class="w-full h-10 p-1 border border-gray-300 rounded-md shadow-sm">
                </div>
            </div>
        </div>
    `;
}

/**
 * 선택 항목 이동 함수
 * @param {HTMLElement} fromList - 출발지 리스트
 * @param {HTMLElement} toList - 목적지 리스트
 */
function moveSelectedItems(fromList, toList) {
    const selectedItems = Array.from(fromList.querySelectorAll('li.selected'));
    selectedItems.forEach(item => {
        item.classList.remove('selected');
        toList.appendChild(item);
    });
}

/**
 * 전체 항목 이동 함수
 * @param {HTMLElement} fromList - 출발지 리스트
 * @param {HTMLElement} toList - 목적지 리스트
 */
function moveAllItems(fromList, toList) {
    const allItems = Array.from(fromList.querySelectorAll('li'));
    allItems.forEach(item => {
        item.classList.remove('selected');
        toList.appendChild(item);
    });
}

export { 
    debugLog, 
    showToast, 
    setActiveColorInput, 
    createStatusSettingRow, 
    moveSelectedItems, 
    moveAllItems 
};