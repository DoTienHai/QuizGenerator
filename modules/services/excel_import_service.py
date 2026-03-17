"""
ExcelImportService: Excel file parsing and import logic
Handles reading Excel files and creating quizzes from them
"""

import openpyxl
from io import BytesIO
from ..models import db, Quiz, Question
from .validation_service import ValidationService
from .quiz_service import QuizService


class ExcelImportService:
    """Service for importing quizzes from Excel files"""

    # Excel sheet structure constants
    QUESTION_COLUMN = 1      # Column A: Question text
    OPTION_A_COLUMN = 2      # Column B: Option A
    OPTION_B_COLUMN = 3      # Column C: Option B
    OPTION_C_COLUMN = 4      # Column D: Option C
    OPTION_D_COLUMN = 5      # Column E: Option D
    CORRECT_ANSWER_COLUMN = 6  # Column F: Correct answer (A/B/C/D)
    DIFFICULTY_COLUMN = 7    # Column G: Difficulty (1-5, optional)
    
    DATA_START_ROW = 2       # Data starts from row 2 (row 1 is header)

    @staticmethod
    def validate_excel_file(file_content):
        """
        Validate Excel file format and structure
        Args: file_content (bytes) - Excel file content
        Returns:
            tuple (is_valid, error_message)
        """
        try:
            workbook = openpyxl.load_workbook(BytesIO(file_content))
            
            # Check if 'questions' sheet exists
            if 'questions' not in workbook.sheetnames:
                return False, "Excel file must contain a 'questions' sheet"
            
            worksheet = workbook['questions']
            
            # Check headers
            headers = [
                'Question',
                'Option A',
                'Option B',
                'Option C',
                'Option D',
                'Correct Answer',
                'Difficulty'
            ]
            
            for idx, expected_header in enumerate(headers, 1):
                cell_value = worksheet.cell(1, idx).value
                if not cell_value or str(cell_value).strip() != expected_header:
                    return False, f"Column {chr(64+idx)} header should be '{expected_header}'"
            
            # Check for at least one data row
            if worksheet.max_row < 2:
                return False, "Excel file must contain at least one question"
            
            return True, None
        
        except Exception as e:
            return False, f"Error validating Excel file: {str(e)}"

    @staticmethod
    def parse_excel_file(file_content, quiz_name):
        """
        Parse Excel file and extract questions
        Args:
            file_content (bytes) - Excel file content
            quiz_name (str) - Name for the quiz
        Returns:
            dict - {
                'success': bool,
                'data': questions_list or None,
                'message': str
            }
        """
        # Validate file structure first
        is_valid, error_msg = ExcelImportService.validate_excel_file(file_content)
        if not is_valid:
            return {'success': False, 'data': None, 'message': error_msg}
        
        try:
            workbook = openpyxl.load_workbook(BytesIO(file_content))
            worksheet = workbook['questions']
            
            questions = []
            
            # Read data rows
            for row_idx in range(ExcelImportService.DATA_START_ROW, worksheet.max_row + 1):
                # Get cell values
                question_text = worksheet.cell(row_idx, ExcelImportService.QUESTION_COLUMN).value
                option_a = worksheet.cell(row_idx, ExcelImportService.OPTION_A_COLUMN).value
                option_b = worksheet.cell(row_idx, ExcelImportService.OPTION_B_COLUMN).value
                option_c = worksheet.cell(row_idx, ExcelImportService.OPTION_C_COLUMN).value
                option_d = worksheet.cell(row_idx, ExcelImportService.OPTION_D_COLUMN).value
                correct_answer = worksheet.cell(row_idx, ExcelImportService.CORRECT_ANSWER_COLUMN).value
                difficulty = worksheet.cell(row_idx, ExcelImportService.DIFFICULTY_COLUMN).value
                
                # Skip empty rows
                if not question_text:
                    continue
                
                # Validate and create question
                question_data = {
                    'question_text': str(question_text).strip(),
                    'option_a': str(option_a).strip() if option_a else '',
                    'option_b': str(option_b).strip() if option_b else '',
                    'option_c': str(option_c).strip() if option_c else '',
                    'option_d': str(option_d).strip() if option_d else '',
                    'correct_answer': str(correct_answer).upper().strip() if correct_answer else 'A',
                    'difficulty': int(difficulty) if difficulty else 3
                }
                
                # Validate question
                is_valid, error_msg = ValidationService.validate_question_format(question_data)
                if not is_valid:
                    return {
                        'success': False,
                        'data': None,
                        'message': f"Error in row {row_idx}: {error_msg}"
                    }
                
                questions.append(question_data)
            
            if not questions:
                return {
                    'success': False,
                    'data': None,
                    'message': "No valid questions found in Excel file"
                }
            
            return {
                'success': True,
                'data': questions,
                'message': f"Parsed {len(questions)} questions from Excel file"
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f"Error parsing Excel file: {str(e)}"
            }

    @staticmethod
    def import_excel_as_quiz(file_content, quiz_name):
        """
        Import Excel file directly as a new quiz
        Args:
            file_content (bytes) - Excel file content
            quiz_name (str) - Name for the new quiz
        Returns:
            dict - {
                'success': bool,
                'data': quiz_obj or None,
                'message': str
            }
        """
        # Parse the Excel file
        parse_result = ExcelImportService.parse_excel_file(file_content, quiz_name)
        if not parse_result['success']:
            return parse_result
        
        questions_data = parse_result['data']
        
        # Create quiz using QuizService
        result = QuizService.create_quiz(quiz_name, questions_data)
        
        return result

    @staticmethod
    def validate_excel_content(file_content):
        """
        Quick validation that Excel file is readable
        Args: file_content (bytes) - Excel file content
        Returns: tuple (is_valid, error_message)
        """
        try:
            workbook = openpyxl.load_workbook(BytesIO(file_content))
            
            if 'questions' not in workbook.sheetnames:
                return False, "Missing 'questions' sheet"
            
            worksheet = workbook['questions']
            
            if worksheet.max_row < 2:
                return False, "No data rows found"
            
            return True, None
        
        except openpyxl.utils.exceptions.InvalidFileException:
            return False, "Invalid Excel file format"
        except Exception as e:
            return False, f"Error reading Excel file: {str(e)}"

    @staticmethod
    def get_import_template():
        """
        Generate an Excel template for quiz import
        Args: None
        Returns:
            BytesIO - Excel file template
        """
        try:
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = 'questions'
            
            # Create headers
            headers = [
                'Question',
                'Option A',
                'Option B',
                'Option C',
                'Option D',
                'Correct Answer',
                'Difficulty'
            ]
            
            for col_idx, header in enumerate(headers, 1):
                cell = worksheet.cell(1, col_idx)
                cell.value = header
                # Make header bold
                from openpyxl.styles import Font
                cell.font = Font(bold=True)
            
            # Add sample row
            sample_data = [
                'What is 2 + 2?',
                '3',
                '4',
                '5',
                '6',
                'B',
                '1'
            ]
            
            for col_idx, value in enumerate(sample_data, 1):
                worksheet.cell(2, col_idx).value = value
            
            # Set column widths
            worksheet.column_dimensions['A'].width = 30
            worksheet.column_dimensions['B'].width = 25
            worksheet.column_dimensions['C'].width = 25
            worksheet.column_dimensions['D'].width = 25
            worksheet.column_dimensions['E'].width = 25
            worksheet.column_dimensions['F'].width = 15
            worksheet.column_dimensions['G'].width = 12
            
            # Write to BytesIO
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            
            return output
        
        except Exception as e:
            return None
