"""Common constants used across the application"""
from enum import Enum, auto

class Language(str, Enum):
    """Language options for interviews and tests"""
    ENGLISH = "English"
    CHINESE = "Chinese"
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]

class TestType(str, Enum):
    """Types of tests available in the system"""
    INTERVIEW = "interview"
    CODING = "coding"
    BEHAVIOR = "behavior"
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]

class Difficulty(str, Enum):
    """Difficulty levels for tests and questions"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]

class UserStatus(int, Enum):
    """User account status options"""
    ACTIVE = 0
    INACTIVE = 1
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]

class UserRole(int, Enum):
    """User role types in the system"""
    INTERVIEWER = 0
    INTERVIEWEE = 1
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]

class TestStatus(str, Enum):
    """Status options for tests"""
    OPEN = "open"
    ONGOING = "on-going"
    COMPLETED = "completed"
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls] 

class QuestionType(str, Enum):
    """Types of questions available in the system"""
    MULTIPLE_CHOICE = "multiple_choice"
    SINGLE_CHOICE = "single_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    
    @classmethod
    def choices(cls):
        return [member.value for member in cls]