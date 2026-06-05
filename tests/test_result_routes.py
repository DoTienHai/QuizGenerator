"""
Tests for paginated /api/results endpoint
Tests the list_results() function with pagination support
"""

import uuid
from datetime import datetime, timedelta
import pytest
from modules.models import db, Quiz, ExamSession, ExamResult


def _seed_results(db_instance, quiz_name='Test Quiz', count=15, pass_count=10):
    """Tạo quiz + N exam results trong DB test."""
    quiz = Quiz(name=quiz_name, total_questions=20)
    db_instance.session.add(quiz)
    db_instance.session.flush()

    for i in range(count):
        session_id = str(uuid.uuid4())
        session = ExamSession(
            session_id=session_id,
            quiz_id=quiz.quiz_id,
            num_questions=20,
            exam_duration=30,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=1),
            status='submitted'
        )
        db_instance.session.add(session)
        db_instance.session.flush()

        status = 'PASS' if i < pass_count else 'FAIL'
        score = 80.0 if status == 'PASS' else 40.0
        result = ExamResult(
            session_id=session_id,
            quiz_id=quiz.quiz_id,
            score=score,
            correct_count=16 if status == 'PASS' else 8,
            incorrect_count=4 if status == 'PASS' else 12,
            skipped_count=0,
            status=status,
            submitted_at=datetime.utcnow() - timedelta(minutes=i),
            time_spent_seconds=1200
        )
        db_instance.session.add(result)

    db_instance.session.commit()
    return quiz.quiz_id


class TestListResultsPaginated:
    """Test pagination for /api/results endpoint"""

    def test_list_results_paginated_returns_10_items(self, client, db):
        """Test that paginated request returns exactly 10 items on page 1"""
        quiz_id = _seed_results(db, count=15)

        response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['data']) == 10

    def test_list_results_paginated_returns_pagination_metadata(self, client, db):
        """Test that pagination metadata is correct"""
        quiz_id = _seed_results(db, count=15)

        response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
        data = response.get_json()

        pagination = data['pagination']
        assert pagination['page'] == 1
        assert pagination['per_page'] == 10
        assert pagination['total'] == 15
        assert pagination['total_pages'] == 2
        assert pagination['has_next'] is True
        assert pagination['has_prev'] is False

    def test_list_results_paginated_returns_correct_stats(self, client, db):
        """Test that stats are calculated correctly"""
        quiz_id = _seed_results(db, count=15, pass_count=10)

        response = client.get(f'/api/results?quiz_id={quiz_id}&page=1&per_page=10')
        data = response.get_json()

        stats = data['stats']
        assert stats['total_attempts'] == 15
        assert stats['pass_count'] == 10
        assert stats['fail_count'] == 5
        assert 'avg_score' in stats

    def test_list_results_paginated_page2_returns_remaining(self, client, db):
        """Test that page 2 returns the remaining 5 items"""
        quiz_id = _seed_results(db, count=15)

        response = client.get(f'/api/results?quiz_id={quiz_id}&page=2&per_page=10')
        data = response.get_json()

        assert response.status_code == 200
        assert len(data['data']) == 5
        assert data['pagination']['page'] == 2
        assert data['pagination']['has_next'] is False
        assert data['pagination']['has_prev'] is True

    def test_list_results_without_page_returns_all(self, client, db):
        """Test backward compatibility: without page param returns all results"""
        quiz_id = _seed_results(db, count=15)

        response = client.get(f'/api/results?quiz_id={quiz_id}')
        data = response.get_json()

        assert response.status_code == 200
        assert len(data['data']) == 15
        assert 'pagination' not in data
        assert 'stats' not in data
