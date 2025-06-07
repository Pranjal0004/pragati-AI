import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.interview_response import QAResult
from utils.llm import get_model
from langchain_core.messages import HumanMessage
from utils.prompt_utils import load_prompt
from utils.log_utils import logger


def analyze_question_answer(answer: str, question: str, language: str = "Chinese", model_name: str = "gpt-4o") -> QAResult:
    logger.info("========== Analyzing Question Answer ==========")
    
    prompt_content: str = load_prompt('prompts/analyze_answer.txt')
    human_prompt: HumanMessage = HumanMessage(content=prompt_content.format(
        question=question, 
        answer=answer, 
        language=language
    ))
        
    model = get_model(model=model_name).with_structured_output(QAResult)
    response: QAResult = model.invoke([human_prompt])
    
    logger.info(f"Analysis Result: {response.model_dump_json(indent=2)}")
    return response

if __name__ == "__main__":
    logger.info("Running QA Analyzer test cases")
    
    # Test case 1: Invalid answer
    question = "Q2. What is the capital of France?"
    answer = "adfadsfdasf"
    logger.info("Test Case 1: Invalid answer")
    qa_result = analyze_question_answer(answer, question, language="Chinese")

    # Test case 2: Valid answer
    question = "Q2. What is the capital of France?\nA. Paris\nB. London\nC. Rome\nD. Madrid"
    answer = "A"
    logger.info("Test Case 2: Valid answer")
    qa_result = analyze_question_answer(answer, question, language="Chinese")

