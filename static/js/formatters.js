// @DOC_FILE: formatters.js
// @DOC_DESC: 데이터 포맷팅 함수 모음

/**
 * 숫자 포맷팅 함수
 * @param {number} number - 포맷팅할 숫자
 * @param {number} decimals - 소수점 자릿수
 * @returns {string} - 포맷팅된 숫자 문자열
 */
function formatNumber(number, decimals = 0) {
    if (typeof number !== 'number' || isNaN(number)) {
        return '0';
    }
    
    return number.toLocaleString('ko-KR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

/**
 * 날짜 포맷팅 함수
 * @param {string|Date} date - 포맷팅할 날짜
 * @param {string} format - 포맷 형식
 * @returns {string} - 포맷팅된 날짜 문자열
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    let d = new Date(date);
    
    if (isNaN(d.getTime())) {
        return 'Invalid Date';
    }
    
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 백분율 포맷팅 함수
 * @param {number} value - 포맷팅할 값
 * @param {number} decimals - 소수점 자릿수
 * @returns {string} - 포맷팅된 백분율 문자열
 */
function formatPercentage(value, decimals = 2) {
    if (typeof value !== 'number' || isNaN(value)) {
        return '0%';
    }
    
    return (value * 100).toFixed(decimals) + '%';
}

/**
 * 파일 크기 포맷팅 함수
 * @param {number} bytes - 바이트 크기
 * @param {number} decimals - 소수점 자릿수
 * @returns {string} - 포맷팅된 파일 크기 문자열
 */
function formatFileSize(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export { 
    formatNumber, 
    formatDate, 
    formatPercentage, 
    formatFileSize 
};