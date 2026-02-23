// static/js/modules/dashboard/data.js

/**
 * @module data
 * @description 대시보드 데이터 로딩 및 상태 관리를 담당합니다.
 * - API를 통해 관리자 설정, 아이콘, Job 목록 등 필수 데이터를 가져옵니다.
 * - 데이터 로딩 상태를 추적하고 관리합니다.
 * 
 * @example
 * // 사용 예시: main.js 또는 dashboard.js
 * import { initializeDashboardData, getJobSettings, getIconMap, getAllAdminSettings } from './modules/dashboard/data.js';
 * 
 * async function init() {
 *   try {
 *     await initializeDashboardData();
 *     const jobSettings = getJobSettings();
 *     const iconMap = getIconMap();
 *     ('초기 데이터 로드 완료:', jobSettings, iconMap);
 *   } catch (error) {
 *     console.error('데이터 초기화 실패:', error);
 *   }
 * }
 * 
 * init();
 */

import { fetchAllMstList } from '../common/api/mst.js';
import { fetchAllMngrSett, fetchAllIcons } from '../common/api/mngr_sett.js';
import { setDataFlowStatus } from '../common/api/client.js';
import { showMessage, filterActiveMstData } from '../common/utils.js';

// 사용자 정보를 가져오는 헬퍼 함수
function getUser() {
    const userElement = document.body;
    if (userElement && userElement.dataset.user) {
        try {
            return JSON.parse(userElement.dataset.user);
        } catch (e) {
            console.error('Failed to parse user data:', e);
            return null;
        }
    }
    return null;
}

// 사용자가 관리자인지 확인하는 헬퍼 함수
function isAdmin() {
    const user = getUser();
    return user && user.permissions && user.permissions.includes('admin');
}

// 전역 변수로 관리자 설정 및 아이콘 맵 저장
let allJobSettings = {}; // 모든 Job 설정 데이터를 저장할 객체 (cd -> settings)
let iconMap = {}; // icon_id -> icon_code (이모지)
let allAdminSettings = []; // 관리자 설정(아이콘/색상 등)
let dashboardSummaryData = []; // 대시보드 요약 데이터 원본 저장

// 데이터 흐름 상태를 추적하는 객체 (디버깅용)
let dataFlowStatus = {
    dashboardSummaryFetch: { apiCallInitiated: false, apiCallSuccess: false, apiResponseCount: 0, dataProcessedCount: 0, chartRendered: false, error: null },
    mstListFetch: { apiCallInitiated: false, apiCallSuccess: false, apiResponseCount: 0, dataProcessedCount: 0, error: null },
    adminSettingsFetch: { apiCallInitiated: false, apiCallSuccess: false, apiResponseCount: 0, dataProcessedCount: 0, error: null },
    iconsFetch: { apiCallInitiated: false, apiCallSuccess: false, apiResponseCount: 0, dataProcessedCount: 0, error: null },
    minMaxDatesFetch: { apiCallInitiated: false, apiCallSuccess: false, apiResponseCount: 0, dataProcessedCount: 0, error: null },
    overallStatus: "idle"
};

// dataFlowStatus 객체를 api.js 모듈에 설정
setDataFlowStatus(dataFlowStatus);

/**
 * @description 모든 Job 설정 데이터를 로드하고 allJobSettings 객체에 저장합니다.
 * @returns {Promise<void>}
 */
async function loadAllAdminSettings() {
    // This function is now deprecated as settings are fetched with the summary data.
    // Kept for potential standalone use, but should not be called during dashboard initialization.
    if (dataFlowStatus.adminSettingsFetch.apiCallInitiated) return;
    
    if (!isAdmin()) {
        return;
    }
    dataFlowStatus.adminSettingsFetch.apiCallInitiated = true;
    try {
        const settings = await fetchAllMngrSett();
        allAdminSettings = settings; // 전체 설정 저장
        allJobSettings = {};
        settings.forEach(setting => {
            allJobSettings[setting.cd] = setting;
        });
        dataFlowStatus.adminSettingsFetch.apiCallSuccess = true;
        dataFlowStatus.adminSettingsFetch.apiResponseCount = settings.length;
        dataFlowStatus.adminSettingsFetch.dataProcessedCount = Object.keys(allJobSettings).length;
    } catch (error) {
        dataFlowStatus.adminSettingsFetch.error = error.message;
        console.error("Failed to load admin settings:", error);
        showMessage('관리자 설정 로드 실패: ' + error.message, 'error');
        throw error;
    }
}

/**
 * @description 모든 아이콘 데이터를 로드하고 iconMap 객체에 저장합니다.
 * @returns {Promise<void>}
 */
async function loadAllIcons() {
    // This function is now deprecated as icon data should be part of the settings object.
    // Kept for potential standalone use, but should not be called during dashboard initialization.
    if (dataFlowStatus.iconsFetch.apiCallInitiated) return;
    
    if (!isAdmin()) {
        return;
    }
    dataFlowStatus.iconsFetch.apiCallInitiated = true;
    try {
        const icons = await fetchAllIcons();
        iconMap = {};
        icons.forEach(icon => {
            iconMap[icon.icon_id] = icon.icon_code;
        });
        dataFlowStatus.iconsFetch.apiCallSuccess = true;
        dataFlowStatus.iconsFetch.apiResponseCount = icons.length;
        dataFlowStatus.iconsFetch.dataProcessedCount = Object.keys(iconMap).length;
    } catch (error) {
        dataFlowStatus.iconsFetch.error = error.message;
        console.error("Failed to load icons:", error);
        showMessage('아이콘 로드 실패: ' + error.message, 'error');
        throw error;
    }
}

/**
 * @description 모든 Job ID 목록을 로드합니다. (현재는 호출만 하고 특별한 처리는 없음)
 * @returns {Promise<void>}
 */
async function loadAllMstList() {
    dataFlowStatus.mstListFetch.apiCallInitiated = true;
    try {
        const mstList = await fetchAllMstList();
        // use_yn 필터 적용
        const activeMstList = filterActiveMstData(mstList);
        
        dataFlowStatus.mstListFetch.apiCallSuccess = true;
        dataFlowStatus.mstListFetch.apiResponseCount = activeMstList.length;
        dataFlowStatus.mstListFetch.dataProcessedCount = activeMstList.length;
        
        return activeMstList;
    } catch (error) {
        dataFlowStatus.mstListFetch.error = error.message;
        console.error("Failed to load MST list for dashboard:", error);
        showMessage('Job ID 목록 로드 실패: ' + error.message, 'error');
        throw error;
    }
}

/**
 * @description 대시보드에 필요한 모든 초기 데이터를 병렬로 로드합니다.
 * @returns {Promise<void>}
 */
export async function initializeDashboardData() {
    // `loadAllAdminSettings` and `loadAllIcons` are removed from parallel loading
    // as this data will now be fetched with the main dashboard summary.
    await Promise.all([
        loadAllMstList()
    ]);
}

/**
 * @description 로드된 Job 설정 객체를 반환합니다.
 * @returns {Object} allJobSettings
 */
export function getJobSettings() {
    return allJobSettings;
}

/**
 * @description 로드된 아이콘 맵을 반환합니다.
 * @returns {Object} iconMap
 */
export function getIconMap() {
    return iconMap;
}

/**
 * @description 로드된 모든 관리자 설정을 반환합니다.
 * @returns {Array} allAdminSettings
 */
export function getAllAdminSettings() {
    return allAdminSettings;
}

/**
 * @description 대시보드 요약 데이터 원본을 저장합니다.
 * @param {Array} data - 저장할 데이터 배열
 */
export function setDashboardSummaryData(data) {
    dashboardSummaryData = data;
}

/**
 * @description 저장된 대시보드 요약 데이터 원본을 반환합니다.
 * @returns {Array} dashboardSummaryData
 */
export function getDashboardSummaryData() {
    return dashboardSummaryData;
}

/**
 * @description 데이터 흐름 상태 객체를 반환합니다.
 * @returns {Object} dataFlowStatus
 */
export function getDataFlowStatus() {
    return dataFlowStatus;
}
