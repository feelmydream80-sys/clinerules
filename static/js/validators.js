// @DOC_FILE: validators.js
// @DOC_DESC: 입력값 검증 함수 모음

/**
 * 이메일 검증 함수
 * @param {string} email - 검증할 이메일 주소
 * @returns {boolean} - 유효성 여부
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * 비밀번호 검증 함수
 * @param {string} password - 검증할 비밀번호
 * @returns {boolean} - 유효성 여부
 */
function isValidPassword(password) {
    // 최소 8자, 최소 하나의 문자와 하나의 숫자 포함
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/;
    return passwordRegex.test(password);
}

/**
 * 사용자 ID 검증 함수
 * @param {string} userId - 검증할 사용자 ID
 * @returns {boolean} - 유효성 여부
 */
function isValidUserId(userId) {
    // 4-20자 영문, 숫자, 언더스코어만 허용
    const userIdRegex = /^[a-zA-Z0-9_]{4,20}$/;
    return userIdRegex.test(userId);
}

/**
 * 전화번호 검증 함수
 * @param {string} phone - 검증할 전화번호
 * @returns {boolean} - 유효성 여부
 */
function isValidPhone(phone) {
    // 한국식 전화번호 형식 (010-1234-5678 또는 02-1234-5678)
    const phoneRegex = /^0\d{1,2}-\d{3,4}-\d{4}$/;
    return phoneRegex.test(phone);
}

/**
 * 숫자 검증 함수
 * @param {any} value - 검증할 값
 * @returns {boolean} - 유효성 여부
 */
function isValidNumber(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}

export { 
    isValidEmail, 
    isValidPassword, 
    isValidUserId, 
    isValidPhone, 
    isValidNumber 
};