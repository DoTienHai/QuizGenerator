/**
 * Utility function to show messages
 * @param {string} message - Message to display
 * @param {string} type - Message type: 'info', 'success', 'error' (default: 'info')
 */
function showMessage(message, type = 'info') {
    // Remove existing messages of the same type
    const main = document.querySelector('main');
    const existingMessages = main.querySelectorAll(`.message.${type}`);
    existingMessages.forEach(msg => msg.remove());

    const container = document.createElement('div');
    container.className = `message ${type}`;
    container.textContent = message;
    main.insertBefore(container, main.firstChild);

    if (type !== 'success' && type !== 'error') {
        setTimeout(() => container.remove(), 3000);
    }
}

/**
 * Utility function for API calls
 * @param {string} endpoint - API endpoint URL
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE) - default: 'GET'
 * @param {object} data - Request body data (optional)
 * @returns {Promise<object>} - Response data
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        showMessage(`Lỗi: ${error.message}`, 'error');
        throw error;
    }
}
