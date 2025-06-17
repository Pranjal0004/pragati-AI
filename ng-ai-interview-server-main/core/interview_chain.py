# core/interview_chain.py

from core.krutrim_client import get_krutrim_response
from core.prompt import question_prompt, hint_prompt, feedback_prompt, timeout_decision_prompt


class QuestionChain:
    @staticmethod
    def run(role, level, questions, previous_question=None, previous_answer=None):
        question_list = [q["question"] for q in questions]

        formatted_prompt = question_prompt.format(
            role=role,
            level=level,
            previous_question=previous_question or "",
            previous_answer=previous_answer or ""
        )

        final_prompt = f"""{formatted_prompt}
            Avoid repeating any of these questions:
            {question_list}
        """

        messages = [{"role": "user", "content": final_prompt}]
        return get_krutrim_response(messages)


class HintChain:
    @staticmethod
    def run(question):
        formatted_prompt = hint_prompt.format(question=question)
        messages = [{"role": "user", "content": formatted_prompt}]
        response = get_krutrim_response(messages)

        import re
        match = re.search(r"Hint:\s*(.+)", response, re.IGNORECASE)
        return match.group(1).strip() if match else "Try breaking the question down into smaller parts."


class FeedbackChain:
    @staticmethod
    def run(history):
        formatted_prompt = feedback_prompt.format(history=history)
        messages = [{"role": "user", "content": formatted_prompt}]
        return get_krutrim_response(messages).strip()


class TimeoutDecisionChain:
    @staticmethod
    def run(question, partial_answer, history):
        formatted_prompt = timeout_decision_prompt.format(
            question=question, partialAnswer=partial_answer, history=history
        )
        messages = [{"role": "user", "content": formatted_prompt}]
        return get_krutrim_response(messages).strip()
