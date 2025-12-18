// 파일명: static/js/modules/chartRenderers.js
// 주요 역할: Chart.js를 사용하여 차트를 렌더링하고 업데이트하는 함수들을 정의합니다.

// 전역 변수로 차트 인스턴스 저장 (모듈 내부에서 관리)
let successRateChartInstance;
let troublePieChartInstance;

/**
 * Chart.js 차트 인스턴스를 생성하거나 업데이트합니다.
 * @param {string} chartId - 캔버스 요소의 ID
 * @param {string} type - 차트 타입 ('line', 'bar', 'doughnut', 'pie')
 * @param {Object} data - 차트 데이터 객체
 * @param {Object} options - 차트 옵션 객체
 * @param {Chart} [existingChart] - 기존 Chart 인스턴스 (업데이트 시)
 * @returns {Chart} 새로 생성되거나 업데이트된 Chart 인스턴스
 */
export function createOrUpdateChart(chartId, type, data, options, existingChart) {
    const ctx = document.getElementById(chartId);
    if (!ctx) {
        console.error(`ERROR: Canvas element with ID '${chartId}' not found.`);
        return null;
    }

    if (existingChart) {
        existingChart.data = data;
        existingChart.options = options;
        existingChart.update();
        return existingChart;
    } else {
        const newChart = new Chart(ctx, {
            type: type,
            data: data,
            options: options
            // Datalabels 플러그인 제거 - 사용자 요청에 따라 데이터 레이블 표시하지 않음
        });
        return newChart;
    }
}

/**
 * 기간별 수집 성공률 차트를 렌더링하거나 업데이트합니다.
 * @param {Array<Object>} data - 성공률 추이 데이터
 * @param {Object} allAdminSettings - 모든 Job ID에 대한 관리자 설정
 * @param {string} chartType - 'line' 또는 'bar'
 */
export function renderSuccessRateChart(data, allAdminSettings, chartType) {

    const labels = [...new Set(data.map(item => item.base_date))].sort(); // 날짜 레이블 추출 및 정렬

    const datasets = Object.values(allAdminSettings)
        .filter(setting => setting.display_yn) // display_yn이 true인 Job만 필터링
        .map(setting => {
            const jobData = data.filter(item => item.job_id === setting.cd);
            const successRates = labels.map(date => {
                const record = jobData.find(item => item.base_date === date);
                return record ? (record.success_rate * 100).toFixed(2) : null;
            });

            return {
                label: setting.cd_nm || setting.cd,
                borderColor: setting.chart_color || '#007bff', // 관리자 설정의 차트 색상 사용
                backgroundColor: setting.chart_color ? `${setting.chart_color}80` : 'rgba(0, 123, 255, 0.5)', // 투명도 추가
                data: successRates,
                tension: 0.3,
                fill: false,
                hidden: false, // 기본적으로 모두 표시
            };
        });

    const chartData = {
        labels: labels,
        datasets: datasets
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: '기간별 수집 성공률 추이',
                font: { size: 18, weight: 'bold' },
                color: '#333'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y;
                        }
                        return label;
                    }
                }
            },
            datalabels: {
                display: false // 기본적으로 데이터 레이블 비활성화
            },
            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    font: { size: 12 },
                    color: '#555',
                    boxWidth: 20,
                    padding: 15
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    tooltipFormat: 'yyyy-MM-dd',
                    displayFormats: {
                        day: 'MM-dd'
                    }
                },
                title: {
                    display: true,
                    text: '날짜',
                    color: '#555'
                },
                grid: {
                    display: false
                }
            },
            y: {
                title: {
                    display: true,
                    text: '성공률 (%)',
                    color: '#555'
                },
                min: 0,
                max: 100,
                ticks: {
                    // % 표시 제거 - 사용자 요청
                },
                grid: {
                    color: '#e0e0e0'
                }
            }
        },
        animation: {
    duration: 800, // 부드러운 페이드
    easing: 'linear' // 선형 페이드 (바운스 없음)
},
    };

    successRateChartInstance = createOrUpdateChart('successRateChart', chartType, chartData, chartOptions, successRateChartInstance);
}

/**
 * 장애 코드별 비율 차트를 렌더링하거나 업데이트합니다.
 * @param {Array<Object>} data - 장애 통계 데이터
 * @param {string} chartType - 'doughnut' 또는 'bar'
 */
export function renderTroubleChart(data, chartType) {

    let chartData;
    let chartOptions;

    if (chartType === 'doughnut') {
        const statusCounts = {};
        data.forEach(item => {
            statusCounts[item.status_name] = (statusCounts[item.status_name] || 0) + item.count;
        });

        const labels = Object.keys(statusCounts);
        const counts = Object.values(statusCounts);

        const backgroundColors = labels.map(label => {
            switch (label) {
                case '장애': return '#dc3545'; // Red
                case '경고': return '#ffc107'; // Orange
                case '주의': return '#ffc107'; // Yellow (경고와 동일 색상 유지)
                case '정상': return '#28a745'; // Green
                case '미수집': return '#6c757d'; // Gray
                case '확인필요': return '#343a40'; // Dark Gray
                default: return '#cccccc'; // Default
            }
        });

        chartData = {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: backgroundColors,
                hoverOffset: 10,
                borderWidth: 1,
                borderColor: '#fff'
            }]
        };

        chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: '장애 코드별 비율',
                    font: { size: 18, weight: 'bold' },
                    color: '#333'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += `${context.parsed} 건`;
                            }
                            return label;
                        }
                    }
                },
                datalabels: {
                    display: false // 완전 비활성화 - 차트 위 데이터 값 표시하지 않음
                }
                legend: {
                    display: true,
                    position: 'right',
                    labels: {
                        font: { size: 12 },
                        color: '#555',
                        boxWidth: 20,
                        padding: 15
                    }
                }
            },
            animation: {
    duration: 800, // 부드러운 페이드
    easing: 'linear' // 선형 페이드 (바운스 없음)
},
        };
    } else if (chartType === 'bar') {
        const hourlyData = {}; // { hour: { status: count } }
        data.forEach(item => {
            if (!hourlyData[item.hour]) {
                hourlyData[item.hour] = {};
            }
            hourlyData[item.hour][item.status] = item.count;
        });

        const hours = Array.from({ length: 24 }, (_, i) => i); // 0부터 23시까지
        const statuses = [...new Set(data.map(item => item.status))].sort(); // 모든 상태 코드

        const backgroundColorsMap = {
            'CD902': '#dc3545', // 장애 (Red)
            'CD903': '#ffc107', // 경고 (Orange)
            'CD901': '#28a745', // 정상 (Green)
            'CD904': '#17a2b8', // 수집중 (Blue)
            'CD905': '#343a40', // 확인필요 (Dark Gray)
            // 필요한 경우 다른 상태 코드에 대한 색상 추가
        };

        const datasets = statuses.map(status => {
            return {
                label: status, // 실제 상태 이름으로 변경 필요 (예: '장애', '경고')
                data: hours.map(hour => (hourlyData[hour] && hourlyData[hour][status]) ? hourlyData[hour][status] : 0),
                backgroundColor: backgroundColorsMap[status] || '#cccccc',
                borderColor: backgroundColorsMap[status] || '#cccccc',
                borderWidth: 1
            };
        });

        chartData = {
            labels: hours.map(h => `${h}시`),
            datasets: datasets
        };

        chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: '시간대별 장애 발생 현황',
                    font: { size: 18, weight: 'bold' },
                    color: '#333'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += `${context.parsed} 건`;
                            }
                            return label;
                        }
                    }
                },
                datalabels: {
                    display: false, // 바 차트에서는 기본적으로 데이터 레이블 비활성화
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        font: { size: 12 },
                        color: '#555',
                        boxWidth: 20,
                        padding: 15
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '시간',
                        color: '#555'
                    },
                    grid: {
                        display: false
                    },
                    stacked: true // 스택 바 차트
                },
                y: {
                    title: {
                        display: true,
                        text: '발생 건수',
                        color: '#555'
                    },
                    beginAtZero: true,
                    grid: {
                        color: '#e0e0e0'
                    },
                    stacked: true // 스택 바 차트
                }
            },
            animation: {
    duration: 800, // 부드러운 페이드
    easing: 'linear' // 선형 페이드 (바운스 없음)
},
        };
    }

    troublePieChartInstance = createOrUpdateChart('troublePieChart', chartType, chartData, chartOptions, troublePieChartInstance);
}
