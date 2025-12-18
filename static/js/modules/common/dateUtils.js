/**
 * 날짜를 YYYY-MM-DD 형식의 문자열로 변환합니다.
 * @param {Date} date - 변환할 Date 객체
 * @returns {string} YYYY-MM-DD 형식의 날짜 문자열
 */
export function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * 지정된 일수 이전부터 오늘까지의 날짜 범위를 가져옵니다.
 * @param {number} daysAgo - 오늘로부터 며칠 전을 시작일로 할지 지정합니다.
 * @returns {{startDate: string, endDate: string}} 시작일과 종료일(오늘)
 */
export function getDateRange(daysAgo) {
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(today.getDate() - daysAgo);

    return {
        startDate: formatDate(startDate),
        endDate: formatDate(today)
    };
}


/**
 * 기본 날짜 범위를 가져옵니다.
 * @returns {{startDateValue: string, todayDate: string}} 2024년 2월 1일부터 오늘 날짜
 */
export function getDefaultDateRange() {
    const today = new Date();

    // 시작 날짜를 2024년 2월 7일로 설정 (일주일 더 뒤로)
    const startDate = new Date(2024, 1, 7); // 2월은 1, 7일

    const todayDate = formatDate(today);
    const startDateValue = formatDate(startDate);

    return { startDateValue, todayDate };
}

/**
 * 페이지의 날짜 입력 필드에 기본값을 설정합니다.
 * 'start-date'와 'end-date' ID를 가진 요소를 찾아 값을 설정합니다.
 */
export function setDefaultDates() {
    const { startDateValue, todayDate } = getDefaultDateRange();

    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    if (startDateInput) {
        startDateInput.value = startDateValue;
    }
    if (endDateInput) {
        endDateInput.value = todayDate;
    }
}

/**
 * 페이지의 날짜 입력 필드에 '올해 1월 1일'부터 '오늘'까지의 값을 설정합니다.
 * 'start-date'와 'end-date' ID를 가진 요소를 찾아 값을 설정합니다.
 */
export function setYearToDate() {
    const today = new Date();
    const year = today.getFullYear();
    const startDate = new Date(year, 0, 1); // January is month 0

    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    if (startDateInput) {
        startDateInput.value = formatDate(startDate);
    }
    if (endDateInput) {
        endDateInput.value = formatDate(today);
    }
}
