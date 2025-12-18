// static/js/modules/common/api/analytics.js
import { showMessage } from '../utils.js';
import { updateApiStatus } from './client.js';

const BASE_URL = '';

/**
 * @AI_NOTE: [기존 기능 유지] 기간별 Job ID별 수집 성공률 추이 데이터를 가져옵니다.
 * @param {string} startDate - 조회 시작 날짜 (YYYY-MM-DD)
 * @param {string} endDate - 조회 종료 날짜 (YYYY-MM-DD)
 * @param {Array<string>} jobIds - 선택된 Job ID 배열
 * @returns {Promise<Array<Object>>} 성공률 추이 데이터 배열
 */
export async function fetchSuccessRateTrendByJob(startDate, endDate, jobIds) {
    const apiName = "successRateTrendFetch";
    updateApiStatus(apiName, "apiCallAttempted", true);
    updateApiStatus(apiName, "apiCallSuccess", false);
    updateApiStatus(apiName, "apiResponseCount", 0);
    updateApiStatus(apiName, "error", null);

    try {
        const params = new URLSearchParams({ start_date: startDate, end_date: endDate });
        (jobIds || []).filter(id => id).forEach(id => params.append('job_ids', id));
        const url = `${BASE_URL}/api/success_rate_trend?${params.toString()}`;
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        showMessage('수집 성공률 데이터 로드 성공.', 'success');
        updateApiStatus(apiName, "apiCallSuccess", true);
        updateApiStatus(apiName, "apiResponseCount", data.length);
        return data;
    } catch (error) {
        console.error("수집 성공률 데이터 로드 실패:", error);
        showMessage('수집 성공률 데이터 로드 실패: ' + error.message, 'error');
        updateApiStatus(apiName, "error", error.message);
        throw error;
    }
}

/**
 * @AI_NOTE: [기존 기능 유지] 장애 코드별 시간대별 데이터를 가져옵니다.
 * @param {string} startDate - 조회 시작 날짜 (YYYY-MM-DD)
 * @param {string} endDate - 조회 종료 날짜 (YYYY-MM-DD)
 * @param {Array<string>} jobIds - 선택된 Job ID 배열
 * @returns {Promise<Array<Object>>} 장애 데이터 배열
 */
export async function fetchTroubleHourlyByStatusData(startDate, endDate, jobIds) {
    const apiName = "troubleDataFetch";
    updateApiStatus(apiName, "apiCallAttempted", true);
    updateApiStatus(apiName, "apiCallSuccess", false);
    updateApiStatus(apiName, "apiResponseCount", 0);
    updateApiStatus(apiName, "error", null);

    try {
        const params = new URLSearchParams({ start_date: startDate, end_date: endDate });
        (jobIds || []).filter(id => id).forEach(id => params.append('job_ids', id));
        const url = `${BASE_URL}/api/trouble/hourly/by-status?${params.toString()}`;
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        showMessage('장애 코드 데이터 로드 성공.', 'success');
        updateApiStatus(apiName, "apiCallSuccess", true);
        updateApiStatus(apiName, "apiResponseCount", data.length);
        return data;
    } catch (error) {
        console.error("장애 코드 데이터 로드 실패:", error);
        showMessage('장애 코드 데이터 로드 실패: ' + error.message, 'error');
        updateApiStatus(apiName, "error", error.message);
        throw error;
    }
}

/**
 * @AI_NOTE: [신규 기능] 분석 차트용 기간별 수집 성공률 추이 데이터를 가져옵니다.
 * @param {string} startDate - 조회 시작 날짜 (YYYY-MM-DD)
 * @param {string} endDate - 조회 종료 날짜 (YYYY-MM-DD)
 * @param {Array<string>} jobIds - 선택된 Job ID 배열
 * @returns {Promise<Array<Object>>} 성공률 추이 데이터 배열
 */
export async function fetchAnalyticsSuccessRateTrend(startDate, endDate, jobIds) {
    const apiName = "analyticsSuccessRateTrendFetch";
    updateApiStatus(apiName, "apiCallAttempted", true);
    updateApiStatus(apiName, "apiCallSuccess", false);
    updateApiStatus(apiName, "apiResponseCount", 0);
    updateApiStatus(apiName, "error", null);

    try {
        const params = new URLSearchParams({ start_date: startDate, end_date: endDate });
        (jobIds || []).filter(id => id).forEach(id => params.append('job_ids', id));
        const url = `${BASE_URL}/api/analytics/success_rate_trend?${params.toString()}`;
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        showMessage('분석 수집 성공률 데이터 로드 성공.', 'success');
        updateApiStatus(apiName, "apiCallSuccess", true);
        updateApiStatus(apiName, "apiResponseCount", data.length);
        return data;
    } catch (error) {
        console.error("분석 수집 성공률 데이터 로드 실패:", error);
        showMessage('분석 수집 성공률 데이터 로드 실패: ' + error.message, 'error');
        updateApiStatus(apiName, "error", error.message);
        throw error;
    }
}

/**
 * @AI_NOTE: [신규 기능] 분석 차트용 장애 코드별 비율 데이터를 가져옵니다.
 * @param {string} startDate - 조회 시작 날짜 (YYYY-MM-DD)
 * @param {string} endDate - 조회 종료 날짜 (YYYY-MM-DD)
 * @param {Array<string>} jobIds - 선택된 Job ID 배열
 * @returns {Promise<Array<Object>>} 장애 데이터 배열
 */
export async function fetchAnalyticsTroubleByCode(startDate, endDate, jobIds) {
    const apiName = "analyticsTroubleDataFetch";
    updateApiStatus(apiName, "apiCallAttempted", true);
    updateApiStatus(apiName, "apiCallSuccess", false);
    updateApiStatus(apiName, "apiResponseCount", 0);
    updateApiStatus(apiName, "error", null);

    try {
        const params = new URLSearchParams({ start_date: startDate, end_date: endDate });
        (jobIds || []).filter(id => id).forEach(id => params.append('job_ids', id));
        const url = `${BASE_URL}/api/analytics/trouble_by_code?${params.toString()}`;
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        showMessage('분석 장애 코드 데이터 로드 성공.', 'success');
        updateApiStatus(apiName, "apiCallSuccess", true);
        updateApiStatus(apiName, "apiResponseCount", data.length);
        return data;
    } catch (error) {
        console.error("분석 장애 코드 데이터 로드 실패:", error);
        showMessage('분석 장애 코드 데이터 로드 실패: ' + error.message, 'error');
        updateApiStatus(apiName, "error", error.message);
        throw error;
    }
}
