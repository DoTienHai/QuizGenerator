/**
 * List Quizzes - Display all available quizzes in table format with pagination
 */

const PER_PAGE = 10;
let currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    loadQuizzes(currentPage);
});

async function loadQuizzes(page) {
    try {
        const response = await fetch(`/api/quizzes?page=${page}&per_page=${PER_PAGE}`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.message || 'Lỗi tải quiz');
        }

        const quizzes = data.data || [];
        const pagination = data.pagination || {};
        const quizTable = document.getElementById('quizTable');
        const quizTableBody = document.getElementById('quizTableBody');
        const noQuizzesDiv = document.getElementById('noQuizzes');

        if (quizzes.length === 0 && page === 1) {
            quizTable.style.display = 'none';
            noQuizzesDiv.style.display = 'block';
            renderPagination(pagination);
            return;
        }

        quizTable.style.display = 'table';
        noQuizzesDiv.style.display = 'none';
        quizTableBody.innerHTML = '';

        const offset = (page - 1) * PER_PAGE;
        quizzes.forEach((quiz, index) => {
            const uploadedDate = new Date(quiz.uploaded_at).toLocaleString('vi-VN') || 'N/A';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="text-align: center; font-weight: bold;">${offset + index + 1}</td>
                <td>${quiz.name || `Quiz #${quiz.quiz_id}`}</td>
                <td style="text-align: center;">
                    <span style="background-color: #e7f3ff; color: #0066cc; padding: 4px 8px; border-radius: 4px;">
                        📚 ${quiz.total_questions || 0}
                    </span>
                </td>
                <td style="text-align: center; font-size: 0.9em; color: #666;">${uploadedDate}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-success" onclick="startExam(${quiz.quiz_id}, '${quiz.name.replace(/'/g, "\\'")}', ${quiz.total_questions})">
                            🎮 Làm Bài
                        </button>
                        <button class="btn btn-secondary" onclick="viewQuizStats(${quiz.quiz_id}, '${quiz.name.replace(/'/g, "\\'")}')">
                            📈 Thống Kê
                        </button>
                    </div>
                </td>
            `;
            quizTableBody.appendChild(row);
        });

        renderPagination(pagination);

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

function renderPagination(pagination) {
    const container = document.getElementById('paginationContainer');
    if (!container) return;

    const { page, total_pages, total } = pagination;
    if (!total_pages || total_pages <= 1) {
        container.innerHTML = '';
        return;
    }

    container.innerHTML = `
        <div class="pagination-info">
            Trang ${page} / ${total_pages} &nbsp;(${total} quiz)
        </div>
        <div class="pagination-controls">
            <button class="btn btn-secondary" onclick="changePage(${page - 1})" ${page <= 1 ? 'disabled' : ''}>
                ← Trước
            </button>
            <button class="btn btn-secondary" onclick="changePage(${page + 1})" ${page >= total_pages ? 'disabled' : ''}>
                Tiếp →
            </button>
        </div>
    `;
}

function changePage(page) {
    currentPage = page;
    loadQuizzes(currentPage);
}

function startExam(quizId, quizName, totalQuestions) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    sessionStorage.setItem('selectedQuizTotal', totalQuestions);
    window.location.href = '/exam-do';
}

function viewQuizStats(quizId, quizName) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    window.location.href = '/quiz-stats';
}
