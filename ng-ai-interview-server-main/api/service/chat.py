from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import uuid4
from api.utils.log_decorator import log
from agent.workflow import build_graph
from langgraph.types import Command
from langgraph.types import StateSnapshot
from api.model.api.test_result import CreateTestResultRequest
from api.service.test_result import TestResultService
from agent.interview_response import InterviewResult
from loguru import logger
from api.service.test import TestService
from langgraph.graph import START


class ChatService:
    """Chat Service Class"""
    
    def __init__(self):
        """Initialize Chat Service"""
        self.workflow = build_graph()
        self.model_name = "gpt-4o"
        self.test_service = TestService()  # Add TestService instance
    
    @log
    async def start_chat(
        self,
        user_id: str,
        test_id: str,
        job_title: str,
        examination_points: str,
        test_time: int,
        language: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """
        Start Chat
        
        Args:
            user_id: User ID
            test_id: Test ID
            job_title: Job Title
            examination_points: Examination Points
            test_time: Test Time (minutes)
            language: Language
            difficulty: Difficulty
            
        Returns:
            Dict: Contains information about the first question
        """
        inputs = {
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "messages": [],
            "job_title": job_title,
            "knowledge_points": examination_points,
            "interview_time": test_time,
            "language": language,
            "difficulty": difficulty
        }

        config = {
            "configurable": {
                "thread_id": test_id, 
                "user_id": user_id
            },
            "model_name": self.model_name,
            # "model_name":"claude-3-5-sonnet",
            # "model_name": "gpt-4o",
            # "model_name": "deepseek-v3",
        }

        # Check if the test exists
        current: StateSnapshot = self.workflow.get_state(config)
        if current:
            # Workflow found
            (next,) = current.next if current.next else (None,)
            feedback = current.values["feedback"] if "feedback" in current.values.keys() else None
            question_id = str(uuid4())
            type = "question"
            if next is None:
                if "interview_result" in current.values.keys():
                    logger.info(f"Start chat, current next is None and interview_result exists")
                    # Workflow ends
                    # Load all messages from the test
                    # Return is_over = true
                    if "qa_history" in current.values.keys():
                        qa_history=[{"question": q, "answer": a, "summary": s} for (q, a, s) in current.values["qa_history"]]
                    else:
                        qa_history = []

                    return {
                        "feedback": feedback,
                        "question_id": question_id,
                        "type": type,
                        "is_over": True,
                        "qa_history": qa_history
                    }
                else:
                    # Normal start of the workflow
                    pass
            elif next == "analyze_answer":
                logger.info(f"Start chat, current next is analyze_answer")
                # Load all messages from the test
                # Wait for user answer
                # Return is_over = false
                if "qa_history" in current.values.keys():
                    qa_history=[{"question": q, "answer": a, "summary": s} for (q, a, s) in current.values["qa_history"]]
                else:
                    qa_history = []

                return {
                    "feedback": feedback,
                    "question_id": question_id,
                    "type": type,
                    "is_over": False,
                    "qa_history": qa_history
                }
            elif next != START:
                logger.info(f"Start chat, current next is {next}")
                # Resume the workflow
                # Load all messages from the test
                events = self.workflow.invoke(None, config=config)
                for event in events:
                    pass

                # get the snapshot state (next question is in the snapshot)
                snapshot = self.workflow.get_state(config)
                if snapshot.next:                    
                    # show the question to user
                    # wait for user answer
                    feedback = snapshot.values["feedback"]
                    is_over = False
                else:
                    # workflow has no next, end
                    is_over = True

                if "qa_history" in current.values.keys():
                    qa_history=[{"question": q, "answer": a, "summary": s} for (q, a, s) in current.values["qa_history"]]
                else:
                    qa_history = []

                return {
                    "feedback": feedback,
                    "question_id": str(uuid4()),  # TODO: Needs to be fetched from snapshot
                    "type": "question",
                    "is_over": is_over,
                    "qa_history": qa_history
                }

        # new workflow
        # start the interview, generate the first question
        events = self.workflow.stream(inputs, config=config, stream_mode="values")
        for event in events:
            pass

        snapshot: StateSnapshot = self.workflow.get_state(config)
        if snapshot.next:                    
            # show the question to user
            feedback = snapshot.values["feedback"]
            is_over = False
        else:
            is_over = True

        return {
            "feedback": feedback,
            "question_id": str(uuid4()),  # TODO: Needs to be fetched from snapshot
            "type": "question",
            "is_over": is_over
        }
    
    @log
    async def process_answer(
        self,
        user_id: str,
        test_id: str,
        question_id: str,
        user_answer: str
    ) -> Dict[str, Any]:
        """
        Process User Answer
        
        Args:
            user_id: User ID
            test_id: Test ID
            question_id: Question ID
            user_answer: User Answer
            
        Returns:
            Dict: Contains information about the next question or feedback
        """
        config = {
            "configurable": {
                "thread_id": test_id, 
                "user_id": user_id
            },
            "model_name": self.model_name,
            # "model_name": "gpt-4o",
            # "model_name": "deepseek-v3",
        }

        # Resume the interview workflow
        # Pass user answer and get the result
        # Then generate next question
        events = self.workflow.invoke(Command(resume="Go ahead", update={"user_answer": user_answer}), config=config)
        for event in events:
            pass

        # Get the snapshot state (next question is in the snapshot)
        snapshot = self.workflow.get_state(config)
        feedback = snapshot.values["feedback"]

        # Check if the interview is over
        if "interview_result" in snapshot.values.keys():
            # Call test result service to update interview result
            # Async call
            interview_result: InterviewResult = snapshot.values["interview_result"]  
            logger.info(f"Interview is over, call test result service to update interview result {interview_result.model_dump_json(indent=2)}")

            # Save test result
            test_result_service = TestResultService()
            request = CreateTestResultRequest(
                test_id=test_id,
                user_id=user_id,
                summary=interview_result.summary,
                score=interview_result.score,
                question_number=interview_result.total_question_number,
                correct_number=interview_result.correct_question_number,
                elapse_time=interview_result.interview_time,
                qa_history=[{"question": q, "answer": a, "summary": s} for (q, a, s) in snapshot.values["qa_history"]]
            )
            await test_result_service.complete_test_result(request)

            # Update test status to completed
            await self.test_service.update_test_status_to_completed(test_id)

            is_over = True
        else:
            is_over = False

        return {
            "feedback": feedback,
            "question_id": str(uuid4()),  # TODO: Needs to be fetched from snapshot
            "type": "question",
            "is_over": is_over
        }
