from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField
from datetime import datetime, UTC, timedelta
from api.constants.common import Language, TestType, Difficulty, TestStatus
from api.model.db.job import Job
from api.model.db.user import User

class Test(Document):
    """Test document model"""
    # Test identification
    test_id = StringField(required=True, unique=True)

    # 8 digits code
    activate_code = StringField(required=True, unique=True)
    
    # User information
    user_id = StringField(required=True)
    user_name = StringField()
    
    # Job information
    job_id = StringField(required=True)
    job_title = StringField()
    
    # Test configuration
    type = StringField(required=True, choices=TestType.choices())
    language = StringField(required=True, choices=Language.choices())
    difficulty = StringField(required=True, choices=Difficulty.choices())
    test_time = IntField(required=True, min_value=1, max_value=120)  # minutes
    examination_points = ListField(StringField())

    # Test questions
    question_ids = ListField(StringField(), default=[])
    
    # Test status
    status = StringField(
        required=True, 
        choices=TestStatus.choices(),
        default=TestStatus.OPEN.value
    )
    
    # Timestamps
    create_date = DateTimeField(default=lambda: datetime.now(UTC))
    start_date = DateTimeField(default=lambda: datetime.now(UTC))
    expire_date = DateTimeField(default=lambda: datetime.now(UTC) + timedelta(days=7))
    update_date = DateTimeField(default=lambda: datetime.now(UTC))
    close_date = DateTimeField()
    
    meta = {
        'collection': 'ai_test',
        'indexes': [
            'test_id',
            'activate_code',
            'user_id',
            'job_id',
            ('type', 'language', 'difficulty'),
            'status',
            'create_date'
        ]
    } 