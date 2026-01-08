// static/js/pages/dashboard.js

/**
 * @file dashboard.js
 * @description 대시보드 페이지의 진입점(Entry Point) 역할을 합니다.
 * - 필요한 모듈들을 가져와서 페이지 초기화를 담당하는 함수를 호출합니다.
 * - 각 기능의 상세 구현은 `static/js/modules/dashboard/` 디렉토리의 모듈들이 담당합니다.
 * 
 * @see {@link module:data} for data loading and state management.
 * @see {@link module:ui} for UI rendering and interaction.
 * @see {@link module:events} for event handling and main application logic.
 * 
 * @example
 * // 이 파일은 HTML에서 <script type="module" src=".../dashboard.js"></script> 형태로 로드됩니다.
 * // 별도의 호출 없이, DOMContentLoaded 이벤트에 따라 자동으로 initializeDashboard 함수가 실행됩니다.
 */

import { initializeDashboard } from '../modules/dashboard/events.js';

/**
 * @description 대시보드 페이지의 진입점 함수. router.js에 의해 호출됩니다.
 */
export function init() {
    // 대시보드 페이지에 진입할 때마다 초기화 플래그를 리셋합니다.
    window.isDashboardInitialized = false;

    // 대시보드 관련 DOM 요소가 있는지 확인하여, 중복 실행을 방지하고
    // 다른 페이지에서 불필요하게 실행되는 것을 막습니다.
    const dashboardElement = document.getElementById('dashboard-main-grid');
    if (dashboardElement && !window.isDashboardInitialized) {
        window.isDashboardInitialized = true;
        // 페이징 초기화 플래그도 리셋
        if (window.resetDashboardPagination) {
            window.resetDashboardPagination();
        }
        initializeDashboard().then(() => {
        });
    }
}

// 페이지가 동적으로 로드될 때 window 객체에 상태를 저장하여 중복 초기화를 방지합니다.
// 다른 페이지로 이동할 때 이 플래그를 초기화하는 로직이 필요할 수 있습니다.
// (현재 router.js 구조에서는 페이지 이동 시 새로 로드되므로 큰 문제는 없습니다.)
window.isDashboardInitialized = false;
