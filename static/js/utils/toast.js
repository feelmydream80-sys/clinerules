// static/js/utils/toast.js

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
 * 토스트 알림을 화면에 표시합니다.
 * @param {string} message - 표시할 메시지
 * @param {string} [category='info'] - 메시지 종류 ('success', 'warning', 'error', 'info')
 * @param {number} [duration=5000] - 메시지가 표시될 시간 (ms)
 */
export function showToast(message, category = 'info', duration = 5000) {
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
    }, duration);
}

/**
 * HTML에 포함된 flash 메시지를 읽어 토스트로 표시합니다.
 */
function initializeFlashedMessages() {
    const flashMessagesElement = document.getElementById('flash-messages-data');
    if (flashMessagesElement) {
        try {
            const messages = JSON.parse(flashMessagesElement.textContent || '[]');
            messages.forEach(msg => {
                // category: msg[0], message: msg[1]
                showToast(msg[1], msg[0]);
            });
        } catch (error) {
            console.error('Flash 메시지를 파싱하는 중 오류 발생:', error);
        }
    }
}

// DOM 로드 후 flash 메시지 표시 함수 실행
document.addEventListener('DOMContentLoaded', initializeFlashedMessages);

// 전역에서 접근 가능하도록 window에 할당
window.showToast = showToast;

