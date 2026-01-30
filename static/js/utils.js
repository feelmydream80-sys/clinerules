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
 * @param {string} type - 메시지 타입 (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    // 기존 toast.js에서 가져온 함수 구현
    // 실제 구현은 toast.js에 위임
    import('./utils/toast.js').then(module => {
        module.showToast(message, type);
    });
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