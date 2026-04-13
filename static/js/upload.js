/**
 * Upload Quiz - Handle file upload and quiz creation
 */

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('excelFile');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleUploadSubmit);
    }

    // Display selected file name
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileNameDisplay = document.getElementById('fileNameDisplay');
            const selectedFileName = document.getElementById('selectedFileName');
            
            if (this.files && this.files.length > 0) {
                selectedFileName.textContent = this.files[0].name;
                fileNameDisplay.classList.add('show');
            } else {
                fileNameDisplay.classList.remove('show');
            }
        });
    }
});

/**
 * Handle quiz file upload form submission
 */
async function handleUploadSubmit(e) {
    e.preventDefault();

    const quizName = document.getElementById('quizName').value;
    const excelFile = document.getElementById('excelFile').files[0];

    if (!excelFile) {
        showMessage('❌ Vui lòng chọn file Excel', 'error');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('quiz_name', quizName);
        formData.append('file', excelFile);

        const response = await fetch('/api/quizzes', {
            method: 'POST',
            body: formData
        });

        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            throw new Error(`Server error (${response.status}): ${text.substring(0, 100)}`);
        }

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.message || 'Lỗi upload file');
        }

        showMessage(`✅ Tải quiz "${quizName}" thành công!`, 'success');
        
        // Reset form
        document.getElementById('uploadForm').reset();
        document.getElementById('uploadProgress').style.display = 'none';

        // Redirect to quiz list after 2 seconds
        setTimeout(() => {
            window.location.href = '/list-quizzes';
        }, 2000);

    } catch (error) {
        showMessage(`❌ ${error.message}`, 'error');
        document.getElementById('uploadProgress').style.display = 'none';
    }
}
