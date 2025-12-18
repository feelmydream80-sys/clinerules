import { parseCronExpression, debounce } from '../common/utils.js';
import { initPagination } from '../ui_components/pagination.js';

// --- Module State ---
let allJobData = [];
let currentJobInfoPageSize = 5;

// --- Job Info Table Functions ---

export function initJobInfo(data, pageSize = 5) {
    allJobData = data;
    currentJobInfoPageSize = pageSize;

    // 검색 이벤트 리스너 설정 (한 번만 실행되도록)
    setupJobInfoSearchListener();
    
    initPagination({
        fullData: allJobData,
        pageSize: currentJobInfoPageSize,
        renderTableCallback: renderJobInfoTableContent,
        paginationId: 'jobInfoPagination',
        pageSizeId: 'jobInfoPageSize',
    });
}

// 검색 이벤트 리스너 중복 등록을 방지하기 위한 플래그
let isSearchListenerSetup = false;

function setupJobInfoSearchListener() {
    if (isSearchListenerSetup) return;

    const searchInput = document.getElementById('jobInfoSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(() => {
            const searchTerm = searchInput.value.toLowerCase();
            const filteredData = allJobData.filter(job => {
                // 모든 열의 값을 대상으로 검색
                return (job.job_id && job.job_id.toLowerCase().includes(searchTerm)) ||
                       (job.cd_nm && job.cd_nm.toLowerCase().includes(searchTerm)) ||
                       (job.cron && job.cron.toLowerCase().includes(searchTerm)) ||
                       (job.description && job.description.toLowerCase().includes(searchTerm));
            });
            // 필터링된 데이터로 페이지네이션을 다시 초기화
            initPagination({
                fullData: filteredData,
                pageSize: currentJobInfoPageSize,
                renderTableCallback: renderJobInfoTableContent,
                paginationId: 'jobInfoPagination',
                pageSizeId: 'jobInfoPageSize',
            });
        }, 300));
        isSearchListenerSetup = true;
    }
}

export function updateJobInfoSearch(term) {
    // This function is now handled by the pagination module
}

export function updateJobInfoPageSize(size) {
    // This function is now handled by the pagination module
}

export function renderPagedJobInfo() {
    // This function is now handled by the pagination module
}

function renderJobInfoTableContent(pageData) {
    const table = document.getElementById('jobInfoTable');
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    pageData.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="px-4 py-2 border-b text-center">${item.job_id || 'N/A'}</td>
            <td class="px-4 py-2 border-b text-center">${item.cd_nm || 'N/A'}</td>
            <td class="px-4 py-2 border-b text-center">
                <div>${item.cron || 'N/A'}</div>
                <div class="text-xs text-gray-500 mt-1">${parseCronExpression(item.cron)}</div>
            </td>
            <td class="px-4 py-2 border-b text-center">${item.description || 'N/A'}</td>
        `;
        tbody.appendChild(tr);
    });
}
