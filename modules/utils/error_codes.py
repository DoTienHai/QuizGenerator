"""
Error codes for API responses
"""

# Request validation errors
ERR_MISSING_FILE = ('MISSING_FILE', 'File not provided')
ERR_MISSING_PARAM = ('MISSING_PARAM', 'Required parameter missing')
ERR_INVALID_PARAM = ('INVALID_PARAM', 'Invalid parameter value')
ERR_INVALID_FILE_TYPE = ('INVALID_FILE_TYPE', 'Invalid file type')

# Resource not found
ERR_QUIZ_NOT_FOUND = ('QUIZ_NOT_FOUND', 'Quiz not found')
ERR_SESSION_NOT_FOUND = ('SESSION_NOT_FOUND', 'Session not found')
ERR_QUESTION_NOT_FOUND = ('QUESTION_NOT_FOUND', 'Question not found')

# Validation errors
ERR_SESSION_EXPIRED = ('SESSION_EXPIRED', 'Session has expired')
ERR_SESSION_ALREADY_SUBMITTED = ('SESSION_SUBMITTED', 'Session already submitted')
ERR_INVALID_ANSWER = ('INVALID_ANSWER', 'Invalid answer format')
ERR_VALIDATION_FAILED = ('VALIDATION_FAILED', 'Validation failed')

# Import/Processing errors
ERR_IMPORT_FAILED = ('IMPORT_FAILED', 'Failed to import quiz')
ERR_DUPLICATE_QUIZ = ('DUPLICATE_QUIZ', 'Quiz name already exists')
ERR_CALCULATION_ERROR = ('CALC_ERROR', 'Error calculating results')

# Server errors
ERR_INTERNAL = ('INTERNAL_ERROR', 'Internal server error')


def error_response(error_tuple, custom_message=None, status_code=400):
    """
    Create standardized error response
    
    Args:
        error_tuple: (error_code, default_message)
        custom_message: Optional custom message
        status_code: HTTP status code
    
    Returns:
        (dict, int): Response dict and status code
    """
    error_code, default_message = error_tuple
    message = custom_message or default_message
    
    response = {
        'success': False,
        'error_code': error_code,
        'message': message
    }
    
    return response, status_code


def success_response(data=None, message='Success', status_code=200):
    """
    Create standardized success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        (dict, int): Response dict and status code
    """
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    
    return response, status_code
