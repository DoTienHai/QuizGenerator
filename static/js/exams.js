/**
 * Exams - List and manage completed exams
 */

document.addEventListener('DOMContentLoaded', () => {
    loadCompletedExams();
});

/**
 * Load all completed exams
 */
async function loadCompletedExams() {
    try {
        const examsList = document.getElementById('examsList');
        
        const response = await fetch('/api/results');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải danh sách bài làm');
        }

        const results = data.data || [];

        if (results.length === 0) {
            examsList.innerHTML = '<p style="text-align: center; color: #999;">📭 Chưa có bài làm nào. Hãy bắt đầu làm bài!</p>';
            return;
        }

        let html = '<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">';
        
        results.forEach(result => {
            const scorePercent = result.total_questions ? Math.round((result.correct_count / result.total_questions) * 100) : 0;
            const scoreClass = scorePercent >= 80 ? 'success' : scorePercent >= 50 ? 'warning' : 'danger';
            
            html += `
                <div class="card" style="border-left: 4px solid #667eea;">
                    <h3 style="margin-top: 0; color: #667eea;">📚 ${result.quiz_name}</h3>
                    
                    <div style="background: #f0f4ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <div style="font-size: 24px; font-weight: bold; color: #667eea;">${scorePercent}%</div>
                        <div style="font-size: 12px; color: #999;">Điểm</div>
                    </div>
                    
                    <div style="margin: 15px 0; line-height: 1.8;">
                        <p><strong>✅ Đúng:</strong> ${result.correct_count}/${result.total_questions}</p>
                        <p><strong>❌ Sai:</strong> ${result.incorrect_count}</p>
                        <p><strong>⏭️ Bỏ qua:</strong> ${result.skipped_count}</p>
                    </div>
                    
                    <div style="color: #999; font-size: 12px; margin: 15px 0;">
                        <strong>📅 Ngày:</strong> ${new Date(result.submitted_at).toLocaleString('vi-VN')}
                    </div>
                    
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button class="btn btn-primary" style="flex: 1; padding: 10px;" onclick="viewResults('${result.session_id}')">
                            👁️ Xem Chi Tiết
                        </button>
                        <button class="btn btn-secondary" style="flex: 1; padding: 10px;" onclick="retakeExam(${result.quiz_id}, '${result.quiz_name}', ${result.num_questions}, ${result.exam_duration})">
                            🔄 Làm Lại
                        </button>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        examsList.innerHTML = html;

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
        examsList.innerHTML = '<p style="text-align: center; color: #999;">Lỗi tải danh sách bài làm</p>';
    }
}

/**
 * View exam results details
 */
function viewResults(sessionId) {
    sessionStorage.setItem('examSessionId', sessionId);
    window.location.href = '/results';
}

/**
 * Retake exam for same quiz with same parameters
 */
function retakeExam(quizId, quizName, numQuestions, examDuration) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    sessionStorage.setItem('selectedNumQuestions', numQuestions);
    sessionStorage.setItem('selectedDuration', examDuration);
    window.location.href = '/exam-do';
}
