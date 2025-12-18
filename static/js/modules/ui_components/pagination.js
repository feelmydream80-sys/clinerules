// static/js/modules/ui_components/pagination.js
/*
 * 주요 역할: 데이터의 페이징, 검색, 렌더링을 관리하는 모듈입니다.
 * 각 페이징 인스턴스는 고유 ID를 통해 독립적인 상태를 가집니다.
 */

// 모듈의 모든 인스턴스 상태를 관리하는 Map
const paginationInstances = new Map();

/**
 * 현재 페이지에 해당하는 데이터를 렌더링하고, 페이징 컨트롤을 다시 그립니다.
 * @param {string} id - 페이징 인스턴스의 고유 ID
 */
function renderPage(id) {
    const state = paginationInstances.get(id);
    if (!state || !state.fullData) return;

    // 필터링은 외부에서 처리된 데이터를 그대로 사용합니다.
    state.filteredData = state.fullData;
    state.totalItems = state.filteredData.length;

    // 2. 데이터가 없을 경우 처리
    if (state.filteredData.length === 0) {
        if (state.renderTableCallback) {
            state.renderTableCallback([]); // 콜백을 호출하여 빈 테이블을 렌더링
        }
        if (state.paginationElement) {
            state.paginationElement.innerHTML = '<span class="ml-4 text-sm text-gray-600">데이터가 없습니다.</span>';
        }
        if (state.totalCountElement) {
            state.totalCountElement.textContent = `총 0개`;
        }
        return;
    }
    
    // 3. 현재 페이지에 맞는 데이터 슬라이싱
    const startIndex = (state.currentPage - 1) * state.pageSize;
    const pageData = state.filteredData.slice(startIndex, startIndex + state.pageSize);
    
    // 4. 콜백을 통해 테이블 렌더링
    if (state.renderTableCallback) {
        state.renderTableCallback(pageData);
    }
    
    // 5. 총 아이템 개수 표시
    if (state.totalCountElement) {
        state.totalCountElement.textContent = `총 ${state.totalItems}개`;
    }
    
    // 6. 페이징 컨트롤 렌더링
    renderPaginationControls(id);
}

/**
 * 페이징 컨트롤 UI(버튼, 페이지 번호 등)를 렌더링합니다.
 * @param {string} id - 페이징 인스턴스의 고유 ID
 */
function renderPaginationControls(id) {
    const state = paginationInstances.get(id);
    if (!state || !state.paginationElement) return;

    const totalPages = Math.ceil(state.totalItems / state.pageSize);
    if (totalPages <= 1) {
        state.paginationElement.innerHTML = ''; // 페이지가 하나뿐이면 컨트롤 숨김
        return;
    }

    let html = '';
    const maxVisiblePages = 5;
    const currentPage = state.currentPage;
    const idPrefix = state.paginationId;

    // 처음 & 이전 버튼
    if (totalPages > maxVisiblePages) {
        html += `<button class="px-3 py-1 mx-1 border rounded ${currentPage === 1 ? 'bg-gray-200 text-gray-500 cursor-not-allowed' : 'bg-white hover:bg-gray-50'}" ${currentPage === 1 ? 'disabled' : ''} id="${idPrefix}-firstPage">처음</button>`;
    }
    html += `<button class="px-3 py-1 mx-1 border rounded ${currentPage === 1 ? 'bg-gray-200 text-gray-500 cursor-not-allowed' : 'bg-white hover:bg-gray-50'}" ${currentPage === 1 ? 'disabled' : ''} id="${idPrefix}-prevPage">이전</button>`;

    // 페이지 번호 생성 로직 (안정성을 위해 재작성)
    const pages = [];
    if (totalPages <= maxVisiblePages) {
        for (let i = 1; i <= totalPages; i++) {
            pages.push(i);
        }
    } else {
        pages.push(1);
        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);

        if (currentPage <= 3) {
            start = 2;
            end = 4;
        } else if (currentPage >= totalPages - 2) {
            start = totalPages - 3;
            end = totalPages - 1;
        }

        if (start > 2) {
            pages.push('...');
        }

        for (let i = start; i <= end; i++) {
            pages.push(i);
        }

        if (end < totalPages - 1) {
            pages.push('...');
        }
        pages.push(totalPages);
    }

    pages.forEach(page => {
        if (page === '...') {
            html += `<span class="px-3 py-1 mx-1">...</span>`;
        } else {
            html += `<button class="px-3 py-1 mx-1 border rounded ${page === currentPage ? 'bg-blue-500 text-white' : 'bg-white hover:bg-gray-50'}" data-page="${page}">${page}</button>`;
        }
    });

    // 다음 & 마지막 버튼
    html += `<button class="px-3 py-1 mx-1 border rounded ${currentPage === totalPages ? 'bg-gray-200 text-gray-500 cursor-not-allowed' : 'bg-white hover:bg-gray-50'}" ${currentPage === totalPages ? 'disabled' : ''} id="${idPrefix}-nextPage">다음</button>`;
    if (totalPages > maxVisiblePages) {
        html += `<button class="px-3 py-1 mx-1 border rounded ${currentPage === totalPages ? 'bg-gray-200 text-gray-500 cursor-not-allowed' : 'bg-white hover:bg-gray-50'}" ${currentPage === totalPages ? 'disabled' : ''} id="${idPrefix}-lastPage">마지막</button>`;
    }

    state.paginationElement.innerHTML = html;

    // 렌더링된 버튼들에 이벤트 리스너 추가
    addPaginationEventListeners(id, totalPages);
}

/**
 * 페이징 컨트롤 버튼들에 클릭 이벤트를 바인딩합니다.
 * @param {string} id - 페이징 인스턴스의 고유 ID
 * @param {number} totalPages - 전체 페이지 수
 */
function addPaginationEventListeners(id, totalPages) {
    const state = paginationInstances.get(id);
    if (!state || !state.paginationElement) return;

    const idPrefix = state.paginationId;

    const firstPageButton = state.paginationElement.querySelector(`#${idPrefix}-firstPage`);
    if (firstPageButton) {
        firstPageButton.addEventListener('click', () => {
            if (state.currentPage > 1) {
                state.currentPage = 1;
                renderPage(id);
            }
        });
    }

    state.paginationElement.querySelector(`#${idPrefix}-prevPage`)?.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            renderPage(id);
        }
    });

    state.paginationElement.querySelector(`#${idPrefix}-nextPage`)?.addEventListener('click', () => {
        if (state.currentPage < totalPages) {
            state.currentPage++;
            renderPage(id);
        }
    });

    const lastPageButton = state.paginationElement.querySelector(`#${idPrefix}-lastPage`);
    if (lastPageButton) {
        lastPageButton.addEventListener('click', () => {
            if (state.currentPage < totalPages) {
                state.currentPage = totalPages;
                renderPage(id);
            }
        });
    }

    state.paginationElement.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', () => {
            state.currentPage = parseInt(btn.dataset.page);
            renderPage(id);
        });
    });
}

/**
 * 페이징 모듈을 초기화합니다.
 * @param {object} config - 설정 객체
 * @param {Array} config.fullData - 페이징할 전체 데이터
 * @param {number} [config.pageSize=5] - 한 페이지에 보여줄 아이템 수
 * @param {Function} config.renderTableCallback - 테이블을 렌더링할 콜백 함수
 * @param {string} config.paginationId - 페이징 컨트롤을 담을 요소의 ID
 * @param {string} config.pageSizeId - 페이지 크기 선택 요소의 ID
 * @param {string} config.searchId - 검색 입력 필드의 ID
 */
export function initPagination({
    fullData,
    pageSize = 5,
    renderTableCallback,
    paginationId,
    pageSizeId,
    searchId,
    totalCountId,
}) {
    const state = {
        currentPage: 1,
        pageSize: pageSize,
        totalItems: 0,
        // searchTerm, filteredData, searchElement는 더 이상 내부에서 관리하지 않음
        fullData: fullData || [],
        renderTableCallback: renderTableCallback,
        paginationId: paginationId,
        paginationElement: document.getElementById(paginationId),
        pageSizeElement: document.getElementById(pageSizeId),
        totalCountElement: totalCountId ? document.getElementById(totalCountId) : null,
    };

    paginationInstances.set(paginationId, state);

    // 페이지 크기 변경 이벤트 리스너
    if (state.pageSizeElement) {
        state.pageSizeElement.value = state.pageSize;
        // 기존 리스너 제거 (중복 방지)
        state.pageSizeElement.replaceWith(state.pageSizeElement.cloneNode(true));
        state.pageSizeElement = document.getElementById(pageSizeId); // 새 노드를 다시 참조
        state.pageSizeElement.addEventListener('change', (e) => {
            state.pageSize = parseInt(e.target.value);
            state.currentPage = 1;
            renderPage(paginationId);
        });
    }
    // 검색 이벤트 리스너는 각 페이지의 events.js에서 개별적으로 처리하므로 제거합니다.

    // 초기 렌더링
    renderPage(paginationId);
}

/**
 * 페이징 모듈의 데이터를 새 데이터로 업데이트합니다.
 * @param {string} id - 업데이트할 페이징 인스턴스의 고유 ID
 * @param {Array} newData - 새로운 전체 데이터 배열
 */
export function updatePaginationData(id, newData) {
    const state = paginationInstances.get(id);
    if (!state) {
        console.error(`Pagination instance with id "${id}" not found.`);
        return;
    }
    state.fullData = newData;
    state.currentPage = 1;
    // 검색어는 유지한 채로 데이터만 업데이트하고 다시 렌더링
    renderPage(id);
}
