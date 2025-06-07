from mongoengine import Document, StringField, ListField
from api.constants.common import Language, QuestionType, Difficulty

class Question(Document):
    """Question document model"""
    
    # 题目编号 (question id), e.g. '1'
    question_id = StringField(required=True, unique=True)
    
    # 题目类型 (question type), e.g. 'multiple_choice'
    type = StringField(required=True, choices=QuestionType.choices())
    
    # 题目 (question), e.g. 'What is the capital of France?'
    question = StringField(required=True)
    
    # 答案 (answer), e.g. 'Paris'
    answer = StringField(required=True)
    
    # 考查要点 (examination points), e.g. ['React', 'JavaScript', 'CSS']
    examination_points = ListField(StringField())
    
    # 岗位名称 (job title), e.g. 'React Developer'
    job_title = StringField(required=True)
    
    # 语言 (language), e.g. 'English'
    language = StringField(required=True, choices=Language.choices())
    
    # 难度 (difficulty), e.g. 'easy'
    difficulty = StringField(required=True, choices=Difficulty.choices())
    
    meta = {
        'collection': 'ai_question',
        'indexes': [
            ('job_title', 'language'),
            'examination_points'
        ]
    } 