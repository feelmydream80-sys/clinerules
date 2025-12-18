// static/js/modules/data_analysis/utils.js

/**
 * @module utils
 * @description 데이터 분석 페이지에서 사용되는 유틸리티 함수들을 제공합니다.
 * - Cron 표현식 파싱, 숫자 포맷팅 등의 보조 기능을 담당합니다.
 * 
 * @example
 * import { parseCronExpression, numberWithCommas } from './utils.js';
 * 
 * const readableCron = parseCronExpression('* * * * *'); // "매분 실행"
 * const formattedNumber = numberWithCommas(10000); // "10,000"
 */


/**
 * @description 주기적 실행 패턴인지 확인하고, 맞다면 해석된 문자열을 반환합니다.
 * @param {string} value - Cron 표현식의 일부 (예: '5')
 * @param {string} unit - 시간 단위 (minute, hour, day, month, dow)
 * @returns {string|null} 해석된 문자열 또는 null
 */
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

/**
 * @description Cron 표현식을 사람이 읽기 쉬운 형식으로 해석합니다.
 * @param {string} cronExpression - Cron 표현식 문자열
 * @returns {string} 해석된 문자열
 */
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
    
    // 일 단위 주기 실행 (예: 0 0 */5 * * → 5일마다 0시 0분에 실행)
    if (minute !== '*' && hour !== '*' && dayInterval && month === '*' && dayOfWeek === '*') {
        return `${dayInterval} ${hour}시 ${minute}분에 실행`;
    }
    
    // 주 단위 주기 실행 (예: 0 0 * * 0 → 매주 일요일 0시 0분에 실행)
    if (minute !== '*' && hour !== '*' && dayOfMonth === '*' && month === '*' && weekInterval) {
        return `${weekInterval} ${hour}시 ${minute}분에 실행`;
    }

    // 매일 실행
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
        if (dayOfMonth.includes(',')) {
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
 * @description 숫자에 콤마를 추가하여 문자열로 반환합니다.
 * @param {number} x - 숫자
 * @returns {string} 콤마가 추가된 문자열
 */
export function numberWithCommas(x) {
    if (x === undefined || x === null) return '';
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * @description 숫자를 만, 억, 조 단위로 변환하여 소수점 첫째 자리까지 표시합니다.
 * @param {number} num - 변환할 숫자
 * @returns {string} 변환된 문자열
 */
export function formatNumberWithUnits(num) {
    if (typeof num !== 'number' || isNaN(num)) {
        return '';
    }

    if (num < 10000) {
        return numberWithCommas(num);
    }

    const units = [
        { value: 1e12, unit: '조' },
        { value: 1e8, unit: '억' },
        { value: 1e4, unit: '만' }
    ];

    for (let i = 0; i < units.length; i++) {
        if (num >= units[i].value) {
            const result = (num / units[i].value);
            // 소수점 첫째 자리까지 표시하되, 정수면 소수점 없이 표시
            return `${parseFloat(result.toFixed(1))}${units[i].unit}`;
        }
    }

    return numberWithCommas(num);
}

/**
 * @description 날짜 문자열을 받아서 한글 요일을 반환합니다.
 * @param {string} dateStr - 날짜 문자열
 * @returns {string} 한글 요일 (일, 월, ...)
 */
export function getKoreanDay(dateStr) {
    if (!dateStr) return '';
    const day = new Date(dateStr).getDay();
    return ['일','월','화','수','목','금','토'][day];
}
