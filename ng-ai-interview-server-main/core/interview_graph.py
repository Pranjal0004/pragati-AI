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

    raw_output = QuestionChain.run(
        role=state["role"],
        level=state["level"],
        questions=state["questions"]
    )

    acknowledgement = "Let's continue."
    question_text = "N/A"
    estimated_time = 60  # default

    import json
    try:
        # json_str = raw_output[raw_output.index("{"): raw_output.rindex("}") + 1]
        # parsed = json.loads(json_str)
        if isinstance(raw_output, str): #remove this
            parsed = json.loads(raw_output)
        else:
            parsed = raw_output  

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
        "action": "await_user_answer",
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
    }


def handle_timeout(state):
    partial_answer = state["answers"][-1] if state["answers"] else "[No answer - timeout]"

    decision = TimeoutDecisionChain.run(
        question=state["currentQuestion"],
        partial_answer=partial_answer,
        history=state["history"]
    )
    print("Decision:", decision)
    return {**state, "next": decision}


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
        "next": "return_hint"
    }


def return_hint(state):

    return {
        **state,
        "next": None, 
        "action": "await_hint_acknowledgement",
        "hint": state.get("hint", "No hint available.")
    }


def continue_answering(state):
    extra_answer = state.get("latestAnswer") or ""
    combined_answer = f"{state['answers'][-1]} {extra_answer}".strip()

    updated_answers = state["answers"][:-1] + [combined_answer]
    updated_history = state["history"][:-1] + [
        {"question": state["currentQuestion"], "answer": combined_answer}
    ]

    next_node = "end_interview" if is_time_up(state) else "ask_question"

    return {
        **state,
        "answers": updated_answers,
        "history": updated_history,
        "next": next_node,
    }

    extra_answer = state.get("latestAnswer") or ""
    combined_answer = f"{state['answers'][-1]} {extra_answer}".strip()

    updated_answers = state["answers"][:-1] + [combined_answer]
    updated_history = state["history"][:-1] + [
        {"question": state["currentQuestion"], "answer": combined_answer}
    ]

    if (current_time() - state["startTime"]) / 60 >= state["duration_minutes"]:
        next_node = "end_interview"
    else:
        next_node = "ask_question"

    return {
        **state,
        "answers": updated_answers,
        "history": updated_history,
        "next": next_node,
    }


def skip_answer(state):
    return {**state, "next": "end_interview" if is_time_up(state) else "ask_question"}


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


def create_interview_graph():
    g = StateGraph(state_schema=InterviewGraphState)

    g.add_node("start_interview", start_interview)
    g.add_node("ask_question", ask_question)
    g.add_node("return_question", return_question)
    g.add_node("submit_answer", submit_answer)
    g.add_node("handle_timeout", handle_timeout)
    g.add_node("give_hint", give_hint)
    g.add_node("return_hint", return_hint)
    g.add_node("continue_answering", continue_answering)
    g.add_node("skip_answer", skip_answer)
    g.add_node("end_interview", end_interview)

    g.add_conditional_edges(START, lambda state: state.get("next") or "start_interview")
    g.add_edge("start_interview", "ask_question")
    g.add_edge("ask_question", "return_question")
    g.add_edge("return_question", END)
    g.add_conditional_edges("submit_answer", lambda state: state["next"])
    g.add_conditional_edges("handle_timeout", lambda state: state["next"])
    g.add_edge("give_hint", "return_hint")
    g.add_conditional_edges("return_hint", lambda state: state["next"])
    g.add_conditional_edges("continue_answering", lambda state: state["next"])
    g.add_conditional_edges("skip_answer", lambda state: state["next"])
    g.add_edge("end_interview", END)

    return g.compile()
