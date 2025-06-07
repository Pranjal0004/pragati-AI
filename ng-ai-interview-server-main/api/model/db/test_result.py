from mongoengine import Document, StringField, IntField, FloatField, ListField, DictField
from datetime import datetime, UTC

class TestResult(Document):
    """Test result document model"""

    # Test id, e.g. '1234567890'
    test_id = StringField(required=True, unique=True)

    # User id, e.g. '1234567890'
    user_id = StringField(required=True)

    # Summary, e.g. 'Good job!' 
    summary = StringField(required=True)

    # Score, e.g. 80
    score = FloatField(required=True, min_value=0, max_value=100)

    # Question number, e.g. 10
    question_number = IntField(required=True, min_value=0)

    # Correct number, e.g. 8
    correct_number = IntField(required=True, min_value=0)

    # Elapse time, e.g. 10 minutes
    elapse_time = IntField(required=True, min_value=0)  # in minutes

    # Q&A history, e.g. [{'question': 'What is the capital of France?', 'answer': 'Paris'}]
    qa_history = ListField(DictField(), required=True)  # list of Q&A pairs
    
    meta = {
        'collection': 'ai_test_result',
        'indexes': [
            'test_id',
            'user_id',
            'score'
        ]
    } 