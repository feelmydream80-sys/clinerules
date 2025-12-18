// static/js/pages/data_analysis.js

/**
 * @file data_analysis.js
 * @description 데이터 분석 페이지의 진입점(Entry Point) 역할을 합니다.
 * - `events.js` 모듈의 `initializeAnalysisPage` 함수를 호출하여 페이지를 초기화합니다.
 * - 모든 기능 구현은 `static/js/modules/data_analysis/` 디렉토리의 모듈들이 담당합니다.
 * 
 * @see {@link module:data} for data fetching and state management.
 * @see {@link module:ui} for UI rendering and DOM manipulation.
 * @see {@link module:events} for event handling and main application logic.
 * @see {@link module:utils} for utility functions.
 * 
 * @example
 * // HTML에서 <script type="module" src=".../data_analysis.js"></script> 형태로 로드됩니다.
 * // DOMContentLoaded 이벤트에 따라 자동으로 initializeAnalysisPage 함수가 실행됩니다.
 */

import { initializeAnalysisPage as init } from '../modules/data_analysis/events.js';

// DOM이 완전히 로드되면 데이터 분석 페이지 초기화 함수를 호출합니다.
document.addEventListener('DOMContentLoaded', init);

export { init };
