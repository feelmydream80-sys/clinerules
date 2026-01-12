# 📊 대시보드 메뉴 상세 문서

## 🎯 메뉴 정보
- **메뉴 ID**: `dashboard`
- **메뉴 이름**: 대시보드
- **URL**: `/dashboard`
- **메뉴 순서**: 2

## 🔗 관련 파일 구조

### 백엔드 (Flask)
```
📁 routes/ui/dashboard_routes.py
├── @dashboard_bp.route("/dashboard") - 메인 페이지
├── @dashboard_bp.route("/api/dashboard/summary") - 요약 데이터 API
└── @dashboard_bp.route("/api/dashboard/detail") - 상세 데이터 API

📁 service/dashboard_service.py
├── get_dashboard_summary() - 대시보드 요약 데이터 조회
├── get_dashboard_detail() - 대시보드 상세 데이터 조회
└── calculate_success_rates() - 성공률 계산 로직

📁 dao/con_hist_dao.py
├── get_recent_connection_history() - 최근 접속 이력 조회
├── get_success_rate_summary() - 성공률 요약 조회
└── get_error_statistics() - 장애 통계 조회
```

### 프론트엔드 (JavaScript)
```
📁 templates/dashboard.html
├── 메인 대시보드 템플릿
├── 카드 레이아웃
└── 차트 캔버스

📁 static/js/pages/dashboard.js
├── initDashboard() - 대시보드 초기화
├── loadDashboardSummary() - 요약 데이터 로드
└── renderDashboardCharts() - 차트 렌더링

📁 static/js/modules/dashboard/
├── ui.js - UI 컴포넌트 (카드, 차트 등)
├── events.js - 이벤트 처리
├── data.js - 데이터 관리
└── utils.js - 유틸리티 함수
```

## 📋 데이터베이스 테이블

### 주요 조회 테이블
```sql
-- tb_con_hist: 접속 이력 (메인 데이터)
SELECT job_id, status, start_dt, end_dt, success_count, fail_count
FROM tb_con_hist
WHERE start_dt >= :start_date AND start_dt < :end_date

-- tb_mngr_sett: 관리자 설정 (임계값 등)
SELECT cd, dly_sucs_rt_thrs_val, wk_sucs_rt_thrs_val, mthl_sucs_rt_thrs_val
FROM tb_mngr_sett
WHERE chrt_dsp_yn = true
```

## 🔐 권한 및 보안

### 접근 권한
```python
@dashboard_required
def dashboard():
    """대시보드 접근 권한 확인"""
    if 'dashboard' not in session['user'].get('permissions', []):
        return render_template("unauthorized.html")
```

### 데이터 필터링
```python
def get_dashboard_summary(user, start_date, end_date):
    """사용자 권한에 따른 데이터 필터링"""
    # 1. 사용자가 접근 가능한 Job ID 목록 조회
    accessible_jobs = get_user_accessible_jobs(user['user_id'])

    # 2. 권한이 없는 데이터는 제외
    filtered_data = [record for record in raw_data
                    if record['job_id'] in accessible_jobs]

    return filtered_data
```

## 🎨 UI/UX 컴포넌트

### 대시보드 카드 구조
```html
<!-- 기간별 성공률 카드 -->
<div class="dashboard-card">
    <div class="card-header">
        <h3>일일 성공률</h3>
        <span class="metric-value">{{ day_success_rate }}%</span>
    </div>
    <div class="card-chart">
        <canvas id="daySuccessChart"></canvas>
    </div>
</div>
```

### 차트 설정
```javascript
const dashboardChartOptions = {
    responsive: true,
    plugins: {
        legend: { display: false },
        tooltip: {
            callbacks: {
                label: (context) => `${context.label}: ${context.raw}%`
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            max: 100,
            title: { display: true, text: '성공률 (%)' }
        }
    }
};
```

## 🔄 데이터 플로우

### 초기 로드 플로우
```
1. 페이지 로드 → DOMContentLoaded
2. initDashboard() 호출
3. loadDashboardSummary() → API 호출
4. renderDashboardCards() → UI 업데이트
5. renderDashboardCharts() → 차트 렌더링
```

### 실시간 업데이트
```javascript
// 5분마다 자동 업데이트
setInterval(() => {
    loadDashboardSummary();
}, 5 * 60 * 1000);
```

## 📊 주요 메트릭 계산

### 성공률 계산 로직
```javascript
function calculateSuccessRate(successCount, totalCount) {
    if (totalCount === 0) return 0;
    return Math.round((successCount / totalCount) * 100 * 100) / 100;
}

// 기간별 계산
const daySuccessRate = calculateSuccessRate(daySuccess, dayTotal);
const weekSuccessRate = calculateSuccessRate(weekSuccess, weekTotal);
const monthSuccessRate = calculateSuccessRate(monthSuccess, monthTotal);
```

### 상태별 색상 매핑
```javascript
const statusColors = {
    success: '#28a745',    // 녹색
    warning: '#ffc107',    // 노란색
    error: '#dc3545'       // 빨간색
};

function getStatusColor(successRate, threshold) {
    if (successRate >= threshold) return statusColors.success;
    if (successRate >= threshold * 0.8) return statusColors.warning;
    return statusColors.error;
}
```

## 🚨 에러 처리 및 로깅

### API 에러 처리
```javascript
async function loadDashboardSummary() {
    try {
        const response = await fetch('/api/dashboard/summary');
        if (!response.ok) throw new Error('API 호출 실패');

        const data = await response.json();
        updateDashboardCards(data);
    } catch (error) {
        console.error('대시보드 데이터 로드 실패:', error);
        showErrorMessage('데이터를 불러올 수 없습니다.');
    }
}
```

### 백엔드 로깅
```python
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"대시보드 오류: {error}", exc_info=True)
    return jsonify({"error": "서버 오류가 발생했습니다."}), 500
```

## ⚡ 성능 최적화

### 데이터 캐싱 전략
```javascript
// 메모리 캐시 (브라우저 세션 동안 유지)
let dashboardCache = {
    summary: null,
    lastUpdate: null,
    ttl: 5 * 60 * 1000  // 5분
};

function getCachedData() {
    if (dashboardCache.summary &&
        Date.now() - dashboardCache.lastUpdate < dashboardCache.ttl) {
        return dashboardCache.summary;
    }
    return null;
}
```

### 차트 최적화
```javascript
// 차트 인스턴스 재사용
let dashboardCharts = {};

function renderDashboardCharts(data) {
    // 기존 차트 파괴 방지
    Object.values(dashboardCharts).forEach(chart => {
        if (chart) chart.destroy();
    });

    // 새 차트 생성
    dashboardCharts.dayChart = createSuccessRateChart('dayChart', data.day);
    dashboardCharts.weekChart = createSuccessRateChart('weekChart', data.week);
}
```

## 🧪 테스트 케이스

### 단위 테스트
```javascript
describe('Dashboard Service', () => {
    test('should calculate success rate correctly', () => {
        expect(calculateSuccessRate(95, 100)).toBe(95);
        expect(calculateSuccessRate(0, 0)).toBe(0);
    });

    test('should filter data by user permissions', () => {
        const user = { user_id: 'user1', permissions: ['dashboard'] };
        const data = [{ job_id: 'JOB1' }, { job_id: 'JOB2' }];
        const filtered = filterDataByPermissions(data, user);
        // 권한에 따른 필터링 검증
    });
});
```

### 통합 테스트
```javascript
describe('Dashboard API', () => {
    test('should return dashboard summary', async () => {
        const response = await request(app)
            .get('/api/dashboard/summary')
            .set('Authorization', 'Bearer token');

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('daySuccessRate');
    });
});
```

---

## 🚨 **과거 이슈 회피 가이드라인**

### **1. 데이터 키 이름 불일치 방지**
```javascript
// ❌ 잘못된 방법: 임의로 키 이름 추측
const successColor = jobSetting.cf_success_wd_color || '#28a745';

// ✅ 올바른 방법: 실제 백엔드 응답 데이터 확인
console.log('API 응답 데이터:', jobSetting); // 실제 키 이름 확인
const successColor = jobSetting.cnn_sucs_wrd_colr || '#28a745';
```

**체크리스트:**
- [ ] 백엔드 API 실제 응답 데이터 `console.log`로 확인
- [ ] 프론트엔드에서 사용하는 키 이름이 백엔드와 일치하는지 검증
- [ ] 데이터가 없을 경우 적절한 기본값 설정

### **2. 요구사항 불완전 이해 방지**
```javascript
// 개발 시작 전 요구사항 명확화
const requirements = {
    iconDisplay: true,      // 아이콘 표시 여부
    colorLogic: 'threshold-based', // 색상 결정 로직
    dataSource: 'mngr_sett' // 데이터 소스
};

// 사용자 확인
console.log('요구사항 확인:', requirements);
// "이 내용이 맞습니까?" - 사용자에게 확인 요청
```

### **3. 데이터 명세 준수**
```javascript
// tb_mngr_sett 테이블의 실제 컬럼명 사용
const colorMapping = {
    success: setting.cnn_sucs_wrd_colr,     // 실제 컬럼명
    warning: setting.cnn_warn_wrd_colr,     // 실제 컬럼명
    error: setting.cnn_failr_wrd_colr       // 실제 컬럼명
};

// 임계값도 실제 컬럼명 사용
const thresholds = {
    day: setting.dly_sucs_rt_thrs_val,      // 실제 컬럼명
    week: setting.dd7_sucs_rt_thrs_val,     // 실제 컬럼명
    month: setting.mthl_sucs_rt_thrs_val    // 실제 컬럼명
};
```

### **4. 데이터 플로우 전체 검증**
```javascript
// 1. 백엔드 데이터 조회
const rawData = await fetchDashboardData();

// 2. 데이터 변환 로직
const processedData = processDashboardData(rawData);

// 3. 프론트엔드 렌더링 전 검증
console.log('최종 렌더링 데이터:', processedData);

// 4. 렌더링 후 결과 확인
renderDashboard(processedData);
```

### **5. 시간대 처리 표준화**
```javascript
// 백엔드에서 KST로 변환된 문자열을 그대로 사용
// ❌ 잘못된 방법
const displayTime = new Date(row.start_dt).toLocaleString();

// ✅ 올바른 방법
const displayTime = row.start_dt; // 백엔드에서 이미 KST로 변환됨
```

### **6. 로깅 표준화**
```javascript
// ❌ 잘못된 방법
print('디버그 메시지'); // 프로덕션에서 사라짐

// ✅ 올바른 방법
current_app.logger.debug('디버그 메시지'); // 환경에 관계없이 기록됨
```

### **7. CSS 로딩 타이밍 문제 방지**
```javascript
// SPA 환경에서 CSS가 로드되기 전 JavaScript 실행 방지
function ensureCSSLoaded() {
    return new Promise((resolve) => {
        const checkCSS = () => {
            const container = document.getElementById('cardContainer');
            if (container && getComputedStyle(container).minHeight !== 'auto') {
                resolve();
            } else {
                setTimeout(checkCSS, 10);
            }
        };
        checkCSS();
    });
}
```

### **8. 차트 크기 안정화**
```javascript
// ResizeObserver를 활용한 안정적인 차트 크기 조정
const observer = new ResizeObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.contentRect.height > 150) {
            successRateChart.update('none'); // 애니메이션 없이 크기 조정
        }
    });
});
observer.observe(chartContainer);
```

### **9. 트랜잭션 관리 표준화**
```python
# 서비스 레벨에서 트랜잭션 관리
def update_dashboard_settings(user_id, settings):
    try:
        with get_db_connection() as conn:
            # 여러 DAO 작업 수행
            user_dao.update_user(conn, user_id, settings)
            settings_dao.update_settings(conn, user_id, settings);

            conn.commit()  # 모든 작업 성공 시 커밋
    except Exception as e:
        conn.rollback()  # 실패 시 롤백
        raise
```

### **10. 세션 관리 보안**
```python
# 사용자별 세션 만료 시간 설정
def set_user_session_expiry(user):
    if user.get('is_admin'):
        lifetime = timedelta(days=365)  # 관리자: 1년
    else:
        lifetime = current_app.config['PERMANENT_SESSION_LIFETIME']  # 일반: 설정값

    session['expiry_time'] = (datetime.utcnow() + lifetime).isoformat()
```

---

## 📋 **개발 시 체크리스트**

### **요구사항 분석 단계:**
- [ ] 사용자 요구사항을 자신의 언어로 요약해서 확인받기
- [ ] 데이터 명세(키 이름, 타입, 기본값) 명확히 확인
- [ ] 백엔드 API 응답 구조 미리 검증

### **개발 시작 단계:**
- [ ] 데이터 플로우 전체(백엔드→프론트엔드) 파악
- [ ] 기존 유사 기능 코드 패턴 분석
- [ ] 시간대 처리 방식 표준화 준수

### **코딩 단계:**
- [ ] 백엔드 로거 사용(`current_app.logger`)
- [ ] 데이터 키 이름 백엔드 실제 응답과 일치 확인
- [ ] CSS 로딩 타이밍 고려한 JavaScript 작성
- [ ] 차트 크기 동적 조정 로직 포함

### **테스트 단계:**
- [ ] 실제 API 응답 데이터로 테스트
- [ ] 시간대 변환 결과 확인
- [ ] 다양한 브라우저에서 UI 확인
- [ ] 모바일 반응형 동작 확인

### **배포 전 검증:**
- [ ] 프로덕션 로그에서 `print()` 문장 없는지 확인
- [ ] 트랜잭션 관리 로직 적절한지 검증
- [ ] 세션 만료 시간 설정 확인
- [ ] 데이터 마스킹 로직 작동 확인</content>
</xai:function_call">Invalid file path 'docs/menu_dashboard.md'. Parent directory doesn't exist.