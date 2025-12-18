# 📊 데이터분석 메뉴 상세 문서

## 🎯 메뉴 정보
- **메뉴 ID**: `data_analysis`
- **메뉴 이름**: 데이터분석
- **URL**: `/data_analysis`
- **메뉴 순서**: 4

## 🔗 관련 파일 구조

### 백엔드 (Flask)
```
📁 routes/analysis_routes.py
├── @analysis_bp.route("/data_analysis") - 메인 페이지
├── @analysis_bp.route('/api/analysis/summary') - 요약 데이터 API
├── @analysis_bp.route('/api/analysis/trend') - 추이 데이터 API
├── @analysis_bp.route('/api/analysis/raw_data') - 원천 데이터 API
├── @analysis_bp.route('/api/analysis/job_ids') - Job ID 목록 API
├── @analysis_bp.route('/api/analysis/error_codes') - 장애코드 목록 API
└── @analysis_bp.route('/api/analysis/error_code_map') - 장애코드 매핑 API

📁 service/dashboard_service.py
├── get_analysis_summary() - 분석 요약 데이터 조회
├── get_analysis_trend() - 분석 추이 데이터 조회
└── get_analysis_raw_data() - 분석 원천 데이터 조회

📁 dao/
├── con_hist_dao.py - 접속 이력 데이터
├── con_mst_dao.py - 접속 마스터 데이터
└── mngr_sett_dao.py - 관리자 설정 데이터
```

### 프론트엔드 (JavaScript)
```
📁 templates/data_analysis.html
├── 메인 데이터분석 템플릿
├── 필터 컨트롤러 (날짜, Job ID, 장애코드)
├── 요약 카드들 (소요시간, 실패건수, 성공률 등)
├── 추이 차트 캔버스
└── 데이터 테이블들 (원천데이터, Job정보)

📁 static/js/pages/data_analysis.js
├── initializeAnalysisPage() - 페이지 초기화
└── 이벤트 리스너 설정

📁 static/js/modules/data_analysis/
├── events.js - 메인 이벤트 처리 및 로직
├── data.js - 데이터 fetching 및 상태 관리
├── ui.js - UI 렌더링 및 컴포넌트
├── heatmap.js - 히트맵 차트 렌더링
├── chartRenderers.js - 차트 렌더링 (추이 차트 등)
└── utils.js - 유틸리티 함수
```

## 📋 데이터베이스 테이블

### 주요 조회 테이블
```sql
-- tb_con_hist: 접속 이력 (메인 데이터)
SELECT
    job_id, con_id, rqs_info, start_dt, execution_dt, end_dt,
    status, trbl_hist_no,
    EXTRACT(EPOCH FROM (end_dt - start_dt)) as duration_seconds
FROM tb_con_hist
WHERE start_dt >= :start_date AND start_dt < :end_date
    AND (:job_ids IS NULL OR job_id = ANY(:job_ids))
    AND (:error_codes IS NULL OR status = ANY(:error_codes))

-- tb_con_mst: 접속 마스터 (Job 정보)
SELECT job_id, job_nm, job_desc, conn_info
FROM tb_con_mst
WHERE job_id IN (
    SELECT DISTINCT job_id FROM tb_con_hist
    WHERE start_dt >= :start_date AND start_dt < :end_date
)

-- tb_mngr_sett: 관리자 설정 (차트 색상 등)
SELECT cd, chrt_colr, chrt_dsp_yn, chrt_tp
FROM tb_mngr_sett
WHERE chrt_dsp_yn = true
```

## 🔐 권한 및 보안

### 접근 권한
```python
@analysis_bp.route("/data_analysis")
@login_required
@check_password_change_required
@log_menu_access
def data_analysis():
    """데이터분석 접근 권한 확인"""
    user = session.get('user', {})
    is_admin = user.get('is_admin', False)
    return render_template("data_analysis.html", is_admin=is_admin)
```

### 데이터 필터링
```python
def get_analysis_data(user, start_date, end_date, job_ids=None, error_codes=None):
    """사용자 권한에 따른 데이터 필터링"""
    # 1. 사용자가 접근 가능한 Job ID 목록 조회
    accessible_jobs = get_user_accessible_jobs(user['user_id'])

    # 2. Job ID 필터 적용
    if job_ids:
        job_ids = [job for job in job_ids if job in accessible_jobs]
    else:
        job_ids = accessible_jobs

    # 3. 민감한 데이터 마스킹 (필요시)
    for record in results:
        if not user_can_access_detail(user, record):
            record['conn_info'] = '***MASKED***'
            record['rqs_info'] = '***MASKED***'

    return filtered_data
```

## 🎨 UI/UX 컴포넌트

### 필터 컨트롤
```html
<!-- 날짜 범위 선택 -->
<div class="flex items-center space-x-2">
    <label for="startDate">시작일:</label>
    <input type="date" id="startDate" class="form-input">
</div>
<div class="flex items-center space-x-2">
    <label for="endDate">종료일:</label>
    <input type="date" id="endDate" class="form-input">
</div>

<!-- Job ID 선택 -->
<div class="flex items-center space-x-2">
    <label for="jobIdSelect">Job ID:</label>
    <select id="jobIdSelect" class="form-select">
        <option value="">전체</option>
        <!-- 동적으로 Job ID 옵션들 -->
    </select>
</div>

<!-- 장애코드 선택 -->
<div class="flex items-center space-x-2">
    <label for="errorCodeSelect">장애코드:</label>
    <select id="errorCodeSelect" class="form-select">
        <option value="">전체</option>
        <!-- 동적으로 장애코드 옵션들 -->
    </select>
</div>
```

### 요약 카드들
```html
<!-- 소요시간 범위 카드 -->
<div class="bg-blue-50 rounded-lg p-4 shadow text-center" id="durationRangeCard">
    <div class="text-blue-600 font-bold text-lg">최대/최소 소요 시간</div>
    <div class="text-2xl font-bold mt-2" id="durationRange">-</div>
</div>

<!-- 실패 건수 카드 -->
<div class="bg-red-50 rounded-lg p-4 shadow text-center" id="failCountCard">
    <div class="text-red-600 font-bold text-lg">실패 호출 건수</div>
    <div class="text-2xl font-bold mt-2" id="failCount">-</div>
</div>

<!-- 성공률 카드 -->
<div class="bg-green-50 rounded-lg p-4 shadow text-center" id="successRateCard">
    <div class="text-green-600 font-bold text-lg">평균 성공률</div>
    <div class="text-2xl font-bold mt-2" id="successRate">-</div>
</div>

<!-- 총 호출 건수 카드 -->
<div class="bg-purple-50 rounded-lg p-4 shadow text-center" id="totalCountCard">
    <div class="text-purple-600 font-bold text-lg">총 호출 건수</div>
    <div class="text-2xl font-bold mt-2" id="totalCount">-</div>
</div>
```

### 차트 및 데이터 테이블
```html
<!-- 추이 차트 -->
<div class="bg-white rounded-lg shadow p-6" id="trendChartCard">
    <h3 class="text-lg font-semibold mb-4">시간별 추이</h3>
    <canvas id="trendChart"></canvas>
</div>

<!-- 원천 데이터 테이블 -->
<div class="bg-white rounded-lg shadow p-6" id="rawDataCard">
    <h3 class="text-lg font-semibold mb-4">원천 데이터</h3>
    <div class="overflow-x-auto">
        <table id="rawDataTable" class="min-w-full table-auto">
            <!-- 동적으로 생성되는 테이블 -->
        </table>
    </div>
    <div id="rawDataPagination" class="mt-4"></div>
</div>

<!-- Job 정보 테이블 -->
<div class="bg-white rounded-lg shadow p-6" id="jobInfoCard">
    <h3 class="text-lg font-semibold mb-4">Job 정보</h3>
    <div class="overflow-x-auto">
        <table id="jobInfoTable" class="min-w-full table-auto">
            <!-- 동적으로 생성되는 테이블 -->
        </table>
    </div>
    <div id="jobInfoPagination" class="mt-4"></div>
</div>
```

## 🔄 데이터 플로우

### 초기 로드 플로우
```
1. 페이지 로드 → DOMContentLoaded
2. initializeAnalysisPage() 호출
3. initializeData() → 메타데이터 로드 (Job ID, 장애코드, 색상)
4. setDefaultDates() → 기본 날짜 설정
5. loadAnalysisData() → 요약/추이/원천 데이터 로드
6. renderSummaryCards() → 요약 카드 렌더링
7. renderTrendChart() → 추이 차트 렌더링
8. renderRawTable() → 원천 데이터 테이블 렌더링
9. renderJobInfoTable() → Job 정보 테이블 렌더링
```

### 필터 변경 플로우
```
1. 필터 변경 (날짜/Job ID/장애코드)
2. loadAnalysisData() 재호출
3. 새 데이터로 모든 컴포넌트 리렌더링
4. 페이징 초기화
```

### AI 분석 플로우
```
1. "AI에게 질문" 버튼 클릭
2. 현재 필터 조건으로 프롬프트 생성
3. AI API 호출 (/api/analysis/dynamic-chart)
4. renderAiAnswer() → AI 응답 표시
5. 관련 차트/테이블 강조 표시
```

## 📊 주요 메트릭 계산

### 요약 데이터 계산
```javascript
// 소요시간 범위 계산
function calculateDurationRange(data) {
    const durations = data
        .filter(item => item.duration_seconds)
        .map(item => item.duration_seconds);

    if (durations.length === 0) return '-';

    const min = Math.min(...durations);
    const max = Math.max(...durations);

    return `${min.toFixed(2)}s - ${max.toFixed(2)}s`;
}

// 실패 건수 계산
function calculateFailCount(data) {
    return data.filter(item => item.status === 'FAILED').length;
}

// 성공률 계산
function calculateSuccessRate(data) {
    if (data.length === 0) return '0.00%';
    const successCount = data.filter(item => item.status === 'SUCCESS').length;
    return ((successCount / data.length) * 100).toFixed(2) + '%';
}
```

### 추이 차트 데이터 가공
```javascript
function processTrendData(rawData, timeUnit = 'hour') {
    // 시간 단위별 그룹화
    const grouped = rawData.reduce((acc, item) => {
        const timeKey = getTimeKey(item.start_dt, timeUnit);
        if (!acc[timeKey]) {
            acc[timeKey] = {
                success: 0,
                failed: 0,
                total: 0
            };
        }

        acc[timeKey].total++;
        if (item.status === 'SUCCESS') {
            acc[timeKey].success++;
        } else {
            acc[timeKey].failed++;
        }

        return acc;
    }, {});

    // 차트 데이터 형식으로 변환
    return Object.entries(grouped).map(([time, stats]) => ({
        time,
        successRate: stats.total > 0 ? (stats.success / stats.total) * 100 : 0,
        successCount: stats.success,
        failCount: stats.failed,
        totalCount: stats.total
    }));
}
```

## 🚨 에러 처리 및 로깅

### API 에러 처리
```javascript
async function loadAnalysisData() {
    try {
        const [summary, trend, raw] = await Promise.all([
            fetchSummaryData(startDate, endDate, jobIds, allData),
            fetchTrendData(startDate, endDate, jobIds, allData),
            fetchRawData(startDate, endDate, jobIds, errorCodes, allData)
        ]);

        // 데이터 검증
        if (!summary || !trend || !raw) {
            throw new Error('데이터 로드 실패');
        }

        renderSummaryCards(summary);
        renderTrendChart(trend);
        renderRawTable(raw);

    } catch (error) {
        console.error('데이터분석 데이터 로드 실패:', error);
        showErrorMessage('데이터를 불러올 수 없습니다.');
    }
}
```

### 데이터 검증
```javascript
function validateAnalysisData(data) {
    if (!Array.isArray(data)) {
        throw new Error('데이터 형식이 올바르지 않습니다');
    }

    data.forEach(item => {
        if (!item.start_dt || !item.job_id) {
            console.warn('필수 필드가 누락된 데이터:', item);
        }
    });

    return data;
}
```

## ⚡ 성능 최적화

### 데이터 캐싱 전략
```javascript
// 메타데이터 캐싱 (Job ID, 장애코드, 색상)
let metadataCache = {
    jobIds: [],
    errorCodes: [],
    colorMap: {},
    lastUpdate: null,
    ttl: 30 * 60 * 1000  // 30분
};

async function loadMetadata() {
    if (isCacheValid(metadataCache)) {
        return metadataCache;
    }

    const [jobIds, errorCodes, colorMap] = await Promise.all([
        fetch('/api/analysis/job_ids'),
        fetch('/api/analysis/error_codes'),
        fetch('/api/analysis/error_code_map')
    ]);

    metadataCache = {
        jobIds: jobIds.data,
        errorCodes: errorCodes.data,
        colorMap: colorMap.data,
        lastUpdate: Date.now()
    };

    return metadataCache;
}
```

### 페이징 최적화
```javascript
// 클라이언트 사이드 페이징
function initRawDataPaging(data, pageSize = 100) {
    const totalPages = Math.ceil(data.length / pageSize);

    updatePaginationData('rawDataPagination', {
        currentPage: 1,
        totalPages,
        onPageChange: (page) => {
            const start = (page - 1) * pageSize;
            const end = start + pageSize;
            renderRawTablePage(data.slice(start, end));
        }
    });
}

// 서버 사이드 페이징 (대용량 데이터)
async function fetchRawDataPaged(page = 1, pageSize = 100) {
    const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate,
        page,
        page_size: pageSize,
        job_ids: jobIds.join(','),
        error_codes: errorCodes.join(',')
    });

    return await fetch(`/api/analysis/raw_data_paged?${params}`);
}
```

### 차트 렌더링 최적화
```javascript
// 차트 인스턴스 재사용
let trendChart = null;

function renderTrendChart(data) {
    const ctx = document.getElementById('trendChart');

    if (trendChart) {
        trendChart.data = processChartData(data);
        trendChart.update('none'); // 애니메이션 없이 업데이트
    } else {
        trendChart = new Chart(ctx, {
            type: 'line',
            data: processChartData(data),
            options: trendChartOptions
        });
    }
}
```

## 🧪 테스트 케이스

### 단위 테스트
```javascript
describe('Data Analysis Utils', () => {
    test('should calculate duration range correctly', () => {
        const data = [
            { duration_seconds: 1.5 },
            { duration_seconds: 3.2 },
            { duration_seconds: 2.1 }
        ];
        expect(calculateDurationRange(data)).toBe('1.50s - 3.20s');
    });

    test('should calculate success rate correctly', () => {
        const data = [
            { status: 'SUCCESS' },
            { status: 'FAILED' },
            { status: 'SUCCESS' }
        ];
        expect(calculateSuccessRate(data)).toBe('66.67%');
    });

    test('should filter data by job IDs', () => {
        const data = [
            { job_id: 'JOB1', status: 'SUCCESS' },
            { job_id: 'JOB2', status: 'FAILED' },
            { job_id: 'JOB1', status: 'SUCCESS' }
        ];
        const filtered = filterByJobIds(data, ['JOB1']);
        expect(filtered).toHaveLength(2);
        expect(filtered.every(item => item.job_id === 'JOB1')).toBe(true);
    });
});
```

### 통합 테스트
```javascript
describe('Data Analysis API', () => {
    test('should return analysis summary data', async () => {
        const response = await request(app)
            .get('/api/analysis/summary?start_date=2024-01-01&end_date=2024-01-31')
            .set('Authorization', 'Bearer token');

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('durationRange');
        expect(response.body).toHaveProperty('failCount');
        expect(response.body).toHaveProperty('successRate');
        expect(response.body).toHaveProperty('totalCount');
    });

    test('should filter data by job IDs', async () => {
        const response = await request(app)
            .get('/api/analysis/summary?start_date=2024-01-01&end_date=2024-01-31&job_ids=JOB1,JOB2')
            .set('Authorization', 'Bearer token');

        expect(response.status).toBe(200);
        // 데이터가 JOB1, JOB2로 필터링되었는지 검증
    });

    test('should handle AI analysis requests', async () => {
        const response = await request(app)
            .get('/api/analysis/dynamic-chart?question=성공률이 낮은 시간대는 언제인가')
            .set('Authorization', 'Bearer token');

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('answer');
        expect(response.body).toHaveProperty('insights');
    });
});
```

### E2E 테스트
```javascript
describe('Data Analysis Page', () => {
    test('should load page and display data', async () => {
        await page.goto('/data_analysis');

        // 필터 요소들이 존재하는지 확인
        await expect(page.locator('#startDate')).toBeVisible();
        await expect(page.locator('#endDate')).toBeVisible();
        await expect(page.locator('#jobIdSelect')).toBeVisible();

        // 요약 카드들이 로드되는지 확인
        await expect(page.locator('#durationRangeCard')).toContainText('최대/최소 소요 시간');
        await expect(page.locator('#failCountCard')).toContainText('실패 호출 건수');

        // 차트가 렌더링되는지 확인
        await expect(page.locator('#trendChart')).toBeVisible();

        // 테이블들이 존재하는지 확인
        await expect(page.locator('#rawDataTable')).toBeVisible();
        await expect(page.locator('#jobInfoTable')).toBeVisible();
    });

    test('should filter data correctly', async () => {
        await page.goto('/data_analysis');

        // Job ID 선택
        await page.selectOption('#jobIdSelect', 'JOB1');

        // 데이터가 필터링되는지 확인 (요약 카드 값 변경)
        await expect(page.locator('#totalCount')).not.toHaveText('-');
    });
});
```</content>
</xai:function_call">Invalid file path 'docs/menu_data_analysis.md'. Parent directory doesn't exist.
