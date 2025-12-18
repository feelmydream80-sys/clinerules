// 파일명: static/js/modules/mngr_sett/adminUtils.js
// 주요 역할: 관리자 설정 페이지에서만 사용되는 유틸리티 함수들을 정의합니다.

/**
 * 관리자 설정 페이지의 차트 색상이 지정되지 않았을 때 사용할 랜덤 색상을 생성합니다.
 * @returns {string} 16진수 색상 코드 (예: '#RRGGBB')
 */
export function getRandomColorForAdmin() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
