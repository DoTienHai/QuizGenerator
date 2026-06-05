/**
 * Quiz Stats - Display quiz statistics and exam results with server-side pagination
 */

let currentPage = 1;
const PER_PAGE = 10;

document.addEventListener('DOMContentLoaded', () => {
    loadQuizStats();
});

/**
 * Load quiz header and first page of results
 */
async function loadQuizStats() {
    const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
    const quizName = sessionStorage.getItem('selectedQuizName');

    if (!quizId) {
        showMessage('Không tìm thấy thông tin quiz', 'error');
        return;
    }

    document.getElementById('quizName').textContent = `📚 ${quizName}`;
    await loadPage(quizId, 1);
}

/**
 * Fetch one page of results from server and render everything
 */
async function loadPage(quizId, page) {
    try {
        const response = await fetch(`/api/results?quiz_id=${quizId}&page=${page}&per_page=${PER_PAGE}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải kết quả');
        }

        const { stats, pagination } = data;
        if (!stats || !pagination) {
            throw new Error('Cấu trúc response không hợp lệ');
        }

        document.getElementById('totalAttempts').textContent = stats.total_attempts;
        document.getElementById('passCount').textContent = stats.pass_count;
        document.getElementById('failCount').textContent = stats.fail_count;
        document.getElementById('avgScore').textContent = stats.avg_score.toFixed(1) + '%';

        renderTable(data.data);
        renderPagination(pagination);
        currentPage = pagination.page;

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Render the results table rows
 */
function renderTable(results) {
    const tableBody = document.getElementById('resultsTableBody');
    const noResults = document.getElementById('noResults');

    if (results.length === 0) {
        tableBody.style.display = 'none';
        noResults.style.display = 'block';
        return;
    }

    tableBody.style.display = 'table-row-group';
    noResults.style.display = 'none';
    tableBody.innerHTML = '';

    results.forEach(result => {
        const statusColor = result.status === 'PASS' ? '#48bb78' : '#f56565';
        const statusText = result.status === 'PASS' ? '✅ PASS' : '❌ FAIL';
        const total = result.correct_count + result.incorrect_count + result.skipped_count;

        const row = document.createElement('tr');
        row.style.borderBottom = '1px solid #e2e8f0';
        row.innerHTML = `
            <td style="padding: 12px; text-align: left;">
                ${new Date(result.submitted_at).toLocaleString('vi-VN')}
            </td>
            <td style="padding: 12px; text-align: center; font-weight: bold; color: #667eea;">
                ${result.score.toFixed(1)}%
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.correct_count}/${total}
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.incorrect_count}
            </td>
            <td style="padding: 12px; text-align: center;">
                ${result.skipped_count}
            </td>
            <td style="padding: 12px; text-align: center;">
                <span style="color: ${statusColor}; font-weight: bold;">
                    ${statusText}
                </span>
            </td>
            <td style="padding: 12px; text-align: center;">
                <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px;"
                        onclick="showExamDetails('${result.session_id}')">
                    👁️ Xem Chi Tiết
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

/**
 * Render prev/next pagination controls
 */
function renderPagination(pagination) {
    const controls = document.getElementById('paginationControls');

    if (pagination.total_pages <= 1) {
        controls.style.display = 'none';
        return;
    }

    controls.style.display = 'flex';
    document.getElementById('pageInfo').textContent =
        `Trang ${pagination.page} / ${pagination.total_pages} (${pagination.total} bài)`;
    document.getElementById('btnPrev').disabled = !pagination.has_prev;
    document.getElementById('btnNext').disabled = !pagination.has_next;
}

/**
 * Navigate to a specific page
 */
function goToPage(page) {
    const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
    loadPage(quizId, page);
}

/**
 * Show detailed exam results on separate page
 */
function showExamDetails(sessionId) {
    sessionStorage.setItem('examSessionId', sessionId);
    window.location.href = '/results';
}
