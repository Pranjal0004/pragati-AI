# core/interview_graph.py

from core.interview_chain import (
    QuestionChain,
    HintChain,
    FeedbackChain,
    TimeoutDecisionChain
)
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict
from typing_extensions import Annotated
import time
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
frontend_url = os.getenv("FRONTEND_URL")


def current_time():
    return time.time()


def is_time_up(state):
    return (current_time() - state["startTime"]) / 60 >= float(state["duration_minutes"])


def start_interview(state):
    print("start_interview received state:", state)

    new_state = {
        **state,
        "startTime": current_time(),
        "currentQuestionNumber": 1,
        "questions": [],
        "answers": [],
        "history": [],
    }
    return {"next": "ask_question", **new_state}


def ask_question(state):
    total_elapsed = int((current_time() - state["startTime"]) / 60)
    q_no = state["currentQuestionNumber"]

    prev_question = state["questions"][-1]["question"] if state["questions"] else ""
    prev_answer = state["answers"][q_no - 2] if q_no > 1 and len(state["answers"]) >= q_no - 1 else ""
    print("Prev question", prev_question)
    print("Prev answers", prev_answer)

    raw_output = QuestionChain.run(
        role=state["role"],
        level=state["level"],
        questions=state["questions"],
        previous_question=prev_question,
        previous_answer=prev_answer
    )

    acknowledgement = "Let's continue."
    question_text = "N/A"
    estimated_time = 60  # default

    import json
    try:
        json_str = raw_output[raw_output.index("{"): raw_output.rindex("}") + 1]
        parsed = json.loads(json_str)

        acknowledgement = parsed.get("acknowledgement", acknowledgement)
        question_text = parsed.get("question", question_text)
        mins = parsed.get("estimatedTime", {}).get("minutes", 0)
        secs = parsed.get("estimatedTime", {}).get("seconds", 0)
        estimated_time = mins * 60 + secs
        if estimated_time == 0:
            estimated_time = 10

    except Exception as e:
        print("Parse error:", e)

    new_state = {
        **state,
        "currentQuestion": question_text,
        "estimatedTime": estimated_time,
        "questions": state["questions"] + [{"question": question_text, "estimatedTime": estimated_time}],
    }
    return {
        **new_state,
        "next": "return_question",
        "questionPayload": {
            "acknowledgement": acknowledgement,
            "question": question_text,
            "estimatedTime": estimated_time,
            "questionNumber": q_no
        }
    }


def return_question(state):
    if is_time_up(state):
        print("⏱️ Interview time over. Ending interview.")
        return {**state, "next": "end_interview"}

    question_payload = state.get("questionPayload", {
        "question": state.get("currentQuestion", "No question"),
        "acknowledgement": "Let's continue.",
        "questionNumber": state.get("currentQuestionNumber", 1),
        # "estimatedTime": state.get("estimatedTime", 60),
        "estimatedTime": 10,
    })
    question_payload["estimatedTime"] = 10      #remove this line

    if not question_payload:
        print("Missing questionPayload in state!")
        return {**state, "next": "ask_question"}

    endpoint = f"{frontend_url.rstrip('/')}/api/receive-question"
    if not endpoint:
        print("FRONTEND_URL not set in environment!")
    else:
        try:
            with httpx.Client() as client:
                response = client.post(endpoint, json=question_payload)
                print("Sent to frontend:", response.status_code, response.text)
        except Exception as e:
            print("Error sending question to frontend:", e)

    return {
        **state,
        "next": None,
        "questionPayload": question_payload 
    }


def submit_answer(state):
    answer = state.get("latestAnswer") or "[No answer given]"
    question_text = state["currentQuestion"]

    updated_answers = state["answers"] + [answer]
    updated_history = state["history"] + [{"question": question_text, "answer": answer}]

    next_node = "end_interview" if is_time_up(state) else "ask_question"

    return {
        **state,
        "answers": updated_answers,
        "history": updated_history,
        "currentQuestionNumber": state["currentQuestionNumber"] + 1,
        "next": next_node,
        "hint": None
    }


def handle_timeout(state):
    partial_answer = state.get("latestAnswer")

    decision = TimeoutDecisionChain.run(
        question=state["currentQuestion"],
        partial_answer=partial_answer,
        history=state["history"]
    )
    # decision = "stop_answering"
    print("Decision:", decision)
    return {**state, "next": decision, "decision": decision}


def give_hint(state):
    question = state.get("currentQuestion")
    print("🧠 Generating hint for:", question)
    
    try:
        hint = HintChain.run(question)
        print("✅ Hint generated:", hint)
    except Exception as e:
        print("❌ Error generating hint:", e)
        hint = "Sorry, no hint available at the moment."

    return {
        **state,
        "hint": hint,
        "next": None,
    }


def continue_answering(state):
    return {
        **state, 
        "next": None, 
    }


def stop_answering(state):
    return {
        **state,
        "next": None,
    }


def end_interview(state):
    formatted_history = "\n\n".join([
        f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}"
        for i, item in enumerate(state["history"])
    ])
    feedback = FeedbackChain.run(formatted_history)

    try:
        with httpx.Client() as client:
            response = client.post(
                f"{frontend_url.rstrip('/')}/api/receive-question",
                json={
                    "question": "Interview is complete. Thank you!",
                    "acknowledgement": "✅ Interview complete.",
                    "questionNumber": -1,
                    "isComplete": True, 
                    "feedback": feedback,
                }
            )
            print("✅ Interview end sent to frontend:", response.status_code, response.text)
    except Exception as e:
        print("❌ Failed to notify frontend about interview end:", e)

    return {
        **state,
        "feedback": feedback,
        "next": None,
    }


class InterviewGraphState(TypedDict, total=False):
    role: Annotated[str, "input"]
    level: Annotated[str, "input"]
    duration_minutes: Annotated[int, "input"]
    startTime: float
    currentQuestionNumber: int
    questions: List[Dict[str, any]]
    answers: List[str]
    history: List[Dict[str, str]]
    currentQuestion: str
    estimatedTime: int
    next: str
    latestAnswer: str
    hint: str
    feedback: str
    questionPayload: Dict[str, str]
    decision: str


def create_interview_graph():
    g = StateGraph(state_schema=InterviewGraphState)

    g.add_node("start_interview", start_interview)
    g.add_node("ask_question", ask_question)
    g.add_node("return_question", return_question)
    g.add_node("submit_answer", submit_answer)
    g.add_node("handle_timeout", handle_timeout)
    g.add_node("give_hint", give_hint)
    g.add_node("continue_answering", continue_answering)
    g.add_node("stop_answering", stop_answering)
    g.add_node("end_interview", end_interview)

    g.add_conditional_edges(START, lambda state: state.get("next") or "start_interview")
    g.add_edge("start_interview", "ask_question")
    g.add_edge("ask_question", "return_question")
    g.add_edge("return_question", END)
    g.add_conditional_edges("submit_answer", lambda state: state["next"])
    g.add_conditional_edges("handle_timeout", lambda state: state["next"])
    g.add_edge("give_hint", END)
    g.add_edge("continue_answering", END)
    g.add_edge("stop_answering", END)
    g.add_edge("end_interview", END)

    return g.compile()
