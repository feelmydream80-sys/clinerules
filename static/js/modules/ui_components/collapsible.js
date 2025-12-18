// static/js/modules/ui_components/collapsible.js

/**
 * @module collapsible
 * @description 접기/펴기 UI 컴포넌트의 모든 기능을 관리하는 모듈.
 * - 개별 카드 제어, 전체 제어(펼치기/접기) 기능을 제공합니다.
 * - `localStorage`를 사용하여 상태를 영구적으로 저장합니다.
 */

/**
 * @description 개별 접기/펴기 카드에 이벤트 리스너를 설정합니다.
 * @private
 */
function initializeIndividualCards() {
    const cards = document.querySelectorAll('.collapsible-card');
    cards.forEach(initSingleCollapsibleCard);
}

/**
 * @description 특정 카드의 접기/펴기 상태를 토글하고 저장합니다.
 * @param {HTMLElement} card - 상태를 변경할 카드 요소.
 */
function toggleCardState(card) {
    const content = card.querySelector('.card-content');
    const icon = card.querySelector('.card-header span');
    if (content) {
        const isCollapsed = content.classList.toggle('hidden');
        if (card.id) {
            localStorage.setItem(card.id, isCollapsed);
        }
        if (icon) {
            icon.classList.toggle('rotate-180', isCollapsed);
        }
        
        // Dispatch a custom event to notify other modules of the state change.
        const event = new CustomEvent('cardToggled', {
            bubbles: true,
            detail: { card, isCollapsed }
        });
        card.dispatchEvent(event);
    }
}


/**
 * @description 페이지의 모든 카드를 펼칩니다.
 */
function expandAllCards() {
    const cards = document.querySelectorAll('.collapsible-card');
    cards.forEach(card => {
        const content = card.querySelector('.card-content');
        if (content && content.classList.contains('hidden')) {
            toggleCardState(card);
        }
    });
}

/**
 * @description 페이지의 모든 카드를 접습니다.
 */
function collapseAllCards() {
    const cards = document.querySelectorAll('.collapsible-card');
    cards.forEach(card => {
        const content = card.querySelector('.card-content');
        if (content && !content.classList.contains('hidden')) {
            toggleCardState(card);
        }
    });
}

/**
 * @description '모두 펼치기/접기' 버튼에 이벤트 리스너를 설정합니다.
 * @private
 */
function initializeGlobalControls() {
    const expandAllBtn = document.getElementById('expandAllBtn');
    const collapseAllBtn = document.getElementById('collapseAllBtn');

    if (expandAllBtn) {
        expandAllBtn.addEventListener('click', expandAllCards);
    }
    if (collapseAllBtn) {
        collapseAllBtn.addEventListener('click', collapseAllCards);
    }
}

/**
 * @description 접기/펴기 기능과 관련된 모든 UI 요소를 초기화하는 메인 함수.
 *              이 함수만 호출하면 모든 기능이 활성화됩니다.
 */
/**
 * @description 특정 카드의 접기/펴기 상태를 적용하고 이벤트 리스너를 설정합니다.
 * @param {HTMLElement} card - 초기화할 카드 요소.
 */
export function initSingleCollapsibleCard(card) {
    if (!card) return;

    // 1. 저장된 상태 적용
    if (card.id) {
        const isCollapsed = localStorage.getItem(card.id) === 'true';
        const content = card.querySelector('.card-content');
        const icon = card.querySelector('.card-header span');
        if (content) {
            content.classList.toggle('hidden', isCollapsed);
            if (icon) {
                icon.classList.toggle('rotate-180', isCollapsed);
            }
        }
    }

    // 2. 이벤트 리스너 설정
    const header = card.querySelector('.card-header');
    if (header && !header.dataset.collapsibleInitialized) {
        header.addEventListener('click', () => {
            toggleCardState(card);
        });
        header.dataset.collapsibleInitialized = 'true';
    }
}

/**
 * @description 접기/펴기 기능과 관련된 모든 UI 요소를 초기화하는 메인 함수.
 *              이 함수만 호출하면 모든 기능이 활성화됩니다.
 */
export function initCollapsibleFeatures() {
    initializeIndividualCards();
    initializeGlobalControls();
}
