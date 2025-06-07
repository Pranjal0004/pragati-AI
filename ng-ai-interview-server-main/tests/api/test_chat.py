import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from api.main import app
import uuid
from api.service.chat import ChatService
from api.service.test_result import TestResultService
from api.model.api.chat import AnswerRequest, ChatResponse
from api.model.api.test_result import CreateTestResultRequest
from datetime import datetime
from agent.interview_response import InterviewResult
from agent.interview_response import QAResult
from agent.interview_response import Question
from agent.interview_response import QuestionType
from agent.interview_response import Answer

client = TestClient(app)

class TestChatAPI:
    """Chat API 测试类"""

    @patch("api.service.chat.ChatService.start_chat")
    def test_start_chat(self, mock_start_chat):
        """测试开始聊天"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        
        # 设置模拟返回值
        mock_response = {
            "feedback": "请介绍一下你的 Python 编程经验",
            "question_id": str(uuid.uuid4()),
            "type": "question"
        }
        mock_start_chat.return_value = mock_response
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/start",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "job_title": "Python 开发工程师",
                "examination_points": "Python, Django, Flask",
                "test_time": 60,
                "language": "Chinese",
                "difficulty": "medium"
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["feedback"] == mock_response["feedback"]
        assert data["data"]["question_id"] == mock_response["question_id"]
        assert data["data"]["type"] == "question"
        
        # 验证模拟调用
        mock_start_chat.assert_called_once()
        args, kwargs = mock_start_chat.call_args
        assert kwargs["user_id"] == user_id
        assert kwargs["test_id"] == test_id
        assert kwargs["job_title"] == "Python 开发工程师"
        assert kwargs["examination_points"] == "Python, Django, Flask"
        assert kwargs["test_time"] == 60
        assert kwargs["language"] == "Chinese"
        assert kwargs["difficulty"] == "medium"

    @patch("api.service.chat.build_graph")
    def test_answer_question_when_interview_is_over(self, mock_build_graph):
        """测试面试结束场景的问题回答接口"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        question_id = str(uuid.uuid4())
        user_answer = "这是最后一个问题的回答"
        
        # Mock workflow graph
        mock_graph = AsyncMock()
        mock_graph.return_value = {
            "interview_result": InterviewResult(
                summary="面试表现良好，技术基础扎实，表达清晰。",
                total_question_number=3,
                correct_question_number=2,
                score=85,
                interview_time=15
            ),
            "qa_history": [
                ("问题1", "回答1", QAResult(
                    question=Question(
                        question="描述Python的GIL?",
                        question_number=1,
                        question_type=QuestionType.ESSAY,
                        knowledge_point="Python基础",
                        answer="标准答案1"
                    ),
                    answer=Answer(
                        is_valid=True,
                        giveup=False,
                        suggest_more_details=False,
                        follow_up_question="",
                        feedback="回答不错",
                        is_correct=True,
                        analysis="分析1",
                        score=4
                    ),
                    is_interview_over=False,
                    summary="第一题回答正确"
                )),
                ("问题2", "回答2", QAResult(
                    question=Question(
                        question="解释装饰器原理",
                        question_number=2,
                        question_type=QuestionType.ESSAY,
                        knowledge_point="Python高级特性",
                        answer="标准答案2"
                    ),
                    answer=Answer(
                        is_valid=True,
                        giveup=False,
                        suggest_more_details=False,
                        follow_up_question="",
                        feedback="回答很好",
                        is_correct=True,
                        analysis="分析2",
                        score=5
                    ),
                    is_interview_over=False,
                    summary="第二题回答优秀"
                )),
                (question_id, user_answer, QAResult(
                    question=Question(
                        question="最后一个问题",
                        question_number=3,
                        question_type=QuestionType.ESSAY,
                        knowledge_point="系统设计",
                        answer="标准答案3"
                    ),
                    answer=Answer(
                        is_valid=True,
                        giveup=False,
                        suggest_more_details=False,
                        follow_up_question="",
                        feedback="面试结束。您的表现很好！",
                        is_correct=True,
                        analysis="分析3",
                        score=4
                    ),
                    is_interview_over=True,
                    summary="最后一题回答良好，面试结束"
                ))
            ],
            "messages": [],  # 这里可以添加消息历史
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "job_title": "Python开发工程师",
            "knowledge_points": "Python, 系统设计",
            "interview_time": 30,
            "language": "Chinese",
            "difficulty": "Medium",
            "question": None,  # 面试结束时没有下一个问题
            "feedback": "面试已结束。您的总分是85分，表现良好。",
            "user_answer": user_answer,
            "analyze_answer_response": None
        }
        mock_build_graph.return_value = mock_graph
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/answer",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "question_id": question_id,
                "user_answer": user_answer
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["is_finished"] == True
        assert data["data"]["score"] == 85
        assert "面试已结束" in data["data"]["feedback"]
        assert data["data"]["question"] is None
        
        # 验证 workflow 调用
        mock_build_graph.assert_called_once()
        mock_graph.assert_called_once()

    @patch("api.service.chat.build_graph")
    def test_answer_question_when_user_stops_interview(self, mock_build_graph):
        """测试用户主动结束面试场景的问题回答接口"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        question_id = str(uuid.uuid4())
        user_answer = "结束面试"  # 用户请求结束面试
        
        # Mock workflow graph
        mock_graph = AsyncMock()
        mock_graph.return_value = {
            "interview_result": None,  # 用户主动结束时可能没有完整的面试结果
            "qa_history": [
                ("问题1", "回答1", MagicMock(answer=MagicMock(score=80, feedback="不错"))),
                (question_id, user_answer, MagicMock(
                    answer=MagicMock(score=0, feedback="面试已结束"),
                    is_interview_over=True
                ))
            ]
        }
        mock_build_graph.return_value = mock_graph
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/answer",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "question_id": question_id,
                "user_answer": user_answer
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["is_finished"] == True
        assert data["data"]["score"] is not None
        assert "面试已结束" in data["data"]["feedback"]
        assert data["data"]["question"] is None
        
        # 验证 workflow 调用
        mock_build_graph.assert_called_once()
        mock_graph.assert_called_once()

    def test_answer_question_with_invalid_input(self):
        """测试无效输入的问题回答接口"""
        # 准备测试数据 - 缺少必要字段
        response = client.post(
            "/api/v1/chat/answer",
            json={
                "user_id": str(uuid.uuid4()),
                # 缺少 test_id
                "question_id": str(uuid.uuid4()),
                "user_answer": "回答内容"
            }
        )
        
        # 验证响应 - 应该返回 422 Unprocessable Entity
        assert response.status_code == 422

    @patch("api.service.chat.build_graph")
    def test_answer_question_service_error(self, mock_build_graph):
        """测试服务层错误的问题回答接口"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        question_id = str(uuid.uuid4())
        user_answer = "回答内容"
        
        # 模拟 workflow 抛出异常
        mock_graph = AsyncMock()
        mock_graph.side_effect = Exception("Workflow error")
        mock_build_graph.return_value = mock_graph
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/answer",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "question_id": question_id,
                "user_answer": user_answer
            }
        )
        
        # 验证响应 - 应该返回 500 Internal Server Error
        assert response.status_code == 500
        data = response.json()
        assert "error" in data["detail"].lower()
        
        # 验证 workflow 调用
        mock_build_graph.assert_called_once()
        mock_graph.assert_called_once()
