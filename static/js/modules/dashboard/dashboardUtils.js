// 파일명: static/js/modules/dashboardUtils.js
// 주요 역할: 대시보드 페이지에 특화된 유틸리티 함수들을 정의합니다.

// 아이콘 매핑 (Job ID별 관리자 설정에서 가져온 icon_id를 실제 이모지로 변환)
let currentIconMap = {}; // icon_id -> icon_code (이모지)

/**
 * 전역 아이콘 맵을 설정합니다.
 * @param {Object} iconMap - icon_id를 icon_code(이모지)로 매핑하는 객체
 */
export function setDashboardIconMap(iconMap) {
    currentIconMap = iconMap;
}

/**
 * 성공률에 따라 스타일링된 HTML을 반환합니다.
 * @param {number} successRate - 성공률 (0-100)
 * @param {number} successCount - 성공 건수
 * @param {number} totalCount - 총 수집 건수
 * @param {number} failCount - 실패 건수
 * @param {number} noDataCount - 미수집 건수
 * @param {Object} adminSetting - 해당 Job ID의 관리자 설정
 * @param {string} thresholdType - (더 이상 상태 판단에 직접 사용되지 않음)
 * @param {number} failStreak - 연속 실패 횟수 (상태 판단에 직접 사용되지 않음, 표시용)
 * @returns {string} 스타일링된 HTML 문자열
 */
export function getStyledSuccessRateHtml(successRate, successCount, totalCount, failCount, noDataCount, adminSetting, thresholdType, failStreak) {
    // 프로그램 수정 사유:
    // 1. 셀 내부에 ℹ️ 아이콘 제거 (사용자 지시)
    // 2. 셀 내부에 실패 수량, 미수집 수량 직접 표시 (사용자 지시)
    // 3. 아이콘과 모든 상세 정보는 툴팁 내부에만 표시 (사용자 지시)
    // 4. 성공률 셀에 상태 아이콘을 직접 포함 (사용자 지시)
    // 5. 상태 판단 로직 전면 수정 (사용자 지시: CD901, CD902, CD903은 데이터 수집 결과에 따라 할당)
    //    - 연속 실패(failStreak, cf_fail_cnt, cf_warning_cnt)는 CDxxx 상태 코드 할당에 사용되지 않음.
    //    - CD901: 데이터 수집 성공 (totalCount > 0 && failCount === 0)
    //    - CD902: 데이터 수집 실패 (failCount > 0)
    //    - CD903: 데이터 미존재 (totalCount === 0)

    let icon;
    let color;
    let statusName;
    let statusCode;

    // 상태 판단 로직 (사용자 지시: 데이터 수집 결과에 따라 CD901, CD902, CD903 할당)
    if (totalCount === 0) {
        statusCode = 'CD903'; // 미존재 (원천에 데이터 없음)
    } else if (failCount > 0) { // 실패 건수가 0보다 크면 장애로 간주
        statusCode = 'CD902'; // 장애 (데이터 요청 실패)
    } else {
        statusCode = 'CD901'; // 정상 (데이터 요청 성공 및 수집 완료)
    }
   
    // 최종 상태 코드에 따른 아이콘, 색상, 이름 가져오기
    // getStatusInfo는 adminSetting이 null일 경우를 대비하여 기본값을 반환하도록 되어 있음.
    const statusInfo = getStatusInfo(statusCode, adminSetting);
    icon = statusInfo.icon;
    color = statusInfo.color;
    statusName = statusInfo.statusName;

    // 툴팁에 표시될 전체 내용 구성 (아이콘, 상태 이름, 상세 통계)
    let tooltipFullContent = `${icon} ${statusName}: 성공률: ${successRate.toFixed(2)}%<br>성공: ${successCount}건, 실패: ${failCount}건, 미수집: ${noDataCount}건 (총: ${totalCount}건)`;
    if (failStreak > 0) {
        tooltipFullContent += `<br>연속 실패: ${failStreak}회`;
    }

    // 최종 HTML 반환: 셀 내부에 아이콘, 성공률, 실패/미수집 건수 표시
    // 툴팁은 전체 셀에 마우스 오버 시 나타나도록 div.tooltip으로 감쌈
    return `
        <div class="tooltip">
            <span class="status-icon" style="color: ${color};">${icon}</span>
            <span class="status-text" style="color: ${color};">${successRate.toFixed(2)}%</span>
            <br>
            <span class="text-sm text-gray-500">(실패: ${failCount}회, 미존재: ${noDataCount}회)</span>
            <span class="tooltiptext">${tooltipFullContent}</span>
        </div>
    `;
}

/**
 * Job ID별 연속 실패 횟수 배지를 생성합니다.
 * @param {number} failStreak - 연속 실패 횟수
 * @param {Object} adminSetting - 해당 Job ID의 관리자 설정
 * @returns {string} 연속 실패 배지 HTML 문자열
 */
export function getFailStreakBadgeHtml(failStreak, adminSetting) {
    // 프로그램 수정 사유:
    // 이 함수는 더 이상 사용되지 않음. (Job ID 셀에 연속 실패 횟수를 포함시키기 위해)
    // 하지만 다른 곳에서 사용될 가능성을 고려하여 유지.
    if (failStreak <= 0) return '';

    let badgeColorClass = 'bg-gray-500'; // 기본값
    if (adminSetting) {
        const cfFailCnt = adminSetting.cf_fail_cnt || 0;
        const cfWarningCnt = adminSetting.cf_warning_cnt || 0;

        if (cfFailCnt > 0 && failStreak >= cfFailCnt) {
            badgeColorClass = 'bg-red-500'; // 장애 임계치 도달
        } else if (cfWarningCnt > 0 && failStreak >= cfWarningCnt) {
            badgeColorClass = 'bg-orange-500'; // 경고 임계치 도달
        }
    }
    return `<span class="inline-block px-2 py-1 ml-2 text-xs font-bold text-white rounded-full ${badgeColorClass}">연속 실패: ${failStreak}</span>`;
}

/**
 * Job ID별 상태 아이콘 및 색상 정보를 반환합니다.
 * 이 함수는 내부적으로 currentIconMap을 사용하여 icon_id를 실제 이모지로 변환합니다.
 * @param {string} statusCode - 상태 코드 (예: 'CD901', 'CD902')
 * @param {Object} adminSettings - 해당 Job ID의 관리자 설정 객체
 * @returns {Object} { icon: string, color: string, statusName: string }
 */
export function getStatusInfo(statusCode, adminSettings) {
    let icon;
    let color;
    let statusName;

    // adminSettings가 없거나 유효하지 않을 경우 기본값 사용
    if (!adminSettings) {
        switch (statusCode) {
            case 'CD901': statusName = '정상'; icon = '🟢'; color = '#28a745'; break;
            case 'CD902': statusName = '장애'; icon = '🔴'; color = '#dc3545'; break;
            case 'CD903': statusName = '미존재'; icon = '⚪'; color = '#6c757d'; break; // CD903을 '미존재'로 변경
            default: statusName = '확인필요'; icon = '⚫'; color = '#343a40'; break; // 알 수 없는 상태 코드에 대한 기본값
        }
        return { icon, color, statusName };
    }

    // adminSettings가 유효할 경우, tb_admin_settings 및 tb_icon 데이터 사용 시도
    switch (statusCode) {
        case 'CD901': // 정상
            icon = currentIconMap[adminSettings.cf_success_icon] || '🟢';
            color = adminSettings.cf_success_wd_color || '#28a745';
            statusName = '정상';
            break;
        case 'CD902': // 장애
            icon = currentIconMap[adminSettings.cf_fail_icon] || '🔴';
            color = adminSettings.cf_fail_wd_color || '#dc3545';
            statusName = '장애';
            break;
        case 'CD903': // 미존재 (CD903을 '미존재'로 변경)
            icon = '⚪'; // 미존재 아이콘 (관리자 설정에 없음, 고정)
            color = '#6c757d'; // 미존재 색상 (고정)
            statusName = '미존재';
            break;
        default:
            // 알 수 없는 상태 코드에 대한 기본값 (이 로직에서는 도달하지 않아야 함)
            icon = '⚫';
            color = '#343a40';
            statusName = '확인필요';
            break;
    }
    return { icon, color, statusName };
}