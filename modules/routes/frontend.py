from flask import Blueprint, render_template, send_file
from openpyxl import Workbook
from io import BytesIO
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def upload():
    """Quiz upload page - Main landing page"""
    return render_template('upload.html')

@frontend_bp.route('/download-template')
def download_template():
    """Download Excel template for quiz creation"""
    # Path to template file
    template_path = os.path.join(
        os.path.dirname(__file__),
        '../../sample_data/Quiz_Template.xlsx'
    )
    
    # Check if file exists, if not create it
    if not os.path.exists(template_path):
        _create_template_file(template_path)
    
    return send_file(
        template_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Quiz_Template.xlsx'
    )


def _create_template_file(template_path):
    """Create template Excel file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "questions"
    
    # Add headers
    headers = ["Câu Hỏi", "Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D", "Đáp án Đúng", "Mức Độ Khó"]
    ws.append(headers)
    
    # Add sample row
    ws.append([
        "Thủ đô của Việt Nam là gì?",
        "Hà Nội",
        "Hồ Chí Minh",
        "Hải Phòng",
        "Đà Nẵng",
        "A",
        "1"
    ])
    
    # Set column widths
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 15
    
    # Save file
    wb.save(template_path)

@frontend_bp.route('/list-quizzes')
def list_quizzes():
    """List all available quizzes"""
    return render_template('list-quizzes.html')

@frontend_bp.route('/exam-do')
def exam_do():
    """Prepare and take exam"""
    return render_template('exam-do.html')

@frontend_bp.route('/results')
def results():
    """Show exam results"""
    return render_template('results.html')

@frontend_bp.route('/quiz-stats')
def quiz_stats():
    """Show quiz statistics and all exam results"""
    return render_template('quiz-stats.html')
