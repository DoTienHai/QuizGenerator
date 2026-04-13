/**
 * Exam - Handle exam session and quiz submission
 */

let sessionId = null;
let remainingTime = 0;
let timerInterval = null;
let answers = {};
let selectedQuizData = null;

// Load quiz list on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedQuizId = sessionStorage.getItem('selectedQuizId');
    if (savedQuizId) {
        // User came from quiz list page
        loadConfigSection();
    } else {
        // User came directly to exam page - show quiz selection
        loadQuizzes();
    }

    const configForm = document.getElementById('configForm');
    if (configForm) {
        configForm.addEventListener('submit', handleConfigSubmit);
    }
});

/**
 * Load available quizzes for selection
 */
async function loadQuizzes() {
    try {
        const quizSelectSection = document.getElementById('quizSelectSection');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const quizListContainer = document.getElementById('quizList');

        const response = await fetch('/api/quizzes');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Lỗi tải danh sách Quiz');
        }

        const quizzes = data.data || [];

        if (quizzes.length === 0) {
            quizListContainer.innerHTML = '<p style="text-align: center; color: #999;">📭 Chưa có Quiz nào. Vui lòng tải Quiz trước!</p>';
            loadingSpinner.style.display = 'none';
            return;
        }

        loadingSpinner.style.display = 'none';
        quizListContainer.innerHTML = '';

        quizzes.forEach(quiz => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.cursor = 'pointer';
            card.style.transition = 'all 0.3s';
            card.innerHTML = `
                <h3>${quiz.name || `Quiz #${quiz.id}`}</h3>
                <p style="color: #666;">📚 <strong>${quiz.total_questions || 0}</strong> câu hỏi</p>
                <button type="button" class="btn btn-success" onclick="selectQuiz(${quiz.quiz_id}, '${quiz.name}', ${quiz.total_questions})">
                    ✅ Chọn Bộ Này
                </button>
            `;
            quizListContainer.appendChild(card);
        });

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Select a quiz
 * @param {number} quizId - Quiz ID
 * @param {string} quizName - Quiz name
 * @param {number} totalQuestions - Total number of questions
 */
function selectQuiz(quizId, quizName, totalQuestions) {
    sessionStorage.setItem('selectedQuizId', quizId);
    sessionStorage.setItem('selectedQuizName', quizName);
    sessionStorage.setItem('selectedQuizTotal', totalQuestions);

    selectedQuizData = {
        id: quizId,
        name: quizName,
        total_questions: totalQuestions
    };

    // Update max num_questions
    document.getElementById('numQuestions').max = totalQuestions;
    loadConfigSection();
}

/**
 * Load configuration section
 */
function loadConfigSection() {
    const quizSelectSection = document.getElementById('quizSelectSection');
    const configSection = document.getElementById('configSection');
    
    const quizName = sessionStorage.getItem('selectedQuizName') || 'Unknown';
    const totalQuestions = sessionStorage.getItem('selectedQuizTotal') || '0';
    const selectedNumQuestions = sessionStorage.getItem('selectedNumQuestions');
    const selectedDuration = sessionStorage.getItem('selectedDuration');
    const totalQuestionsInt = parseInt(totalQuestions);

    document.getElementById('quizNameDisplay').textContent = quizName;
    document.getElementById('totalQuestionsDisplay').textContent = totalQuestions;
    document.getElementById('numQuestions').max = totalQuestionsInt;
    document.getElementById('questionsRange').textContent = `(1-${totalQuestionsInt})`;

    // If coming from retake, pre-fill with same parameters
    if (selectedNumQuestions) {
        document.getElementById('numQuestions').value = selectedNumQuestions;
    }
    if (selectedDuration) {
        document.getElementById('duration').value = selectedDuration;
    }

    quizSelectSection.style.display = 'none';
    configSection.style.display = 'block';

    showMessage(`✅ Đã chọn: ${quizName}`, 'success');
}

/**
 * Handle config form submission
 */
async function handleConfigSubmit(e) {
    e.preventDefault();

    const quizId = parseInt(sessionStorage.getItem('selectedQuizId'));
    const numQuestions = parseInt(document.getElementById('numQuestions').value);
    const duration = parseInt(document.getElementById('duration').value);
    const totalQuestions = parseInt(sessionStorage.getItem('selectedQuizTotal'));

    // Validate
    if (numQuestions > totalQuestions) {
        showMessage(`❌ Số câu vượt quá tổng câu hỏi (${totalQuestions})`, 'error');
        return;
    }

    try {
        showMessage('Đang tạo bài kiểm tra...', 'info');

        const response = await fetch('/api/exams', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quiz_id: quizId,
                num_questions: numQuestions,
                duration_minutes: duration
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tạo bài kiểm tra');
        }

        sessionId = data.data.session_id;
        remainingTime = duration * 60;

        // Clean up retake parameters
        sessionStorage.removeItem('selectedNumQuestions');
        sessionStorage.removeItem('selectedDuration');

        // Load questions
        await loadQuestions(sessionId);

        // Hide config, show exam
        document.getElementById('configSection').style.display = 'none';
        document.getElementById('examSection').style.display = 'block';

        // Start timer
        startTimer();

        showMessage('✅ Bài kiểm tra đã tạo thành công!', 'success');

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Load and display questions
 * @param {string} sessionId - Session ID
 */
async function loadQuestions(sessionId) {
    try {
        const response = await fetch(`/api/exams/${sessionId}/questions`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Lỗi tải câu hỏi');
        }

        const questions = data.data || [];
        const container = document.getElementById('questionContainer');
        container.innerHTML = '';

        questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question-card';
            questionDiv.innerHTML = `
                <div class="question-text">
                    <span style="color: #667eea; font-weight: bold;">Câu ${index + 1}:</span>
                    ${question.question_text || 'Câu hỏi không có nội dung'}
                </div>
                <div class="options">
                    ${['A', 'B', 'C', 'D'].map(option => `
                        <label class="option">
                            <input type="radio" name="question_${question.question_id}" value="${option}" onchange="recordAnswer(${question.question_id}, '${option}')">
                            <span class="option-label">${option}. ${question[`option_${option.toLowerCase()}`] || 'N/A'}</span>
                        </label>
                    `).join('')}
                </div>
            `;
            container.appendChild(questionDiv);
        });

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
    }
}

/**
 * Record user answer
 * @param {number} questionId - Question ID
 * @param {string} answer - Answer (A, B, C, D)
 */
function recordAnswer(questionId, answer) {
    answers[questionId] = answer;
}

/**
 * Start exam timer
 */
function startTimer() {
    updateTimerDisplay();
    timerInterval = setInterval(() => {
        remainingTime--;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            autoSubmitExam();
            return;
        }

        updateTimerDisplay();

        // Warning at 5 minutes
        if (remainingTime === 300) {
            showMessage('⚠️ Còn 5 phút!', 'info');
        }
    }, 1000);
}

/**
 * Update timer display
 */
function updateTimerDisplay() {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    const timerElement = document.getElementById('timer');
    timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Change color based on time remaining
    if (remainingTime <= 60) {
        timerElement.classList.add('danger');
        timerElement.classList.remove('warning');
    } else if (remainingTime <= 300) {
        timerElement.classList.add('warning');
        timerElement.classList.remove('danger');
    } else {
        timerElement.classList.remove('danger', 'warning');
    }
}

/**
 * Submit exam
 */
async function submitExam() {
    if (!sessionId) {
        showMessage('❌ Session không hợp lệ', 'error');
        return;
    }

    if (Object.keys(answers).length === 0) {
        showMessage('⚠️ Bạn chưa trả lời câu nào', 'info');
        return;
    }

    try {
        clearInterval(timerInterval);
        showMessage('Đang nộp bài...', 'info');

        const submitResponse = await fetch(`/api/exams/${sessionId}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: answers })
        });

        const submitData = await submitResponse.json();

        if (!submitResponse.ok) {
            throw new Error(submitData.error || 'Lỗi nộp bài');
        }

        showMessage('✅ Nộp bài thành công!', 'success');

        // Store session and redirect to results
        sessionStorage.setItem('examSessionId', sessionId);
        setTimeout(() => {
            window.location.href = '/results';
        }, 1500);

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
        startTimer(); // Restart timer if error
    }
}

/**
 * Auto submit exam when time runs out
 */
async function autoSubmitExam() {
    showMessage('⏰ Hết thời gian! Đang nộp bài tự động...', 'info');
    await submitExam();
}

/**
 * Reset exam
 */
function resetExam() {
    if (confirm('Bạn có chắc muốn làm lại bài từ đầu?')) {
        clearInterval(timerInterval);
        sessionId = null;
        answers = {};
        document.getElementById('configSection').style.display = 'block';
        document.getElementById('examSection').style.display = 'none';
        document.getElementById('configForm').reset();
    }
}
