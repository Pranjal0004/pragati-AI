from typing import Optional, List
from api.model.db.test_result import TestResult
from api.utils.log_decorator import log

class TestResultRepository:
    @log
    async def create_result(self, result: TestResult) -> TestResult:
        """Create a new test result"""
        return result.save()
    
    @log
    async def get_result_by_test_id(self, test_id: str) -> Optional[TestResult]:
        """Get test result by test ID"""
        return TestResult.objects(test_id=test_id).first()
    
    @log
    async def get_results_by_user_id(self, user_id: str) -> List[TestResult]:
        """Get all test results for a user"""
        return TestResult.objects(user_id=user_id).all() 