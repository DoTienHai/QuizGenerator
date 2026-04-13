/**
 * List Quizzes - Display all available quizzes in table format
 */

document.addEventListener('DOMContentLoaded', function() {
    loadQuizzes();
});

/**
 * Load and display all quizzes in table format
 */
async function loadQuizzes() {
    try {
        const response = await fetch('/api/quizzes');
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.message || 'Lỗi tải quiz');
        }

        const quizzes = data.data || [];
        const quizTable = document.getElementById('quizTable');
        const quizTableBody = document.getElementById('quizTableBody');
        const noQuizzesDiv = document.getElementById('noQuizzes');

        if (quizzes.length === 0) {
            quizTable.style.display = 'none';
            noQuizzesDiv.style.display = 'block';
            showMessage('Chưa có quiz nào. Hãy tải quiz mới!', 'info');
            return;
        }

        quizTable.style.display = 'table';
        noQuizzesDiv.style.display = 'none';
        quizTableBody.innerHTML = '';

        quizzes.forEach((quiz, index) => {
            const uploadedDate = new Date(quiz.uploaded_at).toLocaleString('vi-VN') || 'N/A';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="text-align: center; font-weight: bold;">${index + 1}</td>
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

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Start exam with selected quiz
 * @param {number} quizId - Quiz ID
 * @param {string} quizName - Quiz name
 * @param {number} totalQuestions - Total questions in quiz
 */
function startExam(quizId, quizName, totalQuestions) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    sessionStorage.setItem('selectedQuizTotal', totalQuestions);
    window.location.href = '/exam-do';
}

/**
 * View quiz statistics and results
 * @param {number} quizId - Quiz ID
 * @param {string} quizName - Quiz name
 */
function viewQuizStats(quizId, quizName) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    window.location.href = '/quiz-stats';
}
