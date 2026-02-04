 # 데이터정의 탭 구현 가이드

## 개요

이 문서는 독립적인 HTML 목업 파일(`data_definition_mock.html`)을 실제 시스템에 적용하기 위한 구현 가이드입니다.

## 파일 구조

```
msys/
├── routes/
│   ├── data_definition_routes.py     # 새로운 라우트 파일
│   └── api/
│       └── data_definition_api.py    # 기존 API (유지)
├── service/
│   └── data_definition_service.py    # 기존 서비스 (유지)
├── dao/
│   └── con_mst_dao.py               # 기존 DAO (유지)
└── static/
    └── data-definition/
        ├── data_definition_mock.html  # 독립 HTML 목업
        ├── data_definition.js         # 별도 JS 모듈
        └── data_definition.css        # 별도 CSS 파일
```

## 1. 새로운 라우트 파일 생성

### 파일: `routes/data_definition_routes.py`

```python
# routes/data_definition_routes.py
from flask import Blueprint, request, jsonify, session
import logging
from service.data_definition_service import DataDefinitionService
from msys.database import get_db_connection
from routes.auth_routes import login_required, check_password_change_required

bp = Blueprint('data_definition', __name__, url_prefix='/api/data-definition')

@bp.route('/list', methods=['GET'])
@login_required
@check_password_change_required
def get_data_list():
    """데이터 목록을 조회합니다."""
    try:
        with get_db_connection() as conn:
            service = DataDefinitionService(conn)
            data = service.get_data_list()
            return jsonify(data), 200
    except Exception as e:
        logging.error(f"Error fetching data list: {e}", exc_info=True)
        return jsonify({"message": "Error fetching data list."}), 500

@bp.route('/create', methods=['POST'])
@login_required
@check_password_change_required
def create_data():
    """새로운 데이터를 생성합니다."""
    try:
        data = request.json
        with get_db_connection() as conn:
            service = DataDefinitionService(conn)
            service.create_data(data)
            conn.commit()
            return jsonify({"message": "Data created successfully."}), 201
    except ValueError as e:
        logging.warning(f"Failed to create data: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error creating data: {e}", exc_info=True)
        return jsonify({"message": "Error creating data."}), 500

@bp.route('/create_mngr_sett', methods=['POST'])
@login_required
@check_password_change_required
def create_mngr_sett():
    """관리자 설정 데이터를 생성합니다."""
    try:
        data = request.json
        cd = data.get('cd')
        
        if not cd:
            return jsonify({"message": "CD is required."}), 400
            
        # CD900-CD999 범위와 100의 배수는 제외
        cd_number = int(cd[2:]) if cd.startswith('CD') and cd[2:].isdigit() else None
        if cd_number and ((900 <= cd_number <= 999) or (cd_number % 100 == 0)):
            return jsonify({"message": "CD900-CD999 범위와 100의 배수는 제외됩니다."}), 400
        
        with get_db_connection() as conn:
            service = DataDefinitionService(conn)
            service.create_mngr_sett(cd)
            conn.commit()
            return jsonify({"message": "Mngr sett created successfully."}), 201
    except ValueError as e:
        logging.warning(f"Failed to create mngr sett: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error creating mngr sett: {e}", exc_info=True)
        return jsonify({"message": "Error creating mngr sett."}), 500

@bp.route('/update/<cd_cl>/<cd>', methods=['POST'])
@login_required
@check_password_change_required
def update_data(cd_cl, cd):
    """기존 데이터를 수정합니다."""
    try:
        data = request.json
        with get_db_connection() as conn:
            service = DataDefinitionService(conn)
            service.update_data(cd_cl, cd, data)
            conn.commit()
            return jsonify({"message": "Data updated successfully."}), 200
    except ValueError as e:
        logging.warning(f"Failed to update data: {e}")
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error updating data: {e}", exc_info=True)
        return jsonify({"message": "Error updating data."}), 500

@bp.route('/delete/<cd_cl>/<cd>', methods=['DELETE'])
@login_required
@check_password_change_required
def delete_data(cd_cl, cd):
    """데이터를 삭제합니다."""
    try:
        with get_db_connection() as conn:
            service = DataDefinitionService(conn)
            service.delete_data(cd_cl, cd)
            conn.commit()
            return jsonify({"message": "Data deleted successfully."}), 200
    except Exception as e:
        logging.error(f"Error deleting data: {e}", exc_info=True)
        return jsonify({"message": "Error deleting data."}), 500
```

## 2. 라우트 등록

### 파일: `routes/__init__.py`

```python
# routes/__init__.py
from flask import Flask
from routes.auth_routes import auth_bp
from routes.today_routes import today_bp
from routes.admin_routes import admin_bp
from routes.analysis_routes import analysis_bp
from routes.jandi_routes import jandi_bp
from routes.data_spec_routes import data_spec_bp
from routes.mapping_routes import mapping_bp
from routes.mngr_sett_routes import mngr_sett_bp
from routes.card_summary_routes import card_summary_bp
from routes.data_report_routes import data_report_bp
from routes.data_definition_routes import bp as data_definition_bp  # 추가

def register_routes(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(today_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(jandi_bp)
    app.register_blueprint(data_spec_bp)
    app.register_blueprint(mapping_bp)
    app.register_blueprint(mngr_sett_bp)
    app.register_blueprint(card_summary_bp)
    app.register_blueprint(data_report_bp)
    app.register_blueprint(data_definition_bp)  # 추가
```

## 3. JavaScript 모듈 분리

### 파일: `static/data-definition/data_definition.js`

```javascript
// static/data-definition/data_definition.js
// 이 파일은 data_definition_mock.html의 <script> 섹션을 별도 모듈로 분리한 것입니다.

// Global Variables
let dataTable;
let currentEditData = null;
let isEditing = false;

// Configuration
const API_BASE_URL = '/api/data-definition';
const DEFAULT_SETTINGS = {
    cnn_failr_thrs_val: 5,
    cnn_warn_thrs_val: 3,
    cnn_failr_icon_id: 2,
    cnn_failr_wrd_colr: '#dc3545',
    cnn_warn_icon_id: 5,
    cnn_warn_wrd_colr: '#ffc107',
    cnn_sucs_icon_id: 1,
    cnn_sucs_wrd_colr: '#28a745',
    dly_sucs_rt_thrs_val: 95.0,
    dd7_sucs_rt_thrs_val: 90.0,
    mthl_sucs_rt_thrs_val: 85.0,
    mc6_sucs_rt_thrs_val: 80.0,
    yy1_sucs_rt_thrs_val: 75.0,
    sucs_rt_sucs_icon_id: 1,
    sucs_rt_sucs_wrd_colr: '#28a745',
    sucs_rt_warn_icon_id: 5,
    sucs_rt_warn_wrd_colr: '#ffc107',
    chrt_colr: '#007bff',
    chrt_dsp_yn: 'Y',
    grass_chrt_min_colr: '#9be9a8',
    grass_chrt_max_colr: '#216e39'
};

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeDataTable();
    loadInitialData();
    setupEventListeners();
});

// DataTable Initialization
function initializeDataTable() {
    dataTable = $('#dataTable').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/ko.json'
        },
        pageLength: 10,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, '전체']],
        responsive: true,
        ordering: true,
        searching: true,
        paging: true,
        info: true,
        autoWidth: false,
        columnDefs: [
            { targets: [0, 1, 2, 3], orderable: true },
            { targets: [4, 5, 6, 7, 8, 9, 10, 11, 12, 13], orderable: false },
            { targets: [14], orderable: false, searchable: false }
        ],
        dom: '<"row"<"col-md-6"l><"col-md-6"f>>rt<"row"<"col-md-5"i><"col-md-7"p>>',
        drawCallback: function() {
            updateStatistics();
        }
    });
}

// Event Listeners Setup
function setupEventListeners() {
    // Form submission
    document.getElementById('dataForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('modalForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveModalData();
    });

    // Input validation
    document.getElementById('formCd').addEventListener('input', validateCdInput);
    document.getElementById('modalFormCd').addEventListener('input', validateCdInput);

    // Modal events
    const modal = document.getElementById('dataModal');
    modal.addEventListener('hidden.bs.modal', function() {
        resetModalForm();
    });
}

// Load Initial Data
async function loadInitialData() {
    showLoading(true);
    try {
        const data = await fetchAllData();
        renderDataTable(data);
        updateStatistics();
        showToast('데이터를 성공적으로 로드했습니다.', 'success');
    } catch (error) {
        console.error('Error loading data:', error);
        showToast('데이터 로드에 실패했습니다.', 'error');
    } finally {
        showLoading(false);
    }
}

// API Functions
async function fetchAllData() {
    const response = await fetch(`${API_BASE_URL}/list`);
    if (!response.ok) {
        throw new Error('데이터를 가져오는 데 실패했습니다.');
    }
    return await response.json();
}

async function createData(data) {
    const response = await fetch(`${API_BASE_URL}/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || '데이터 생성에 실패했습니다.');
    }
    return await response.json();
}

async function updateData(cdCl, cd, data) {
    const response = await fetch(`${API_BASE_URL}/update/${cdCl}/${cd}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || '데이터 수정에 실패했습니다.');
    }
    return await response.json();
}

async function deleteData(cdCl, cd) {
    const response = await fetch(`${API_BASE_URL}/delete/${cdCl}/${cd}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || '데이터 삭제에 실패했습니다.');
    }
    return await response.json();
}

// UI Functions
function renderDataTable(data) {
    if (!data || !Array.isArray(data)) {
        data = [];
    }

    // Clear existing data
    dataTable.clear();

    // Add new data
    data.forEach(item => {
        const row = createTableRow(item);
        dataTable.row.add(row);
    });

    // Draw table
    dataTable.draw();
}

function createTableRow(item) {
    const actions = `
        <div class="action-buttons">
            <button class="btn btn-sm btn-outline-primary" onclick="editData('${item.cd_cl}', '${item.cd}')">
                <i class="fas fa-edit"></i> 수정
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteDataConfirm('${item.cd_cl}', '${item.cd}', '${item.cd_nm}')">
                <i class="fas fa-trash"></i> 삭제
            </button>
        </div>
    `;

    return [
        `<span class="fw-bold">${item.cd || ''}</span>`,
        item.cd_nm || '',
        item.cd_desc || '',
        item.item5 || '',
        item.item1 || '',
        item.item2 || '',
        item.item3 || '',
        item.item4 || '',
        item.item6 || '',
        item.item7 || '',
        item.item8 || '',
        item.item9 || '',
        item.item10 || '',
        actions
    ];
}

function updateStatistics() {
    const totalRows = dataTable.rows().count();
    const activeRows = totalRows; // Assuming all rows are active
    const restrictedCount = calculateRestrictedCount();
    
    document.getElementById('totalDataCount').textContent = totalRows;
    document.getElementById('activeDataCount').textContent = activeRows;
    document.getElementById('restrictedCount').textContent = restrictedCount;
    document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ko-KR');
}

function calculateRestrictedCount() {
    let count = 0;
    dataTable.rows().every(function() {
        const data = this.data();
        const cd = data[0];
        if (isRestrictedCd(cd)) {
            count++;
        }
    });
    return count;
}

// Form Functions
function showAddModal() {
    isEditing = false;
    document.getElementById('dataModalLabel').textContent = '데이터 추가';
    const modal = new bootstrap.Modal(document.getElementById('dataModal'));
    modal.show();
}

function editData(cdCl, cd) {
    isEditing = true;
    document.getElementById('dataModalLabel').textContent = '데이터 수정';
    
    // Find the data item
    const data = dataTable.rows().data().toArray();
    const item = data.find(row => row[0] === cd);
    
    if (item) {
        populateModalForm(item);
        const modal = new bootstrap.Modal(document.getElementById('dataModal'));
        modal.show();
    }
}

function populateModalForm(item) {
    document.getElementById('modalFormCd').value = item[0] || '';
    document.getElementById('modalFormCdNm').value = item[1] || '';
    document.getElementById('modalFormCdDesc').value = item[2] || '';
    document.getElementById('modalFormItem5').value = item[3] || '';
    document.getElementById('modalFormItem1').value = item[4] || '';
    document.getElementById('modalFormItem2').value = item[5] || '';
    document.getElementById('modalFormItem3').value = item[6] || '';
    document.getElementById('modalFormItem4').value = item[7] || '';
    document.getElementById('modalFormItem6').value = item[8] || '';
    document.getElementById('modalFormItem7').value = item[9] || '';
    document.getElementById('modalFormItem8').value = item[10] || '';
    document.getElementById('modalFormItem9').value = item[11] || '';
    document.getElementById('modalFormItem10').value = item[12] || '';
}

function resetModalForm() {
    document.getElementById('modalForm').reset();
    document.getElementById('cdError').style.display = 'none';
    isEditing = false;
}

// Validation Functions
function validateCdInput(event) {
    const input = event.target;
    const value = input.value;
    const errorDiv = document.getElementById('cdError');
    
    if (!value.startsWith('CD')) {
        showError(input, 'CD로 시작해야 합니다.');
        return false;
    }
    
    if (value.length > 2) {
        const cdNumber = parseInt(value.substring(2));
        if ((cdNumber >= 900 && cdNumber <= 999) || (cdNumber % 100 === 0)) {
            showError(input, 'CD900-CD999 범위와 100의 배수는 사용할 수 없습니다.');
            return false;
        }
    }
    
    hideError(input);
    return true;
}

function showError(input, message) {
    const errorDiv = document.getElementById('cdError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    input.classList.add('is-invalid');
}

function hideError(input) {
    const errorDiv = document.getElementById('cdError');
    errorDiv.style.display = 'none';
    input.classList.remove('is-invalid');
}

function isRestrictedCd(cd) {
    if (!cd || !cd.startsWith('CD')) return false;
    const cdNumber = parseInt(cd.substring(2));
    return (cdNumber >= 900 && cdNumber <= 999) || (cdNumber % 100 === 0);
}

// Save Functions
async function saveModalData() {
    const cd = document.getElementById('modalFormCd').value;
    const cdNm = document.getElementById('modalFormCdNm').value;
    
    if (!cd || !cdNm) {
        showToast('필수 필드를 모두 입력해주세요.', 'warning');
        return;
    }
    
    if (!validateCdInput({ target: document.getElementById('modalFormCd') })) {
        return;
    }

    const data = {
        cd_cl: document.getElementById('modalFormCdCl').value,
        cd: cd,
        cd_nm: cdNm,
        cd_desc: document.getElementById('modalFormCdDesc').value,
        item1: document.getElementById('modalFormItem1').value,
        item2: document.getElementById('modalFormItem2').value,
        item3: document.getElementById('modalFormItem3').value,
        item4: document.getElementById('modalFormItem4').value,
        item5: document.getElementById('modalFormItem5').value,
        item6: document.getElementById('modalFormItem6').value,
        item7: document.getElementById('modalFormItem7').value,
        item8: document.getElementById('modalFormItem8').value,
        item9: document.getElementById('modalFormItem9').value,
        item10: document.getElementById('modalFormItem10').value
    };

    showLoading(true);
    try {
        if (isEditing) {
            // Update existing data
            await updateData(data.cd_cl, data.cd, data);
            showToast('데이터가 성공적으로 수정되었습니다.', 'success');
        } else {
            // Create new data
            await createData(data);
            showToast('데이터가 성공적으로 추가되었습니다.', 'success');
        }
        
        // Refresh data
        await loadInitialData();
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('dataModal'));
        modal.hide();
        
    } catch (error) {
        console.error('Error saving data:', error);
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Delete Functions
function deleteDataConfirm(cdCl, cd, cdNm) {
    if (confirm(`'${cdNm}' 데이터를 정말로 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.`)) {
        deleteDataHandler(cdCl, cd);
    }
}

async function deleteDataHandler(cdCl, cd) {
    showLoading(true);
    try {
        await deleteData(cdCl, cd);
        showToast('데이터가 성공적으로 삭제되었습니다.', 'success');
        await loadInitialData();
    } catch (error) {
        console.error('Error deleting data:', error);
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Utility Functions
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.style.display = 'flex';
    } else {
        overlay.style.display = 'none';
    }
}

function showToast(message, type = 'info') {
    const toastEl = document.getElementById('liveToast');
    const toastBody = document.getElementById('toastMessage');
    const toastHeader = toastEl.querySelector('.toast-header');
    
    // Set message
    toastBody.textContent = message;
    
    // Set type colors
    const icon = toastHeader.querySelector('i');
    toastHeader.className = 'toast-header';
    icon.className = 'me-2';
    
    switch(type) {
        case 'success':
            toastHeader.classList.add('text-success');
            icon.classList.add('text-success', 'fas', 'fa-check-circle');
            break;
        case 'error':
            toastHeader.classList.add('text-danger');
            icon.classList.add('text-danger', 'fas', 'fa-exclamation-circle');
            break;
        case 'warning':
            toastHeader.classList.add('text-warning');
            icon.classList.add('text-warning', 'fas', 'fa-exclamation-triangle');
            break;
        default:
            toastHeader.classList.add('text-primary');
            icon.classList.add('text-primary', 'fas', 'fa-info-circle');
    }
    
    // Show toast
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

function refreshData() {
    loadInitialData();
}

function exportCSV() {
    const data = dataTable.rows().data().toArray();
    if (data.length === 0) {
        showToast('내보낼 데이터가 없습니다.', 'warning');
        return;
    }

    // Create CSV content
    const headers = ['CD_CL', 'CD', 'CD_NM', 'CD_DESC', 'ITEM1', 'ITEM2', 'ITEM3', 'ITEM4', 'ITEM5', 'ITEM6', 'ITEM7', 'ITEM8', 'ITEM9', 'ITEM10'];
    const csvContent = [
        headers.join(','),
        ...data.map(row => row.slice(0, 14).map(cell => `"${cell.replace(/"/g, '""')}"`).join(','))
    ].join('\n');

    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `data_definition_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('CSV 파일이 다운로드되었습니다.', 'success');
}

// Global Functions for onclick events
window.showAddModal = showAddModal;
window.editData = editData;
window.deleteDataConfirm = deleteDataConfirm;
window.refreshData = refreshData;
window.exportCSV = exportCSV;
```

## 4. CSS 스타일 분리

### 파일: `static/data-definition/data_definition.css`

```css
/* static/data-definition/data_definition.css */
/* 이 파일은 data_definition_mock.html의 <style> 섹션을 별도 CSS 파일로 분리한 것입니다. */

:root {
    --primary-color: #007bff;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    --dark-color: #343a40;
    --light-color: #f8f9fa;
}

body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 0;
    margin-bottom: 2rem;
}

.header-section h1 {
    font-size: 2.5rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.btn-custom {
    border-radius: 25px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-custom:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.table-container {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.data-table th {
    background-color: #f8f9fa;
    border-bottom: 2px solid #dee2e6;
    font-weight: 600;
    color: #495057;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}

.data-table td {
    border-bottom: 1px solid #dee2e6;
    vertical-align: middle;
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.form-container {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
}

.form-label {
    font-weight: 600;
    color: #495057;
}

.form-control, .form-select {
    border-radius: 10px;
    border: 2px solid #e9ecef;
    padding: 0.75rem;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    transform: translateY(-1px);
}

.modal-content {
    border-radius: 15px;
    border: none;
}

.modal-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom: none;
    border-radius: 15px 15px 0 0;
}

.modal-footer {
    border-top: none;
    border-radius: 0 0 15px 15px;
}

.alert-custom {
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    backdrop-filter: blur(5px);
}

.spinner-custom {
    width: 3rem;
    height: 3rem;
    border: 0.5rem solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}

.btn-icon {
    margin-right: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header-section h1 {
        font-size: 2rem;
    }
    
    .table-container {
        padding: 1rem;
    }
    
    .form-container {
        padding: 1.5rem;
    }
}
```

## 5. 기존 파일 수정

### 파일: `templates/mngr_sett.html`

데이터정의 탭 내용을 간소화하여 독립 파일로 이동:

```html
<!-- 기존 데이터정의 탭 내용을 다음과 같이 변경 -->
<div id="dataDefinition" class="tab-content">
    <div class="content-section">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">데이터정의</h2>
        <p class="text-gray-600 mb-4">데이터정의 기능은 독립적인 페이지로 제공됩니다.</p>
        <div class="flex gap-4">
            <a href="/data-definition" class="btn btn-primary">
                <i class="fas fa-external-link-alt"></i>
                독립 데이터정의 페이지로 이동
            </a>
            <button onclick="openDataDefinitionModal()" class="btn btn-secondary">
                <i class="fas fa-window-restore"></i>
                모달로 열기
            </button>
        </div>
    </div>
</div>
```

### 파일: `routes/mngr_sett_routes.py`

데이터정의 페이지 라우트 추가:

```python
# routes/mngr_sett_routes.py
from flask import render_template, request, jsonify, session
from routes.auth_routes import login_required, check_password_change_required
from msys.database import get_db_connection
from service.data_definition_service import DataDefinitionService

@bp.route('/data-definition')
@login_required
@check_password_change_required
def data_definition_page():
    """데이터정의 페이지를 렌더링합니다."""
    return render_template('data_definition_mock.html')
```

## 6. 테스트 절차

### 6.1 API 테스트

1. **데이터 목록 조회 테스트**
   ```bash
   curl -X GET http://localhost:5000/api/data-definition/list
   ```

2. **데이터 생성 테스트**
   ```bash
   curl -X POST http://localhost:5000/api/data-definition/create \
   -H "Content-Type: application/json" \
   -d '{
       "cd_cl": "CD001",
       "cd": "CD123",
       "cd_nm": "테스트 Job",
       "cd_desc": "테스트 설명",
       "item1": "값1",
       "item2": "값2"
   }'
   ```

3. **데이터 수정 테스트**
   ```bash
   curl -X POST http://localhost:5000/api/data-definition/update/CD001/CD123 \
   -H "Content-Type: application/json" \
   -d '{
       "cd_nm": "수정된 Job",
       "cd_desc": "수정된 설명"
   }'
   ```

4. **데이터 삭제 테스트**
   ```bash
   curl -X DELETE http://localhost:5000/api/data-definition/delete/CD001/CD123
   ```

### 6.2 UI 테스트

1. **페이지 접근 테스트**
   - `/data-definition` 페이지 접근
   - 데이터 목록 표시 확인
   - 검색, 정렬, 페이지네이션 기능 테스트

2. **CRUD 기능 테스트**
   - 데이터 추가 기능 테스트
   - 데이터 수정 기능 테스트
   - 데이터 삭제 기능 테스트
   - 유효성 검사 기능 테스트

3. **CSV 내보내기 테스트**
   - CSV 파일 다운로드 기능 테스트
   - 파일 내용 확인

## 7. 보안 고려사항

### 7.1 인증 및 권한
- 모든 API 엔드포인트에 `@login_required` 데코레이터 적용
- `@check_password_change_required` 데코레이터로 비밀번호 변경 확인
- 관리자 권한 확인 로직 추가 (필요 시)

### 7.2 입력 검증
- CD 형식 검증 (CD로 시작, 금지 범위 확인)
- SQL 인젝션 방지 (파라미터화된 쿼리 사용)
- XSS 공격 방지 (입력값 검증 및 이스케이프)

### 7.3 로깅
- 모든 API 호출 로깅
- 에러 상황 상세 로깅
- 사용자 작업 이력 로깅

## 8. 성능 최적화

### 8.1 데이터베이스 쿼리 최적화
- 인덱스 활용
- 불필요한 JOIN 회피
- 페이징 처리

### 8.2 프런트엔드 최적화
- DataTables 페이징 활용
- 검색 결과 캐싱
- 불필요한 렌더링 방지

## 9. 배포 체크리스트

- [ ] 새로운 라우트 파일 생성 및 등록
- [ ] JavaScript 모듈 분리
- [ ] CSS 스타일 분리
- [ ] 기존 파일 수정
- [ ] API 테스트 완료
- [ ] UI 테스트 완료
- [ ] 보안 검증 완료
- [ ] 성능 테스트 완료
- [ ] 문서 업데이트 완료

## 10. 문제 해결

### 10.1 흔한 문제 및 해결책

1. **API 호출 실패**
   - CORS 설정 확인
   - 인증 토큰 확인
   - 네트워크 연결 확인

2. **데이터 표시 안됨**
   - 데이터베이스 연결 확인
   - 쿼리 로그 확인
   - JSON 형식 확인

3. **UI 렌더링 오류**
   - JavaScript 오류 확인
   - CSS 로딩 확인
   - 브라우저 호환성 확인

### 10.2 디버깅 팁

1. **브라우저 개발자 도구 활용**
   - Network 탭에서 API 호출 확인
   - Console 탭에서 JavaScript 오류 확인
   - Elements 탭에서 DOM 구조 확인

2. **서버 로그 확인**
   - Flask 개발 서버 로그 확인
   - 데이터베이스 로그 확인
   - 에러 상세 내용 확인

이 가이드를 따라 구현하면 독립적인 HTML 목업을 실제 시스템에 성공적으로 적용할 수 있습니다.