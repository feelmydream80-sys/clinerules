// static/js/modules/data_spec/api.js

/**
 * @module api
 * @description 데이터 명세 페이지의 모든 API 통신을 담당합니다.
 * 
 * @example
 * import * as api from './api.js';
 * 
 * const specs = await api.getSpecs();
 * await api.saveSpec(specData);
 */

/**
 * @description 데이터 명칭 중복을 확인합니다.
 * @param {string} name - 확인할 데이터 명칭
 * @param {string|null} id - 기존 명세 ID (수정 시)
 * @returns {Promise<Object>} 중복 여부
 */
export async function checkName(name, id) {
    const url = `/api/data-spec/check-name?data_name=${encodeURIComponent(name)}&spec_id=${id || ''}`;
    const response = await fetch(url);
    return response.json();
}

/**
 * @description URL에서 명세 정보를 스크래핑합니다.
 * @param {string} url - 스크래핑할 URL
 * @returns {Promise<Object>} 스크래핑된 데이터
 */
export async function scrapeSpec(url) {
    const response = await fetch('/api/scrape-spec', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Scraping failed');
    }
    return response.json();
}

/**
 * @description 모든 데이터 명세 목록을 가져옵니다.
 * @returns {Promise<Array>} 명세 목록
 */
export async function getSpecs() {
    const response = await fetch('/api/data-spec');
    return response.json();
}

/**
 * @description ID로 특정 데이터 명세를 가져옵니다.
 * @param {string} id - 명세 ID
 * @returns {Promise<Object>} 명세 데이터
 */
export async function getSpecById(id) {
    const response = await fetch(`/api/data-spec/${id}`);
    return response.json();
}

/**
 * @description 데이터 명세를 저장(생성 또는 수정)합니다.
 * @param {string|null} id - 명세 ID (수정 시)
 * @param {Object} specData - 저장할 명세 데이터
 * @returns {Promise<Object>} 저장 결과
 */
export async function saveSpec(id, specData) {
    const url = id ? `/api/data-spec/${id}` : '/api/data-spec';
    const method = id ? 'PUT' : 'POST';

    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(specData),
    });

    if (!response.ok) {
        const errorText = await response.text();
        try {
            const errorJson = JSON.parse(errorText);
            throw new Error(errorJson.message || 'Save failed');
        } catch (e) {
            throw new Error(errorText || 'Save failed');
        }
    }
    return response.json();
}

/**
 * @description 데이터 명세를 삭제합니다.
 * @param {string} id - 삭제할 명세 ID
 * @param {string|null} password - 비밀번호 (필요 시)
 * @returns {Promise<Object>} 삭제 결과
 */
export async function deleteSpec(id, password) {
    const payload = password !== null ? { password: password } : {};
    const response = await fetch(`/api/data-spec/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Delete failed');
    }
    return response.json();
}
