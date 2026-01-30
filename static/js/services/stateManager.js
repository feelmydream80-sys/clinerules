// @DOC_FILE: stateManager.js
// @DOC_DESC: 중앙 집중식 상태 관리 시스템

import { statisticsApi } from './api.js';
import { userManagementApi } from './api.js';
import { dataAccessApi } from './api.js';
import { scheduleSettingsApi } from './api.js';
import { excelTemplateApi } from './api.js';

/**
 * 중앙 집중식 상태 관리 클래스
 */
class StateManager {
    /**
     * 생성자
     */
    constructor() {
        // 애플리케이션 상태
        this.state = {
            icons: [],
            users: [],
            menus: [],
            settings: [],
            scheduleSettings: null,
            excelTemplateInfo: null
        };
        
        // 상태 변경 리스너
        this.listeners = {};
    }

    /**
     * 상태 업데이트
     * @param {string} key - 상태 키
     * @param {any} value - 상태 값
     */
    setState(key, value) {
        this.state[key] = value;
        this.notifyListeners(key);
    }

    /**
     * 상태 조회
     * @param {string} key - 상태 키
     * @returns {any} - 상태 값
     */
    getState(key) {
        return this.state[key];
    }

    /**
     * 상태 변경 리스너 등록
     * @param {string} key - 상태 키
     * @param {function} callback - 콜백 함수
     */
    subscribe(key, callback) {
        if (!this.listeners[key]) {
            this.listeners[key] = [];
        }
        this.listeners[key].push(callback);
    }

    /**
     * 상태 변경 알림
     * @param {string} key - 상태 키
     */
    notifyListeners(key) {
        if (this.listeners[key]) {
            this.listeners[key].forEach(callback => callback(this.state[key]));
        }
    }

    /**
     * 초기 데이터 로드
     * @returns {Promise<boolean>} - 로드 성공 여부
     */
    async loadInitialData() {
        try {
            // 아이콘 데이터 로드
            const iconsResponse = await statisticsApi.getConfig();
            this.setState('icons', iconsResponse.icons || []);

            // 사용자 및 메뉴 데이터 로드
            const usersResponse = await userManagementApi.getUsers();
            this.setState('users', usersResponse.users || []);
            this.setState('menus', usersResponse.menus || []);

            // 설정 데이터 로드
            const settingsResponse = await statisticsApi.getData('daily', { 
                start_date: new Date().toISOString().split('T')[0], 
                end_date: new Date().toISOString().split('T')[0] 
            });
            this.setState('settings', settingsResponse.menu_access_stats || []);

            // 스케줄 설정 로드
            const scheduleResponse = await scheduleSettingsApi.getSettings();
            this.setState('scheduleSettings', scheduleResponse);

            // 엑셀 템플릿 정보 로드
            const excelResponse = await excelTemplateApi.getInfo();
            this.setState('excelTemplateInfo', excelResponse);

            return true;
        } catch (error) {
            console.error('초기 데이터 로드 실패:', error);
            return false;
        }
    }
}

// 전역 상태 관리 인스턴스 생성 및 내보내기
export const stateManager = new StateManager();