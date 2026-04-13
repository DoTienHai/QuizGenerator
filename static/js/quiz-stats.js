/**
 * Quiz Stats - Display quiz statistics and exam results
 */

document.addEventListener('DOMContentLoaded', () => {
    loadQuizStats();
});

/**
 * Load quiz statistics - calculated from actual exam results
 */
async function loadQuizStats() {
    try {
        const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
        const quizName = sessionStorage.getItem('selectedQuizName');

        if (!quizId) {
            showMessage('Không tìm thấy thông tin quiz', 'error');
            return;
        }

        // Update header
        document.getElementById('quizName').textContent = `📚 ${quizName}`;

        // Fetch all results
        const response = await fetch('/api/results');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải kết quả');
        }

        const allResults = data.data || [];
        // Filter results for this quiz only
        const quizResults = allResults.filter(r => r.quiz_id === quizId);

        // Calculate statistics from actual results
        let stats = {
            total_attempts: 0,
            pass_count: 0,
            average_score: 0,
            total_correct: 0,
            total_incorrect: 0,
            total_skipped: 0
        };

        if (quizResults.length > 0) {
            stats.total_attempts = quizResults.length;
            stats.pass_count = quizResults.filter(r => r.status === 'PASS').length;
            
            let totalScore = 0;
            quizResults.forEach(result => {
                totalScore += result.score;
                stats.total_correct += result.correct_count;
                stats.total_incorrect += result.incorrect_count;
                stats.total_skipped += result.skipped_count;
            });
            
            stats.average_score = totalScore / quizResults.length;
        }

        // Update stat cards
        document.getElementById('totalAttempts').textContent = stats.total_attempts;
        document.getElementById('passCount').textContent = stats.pass_count;
        document.getElementById('failCount').textContent = stats.total_attempts - stats.pass_count;
        document.getElementById('avgScore').textContent = stats.average_score.toFixed(1) + '%';

        // Load and display results table
        loadQuizResults(quizId, quizResults);

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Load and display quiz results
 */
function loadQuizResults(quizId, quizResults) {
    try {
        const tableBody = document.getElementById('resultsTableBody');
        const noResults = document.getElementById('noResults');

        if (quizResults.length === 0) {
            tableBody.style.display = 'none';
            noResults.style.display = 'block';
            return;
        }

        tableBody.style.display = 'table-row-group';
        noResults.style.display = 'none';
        tableBody.innerHTML = '';

        quizResults.forEach(result => {
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

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Show detailed exam results on separate page
 * @param {string} sessionId - Exam session ID
 */
function showExamDetails(sessionId) {
    sessionStorage.setItem('examSessionId', sessionId);
    window.location.href = '/results';
}
