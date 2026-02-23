// 파일명: static/js/modules/utils.js
// 주요 역할: 유틸리티 함수들을 정의합니다.

/**
 * 사용자에게 메시지를 표시합니다.
 * @param {string} message - 표시할 메시지 텍스트
 * @param {string} type - 메시지 유형 ('info', 'success', 'error', '기본값: info')
 */
export function showMessage(message, type = 'info') {
    /*
    const container = document.createElement('div');
    container.className = `fixed top-20 left-1/2 -translate-x-1/2 p-4 rounded-lg shadow-lg text-white z-50 transition-opacity duration-300`;

    const typeClasses = {
        info: 'bg-blue-500',
        success: 'bg-green-500',
        error: 'bg-red-500'
    };

    container.classList.add(typeClasses[type] || typeClasses.info);
    container.textContent = message;

    document.body.appendChild(container);

    setTimeout(() => {
        container.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(container);
        }, 300);
    }, 3000);
    */
}

/**
 * 사용자에게 확인/취소 대화 상자를 표시합니다.
 * @param {string} message - 표시할 확인 메시지 텍스트
 * @param {Function} onConfirm - 사용자가 '확인'을 클릭했을 때 실행될 콜백 함수
 * @param {Function} [onCancel] - 사용자가 '취소'를 클릭했을 때 실행될 콜백 함수 (선택 사항)
 */
export function showConfirm(message, onConfirm, onCancel = () => {}) {
    const confirmOverlay = document.createElement('div');
    confirmOverlay.id = 'confirmOverlay';
    confirmOverlay.className = 'fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50';
    confirmOverlay.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-lg flex flex-col items-center max-w-sm mx-auto">
            <p class="text-gray-700 text-lg mb-4 text-center">${message}</p>
            <div class="flex space-x-4">
                <button id="confirmBtn" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition duration-300">확인</button>
                <button id="cancelBtn" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-md transition duration-300">취소</button>
            </div>
        </div>
    `;

    document.body.appendChild(confirmOverlay);

    document.getElementById('confirmBtn').addEventListener('click', () => {
        onConfirm();
        document.body.removeChild(confirmOverlay);
    });

    document.getElementById('cancelBtn').addEventListener('click', () => {
        onCancel();
        document.body.removeChild(confirmOverlay);
    });
}

export function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function isIntervalPattern(value, unit) {
    if (!value.startsWith('*/')) return null;
    const interval = parseInt(value.substring(2));
    if (isNaN(interval)) return null;
    
    const unitMap = {
        'minute': '분',
        'hour': '시간',
        'day': '일',
        'month': '개월',
        'dow': '주' // day of week
    };
    
    return `${interval}${unitMap[unit]}마다`;
}

export function parseCronExpression(cronExpression) {
    if (!cronExpression || cronExpression.trim() === '') {
        return '설정 없음';
    }
    
    const parts = cronExpression.trim().split(' ');
    if (parts.length < 5) {
        return '잘못된 형식';
    }
    
    const [minute, hour, dayOfMonth, month, dayOfWeek] = parts;
    
    // 주기적 실행 패턴 확인
    const minuteInterval = isIntervalPattern(minute, 'minute');
    const hourInterval = isIntervalPattern(hour, 'hour');
    const dayInterval = isIntervalPattern(dayOfMonth, 'day');
    const monthInterval = isIntervalPattern(month, 'month');
    const weekInterval = isIntervalPattern(dayOfWeek, 'dow');
    
    // 분 단위 주기 실행 (예: */5 * * * * → 5분마다)
    if (minuteInterval && hour === '*' && dayOfMonth === '*' && month === '*' && dayOfWeek === '*') {
        return `${minuteInterval} 실행`;
    }
    
    // 시간 단위 주기 실행 (예: 0 */3 * * * → 3시간마다)
    if (minute !== '*' && hourInterval && dayOfMonth === '*' && month === '*' && dayOfWeek === '*') {
        return `${hourInterval} ${minute}분에 실행`;
    }
    
    // 일 단위 주기 실행 (예: 0 0 */5 * * → 5일마다)
    if (minute !== '*' && hour !== '*' && dayInterval && month === '*' && dayOfWeek === '*') {
        return `${dayInterval} ${hour}시 ${minute}분에 실행`;
    }
    
    // 주 단위 주기 실행 (예: 0 0 * * 0 → 매주 일요일)
    if (minute !== '*' && hour !== '*' && dayOfMonth === '*' && month === '*' && weekInterval) {
        return `${weekInterval} ${hour}시 ${minute}분에 실행`;
    }
    
    // 매일 실행 (기본 케이스)
    if (dayOfMonth === '*' && dayOfWeek === '*') {
        if (hour === '*' && minute === '*') {
            return '매분 실행';
        } else if (hour === '*' && minute !== '*') {
            return `매시간 ${minute}분에 실행`;
        } else if (hour !== '*' && minute === '*') {
            return `매일 ${hour}시에 실행`;
        } else {
            return `매일 ${hour}시 ${minute}분에 실행`;
        }
    }
    
    // 특정 요일 실행
    if (dayOfWeek !== '*') {
        const weekdays = ['일', '월', '화', '수', '목', '금', '토'];
        if (dayOfWeek.includes(',')) {
            const days = dayOfWeek.split(',').map(d => weekdays[parseInt(d)]).join(', ');
            return `매주 ${days}요일에 실행`;
        } else if (dayOfWeek.includes('-')) {
            const [start, end] = dayOfWeek.split('-');
            const startDay = weekdays[parseInt(start)];
            const endDay = weekdays[parseInt(end)];
            return `매주 ${startDay}~${endDay}요일에 실행`;
        } else {
            const day = weekdays[parseInt(dayOfWeek)];
            return `매주 ${day}요일에 실행`;
        }
    }
    
    // 특정 날짜 실행
    if (dayOfMonth !== '*') {
        if (dayOfMonth === '*/6') {
            return '6일마다 실행';
        } else if (dayOfMonth.startsWith('*/') && !isNaN(dayOfMonth.substring(2))) {
            const days = dayOfMonth.substring(2);
            return `${days}일마다 실행`;
        } else if (dayOfMonth.includes(',')) {
            const days = dayOfMonth.split(',').join(', ');
            return `매월 ${days}일에 실행`;
        } else if (dayOfMonth.includes('-')) {
            const [start, end] = dayOfMonth.split('-');
            return `매월 ${start}~${end}일에 실행`;
        } else {
            return `매월 ${dayOfMonth}일에 실행`;
        }
    }
    
    // 특정 월 실행
    if (month !== '*') {
        const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
        if (month.includes(',')) {
            const monthList = month.split(',').map(m => months[parseInt(m)-1]).join(', ');
            return `${monthList}에 실행`;
        } else {
            return `${months[parseInt(month)-1]}에 실행`;
        }
    }
    
    return '정기 실행';
}

/**
 * 숫자에 천 단위 콤마를 추가하여 문자열로 반환합니다.
 * @param {number | string} number - 포맷할 숫자 또는 숫자 형식의 문자열
 * @returns {string} 천 단위 콤마가 추가된 문자열
 */
export function formatNumberWithCommas(number) {
    if (number === null || number === undefined) return '';
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * 숫자를 만, 억 단위로 축약하여 표시하고, 툴팁으로 전체 숫자를 보여줍니다.
 * @param {number} num - 변환할 숫자
 * @returns {string} 포맷된 HTML 문자열
 */
export function formatNumberToKorean(num) {
    if (typeof num !== 'number' || isNaN(num)) {
        return '0';
    }

    const fullNumber = num.toLocaleString();
    let formattedNumber;

    if (num >= 100000000) {
        formattedNumber = `${(num / 100000000).toFixed(1).replace(/\.0$/, '')}억`;
    } else if (num >= 10000) {
        formattedNumber = `${(num / 10000).toFixed(1).replace(/\.0$/, '')}만`;
    } else {
        formattedNumber = fullNumber;
    }
    
    return `<span title="${fullNumber}">${formattedNumber}</span>`;
}

/**
 * 숫자를 '만' 단위 이상의 한국어 서식으로 변환합니다.
 * @param {number} number - 변환할 숫자
 * @returns {string} 포맷팅된 문자열
 */
export function formatNumberWithKoreanUnits(number) {
    if (isNaN(number)) return '0';

    if (number >= 100000000) {
        const eok = Math.floor(number / 100000000);
        const man = Math.floor((number % 100000000) / 10000);
        if (man > 0) {
            return `${eok.toLocaleString()}억 ${man.toLocaleString()}만`;
        }
        return `${eok.toLocaleString()}억`;
    }
    
    if (number >= 10000) {
        const man = Math.floor(number / 10000);
        return `${man.toLocaleString()}만`;
    }
    return number.toLocaleString();
}

/**
 * tb_con_mst 데이터에서 use_yn === 'Y'인 항목만 필터링합니다.
 * @param {Array} data - tb_con_mst 데이터 배열
 * @returns {Array} use_yn === 'Y'인 데이터 배열
 */
export function filterActiveMstData(data) {
    if (!Array.isArray(data)) {
        console.warn('filterActiveMstData: Input is not an array');
        return [];
    }
    
    const activeData = data.filter(item => {
        // use_yn이 'Y'이거나 undefined일 경우는 기본적으로 활성화 처리
        return item.use_yn === undefined || item.use_yn === null || item.use_yn.trim().toUpperCase() === 'Y';
    });
    
    console.debug(`filterActiveMstData: ${data.length} -> ${activeData.length} items filtered`);
    return activeData;
}

/**
 * Job ID 목록을 규칙에 따라 필터링합니다.
 * - 100의 배수인 Job ID 제외
 * - 900-910 범위의 Job ID 제외
 * @param {Array<Object>} jobs - 필터링할 Job 객체 배열. 각 객체는 'job_id' 또는 'cd' 속성을 가져야 합니다.
 * @returns {Array<Object>} 필터링된 Job 객체 배열
 */
export function filterValidJobs(jobs) {
    if (!Array.isArray(jobs)) {
        return [];
    }
    
    return jobs.filter(job => {
        const jobId = job.job_id || job.cd; // 다양한 속성 이름에 대응
        if (!jobId) return false;

        const numericString = String(jobId).replace(/[^0-9]/g, '');
        if (!numericString) return false;
        
        const jobIdNum = parseInt(numericString, 10);
        if (isNaN(jobIdNum)) return false;

        const isMultipleOf100 = jobIdNum > 0 && jobIdNum % 100 === 0;
        const isIn900Range = jobIdNum >= 900 && jobIdNum <= 910;

        return !isMultipleOf100 && !isIn900Range;
    });
}
