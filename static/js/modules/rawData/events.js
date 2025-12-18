/**
 * @module events
 * @description 이벤트 리스너 등록 및 관리를 담당하는 모듈
 */

import { filterData, downloadExcel } from './utils.js';

/**
 * 기본 이벤트 리스너를 등록합니다.
 * @param {object} state - 현재 애플리케이션 상태 객체
 * @param {Function} rerender - UI를 다시 렌더링하는 함수 (클라이언트 사이드)
 * @param {Function} reloadData - 데이터를 서버에서 다시 로드하는 함수
 */
export function setupEventListeners(state, rerender, reloadData) {
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const jobSelect = document.getElementById('job-id-select');
    const searchInput = document.getElementById('table-search');
    const pageSizeSelect = document.getElementById('pageSizeSelect');
    const excelBtn = document.getElementById('excel-download-btn');

    // 데이터 리로드가 필요한 이벤트
    startDateInput.addEventListener('change', reloadData);
    endDateInput.addEventListener('change', reloadData);
    jobSelect.addEventListener('change', reloadData);

    // 클라이언트 사이드에서 처리 가능한 이벤트
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            state.searchTerm = this.value.trim();
            state.currentPage = 1;
            rerender();
        });
    }

    if (pageSizeSelect) {
        pageSizeSelect.addEventListener('change', function() {
            state.pageSize = parseInt(this.value, 10);
            state.currentPage = 1;
            rerender();
        });
    }

    if (excelBtn) {
        excelBtn.addEventListener('click', function() {
            const filtered = filterData(state);
            downloadExcel(filtered);
        });
    }
}
