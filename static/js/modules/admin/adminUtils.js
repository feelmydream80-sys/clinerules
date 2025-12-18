// 파일명: static/js/modules/adminUtils.js
// 주요 역할: 관리자 설정 페이지에 특화된 유틸리티 함수들을 정의합니다.

const adminUsedColors = new Set();
const adminPredefinedColors = [
    '#A3E4D7', '#FADBD8', '#D7BDE2', '#A9CCE3', '#A2D9CE',
    '#F5CBA7', '#D2B4DE', '#AED6F1', '#A9DFBF', '#F9E79F'
];
let adminColorIndex = 0;

/**
 * 관리자 페이지에서 Job ID별 차트 색상으로 사용될 랜덤 색상을 생성합니다.
 * 미리 정의된 색상을 우선 사용하고, 모두 사용하면 무작위 색상을 생성합니다.
 * @returns {string} 헥사 코드 색상 문자열 (예: '#RRGGBB')
 */
export function getRandomColorForAdmin() {
    if (adminColorIndex < adminPredefinedColors.length) {
        const color = adminPredefinedColors[adminColorIndex];
        adminUsedColors.add(color);
        adminColorIndex++;
        return color;
    }
    // 모든 미리 정의된 색상을 사용한 경우, 랜덤 색상 생성 (충돌 방지 로직 포함)
    let color;
    do {
        color = '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
    } while (adminUsedColors.has(color));
    adminUsedColors.add(color);
    return color;
}
