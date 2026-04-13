/**
 * Results - Display exam results with detailed answer review
 */

let examData = null;

document.addEventListener('DOMContentLoaded', loadResults);

/**
 * Load and display exam results
 */
async function loadResults() {
    try {
        const sessionId = sessionStorage.getItem('examSessionId');

        if (!sessionId) {
            throw new Error('Không có session để xem kết quả');
        }

        // Fetch detailed answers with questions
        const response = await fetch(`/api/exams/${sessionId}/answers-detail`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải chi tiết kết quả');
        }

        examData = data.data;
        displayResults(data.data);
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('resultsContainer').style.display = 'block';

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('resultsContainer').innerHTML = `<p style="text-align: center; color: #999;">Lỗi tải kết quả</p>`;
    }
}

/**
 * Display results by populating HTML elements
 * @param {object} data - Result data with answers
 */
function displayResults(data) {
    const answers = data.answers || [];
    const score = data.score || 0;
    const status = data.status || 'PENDING';
    const submittedAt = data.submitted_at ? new Date(data.submitted_at).toLocaleString('vi-VN') : 'N/A';

    const correct = answers.filter(a => a.is_correct).length;
    const total = answers.length;
    const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;
    const statusText = status === 'PASS' ? '✅ ĐẬU' : '❌ KHÔNG ĐẬU';
    const statusColor = status === 'PASS' ? '#28a745' : '#dc3545';

    // Update score card
    document.getElementById('scorePercent').textContent = percentage + '%';
    document.getElementById('scoreStatus').textContent = statusText;
    document.getElementById('scoreStatus').style.color = statusColor;
    document.getElementById('scoreDetail').innerHTML = `Bạn trả lời đúng: <strong>${correct}/${total}</strong> câu`;
    document.getElementById('submittedAt').textContent = `Ngày làm: ${submittedAt}`;

    // Display detailed answers
    displayAnswers(answers);
}

/**
 * Display detailed answers for each question
 * @param {array} answers - Array of answer objects
 */
function displayAnswers(answers) {
    const answersContainer = document.getElementById('answersContainer');
    let answersHtml = '';

    if (answers.length === 0) {
        answersContainer.innerHTML = '<p style="text-align: center; color: #999;">Không có câu trả lời nào</p>';
        return;
    }

    answers.forEach((answer, index) => {
        const statusIcon = !answer.user_answer ? '❓' : answer.is_correct ? '✅' : '❌';
        const statusColor = !answer.user_answer ? '#999' : answer.is_correct ? '#48bb78' : '#f56565';

        const optionA = answer.option_a;
        const optionB = answer.option_b;
        const optionC = answer.option_c;
        const optionD = answer.option_d;

        const correctOptionText = {
            'A': optionA,
            'B': optionB,
            'C': optionC,
            'D': optionD
        }[answer.correct_answer] || '';

        const userOptionText = answer.user_answer ? {
            'A': optionA,
            'B': optionB,
            'C': optionC,
            'D': optionD
        }[answer.user_answer] || '' : '';

        answersHtml += `
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid ${statusColor};">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <h4 style="margin: 0; color: #333; flex: 1;">
                        ${index + 1}. ${answer.question_text}
                    </h4>
                    <span style="color: ${statusColor}; font-size: 20px; margin-left: 10px;">${statusIcon}</span>
                </div>

                <div style="margin: 15px 0; background: white; padding: 15px; border-radius: 5px;">
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #667eea;">✅ Đáp án đúng:</strong>
                        <span style="color: #48bb78; font-weight: bold;">
                            ${answer.correct_answer} - ${correctOptionText}
                        </span>
                    </div>

                    <div style="margin-bottom: 12px;">
                        <strong style="color: #667eea;">👤 Đáp án bạn chọn:</strong>
                        <span style="color: ${statusColor}; font-weight: bold;">
                            ${answer.user_answer ? answer.user_answer + ' - ' + userOptionText : '(Bỏ qua)'}
                        </span>
                    </div>

                    ${!answer.is_correct && answer.user_answer ? `
                        <div style="background: #fff5f5; padding: 10px; border-radius: 5px; border-left: 3px solid #f56565;">
                            <strong style="color: #f56565;">⚠️ Sai:</strong> Bạn chọn <strong>${answer.user_answer}</strong> nhưng đáp án đúng là <strong>${answer.correct_answer}</strong>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    });

    answersContainer.innerHTML = answersHtml;
}

/**
 * Retake the same exam with same parameters
 */
async function retakeExam() {
    try {
        const sessionId = sessionStorage.getItem('examSessionId');
        
        if (!sessionId || !examData) {
            throw new Error('Không thể tìm thấy thông tin bài exam');
        }

        // Fetch exam session to get num_questions and duration
        const response = await fetch(`/api/exams/${sessionId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error('Lỗi tải thông tin exam');
        }

        const exam = data.data;

        // Get quiz name from stored data or fetch it
        let quizName = sessionStorage.getItem('selectedQuizName');
        if (!quizName) {
            // Try to fetch quiz info (fallback)
            const quizResponse = await fetch(`/api/quizzes/${examData.quiz_id}`);
            if (quizResponse.ok) {
                const quizData = await quizResponse.json();
                quizName = quizData.data.name;
            } else {
                quizName = `Quiz #${examData.quiz_id}`;
            }
        }

        // Set session storage with exam parameters
        sessionStorage.setItem('selectedQuizId', examData.quiz_id);
        sessionStorage.setItem('selectedQuizName', quizName);
        sessionStorage.setItem('selectedQuizTotal', exam.num_questions);
        sessionStorage.setItem('selectedNumQuestions', exam.num_questions);
        sessionStorage.setItem('selectedDuration', exam.exam_duration);

        // Redirect to exam page
        window.location.href = '/exam-do';

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}
