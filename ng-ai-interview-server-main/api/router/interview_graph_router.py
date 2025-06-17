from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from uuid import uuid4
from core.interview_graph import create_interview_graph
from api.utils.store import session_store

router = APIRouter()
interview_graph = create_interview_graph()

class InterviewRequest(BaseModel):
    role: str
    level: Literal["Entry", "Mid", "Senior"]
    durationMinutes: int = 2  

@router.post("/start")
async def start_interview(request: Request):
    try:
        body = await request.json()
        role = body.get("role", "Default Role")
        level = body.get("level", "Entry")
        duration = body.get("durationMinutes", 5)
        session_id = str(uuid4())
        state = {
            "currentQuestionNumber": 1,
            "history": [],
            "answers": [],
            "questions": [],
            "currentQuestion": "",
            "duration_minutes": duration,
            "startTime": datetime.utcnow().timestamp(),
            "role": role,
            "level": level,
            "next": "start_interview"
        }
        session_store[session_id] = state
        result = interview_graph.invoke(state)
        session_store[session_id] = result 

        return JSONResponse(content={
            "sessionId": session_id,
            "message": "Interview started",
            "state": result,
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/submit-answer")
async def submit_answer(request: Request):
    try:
        body = await request.json()
        answer = body.get("answer")
        session_id = body.get("sessionId")
        if not answer or not session_id:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing 'answer' or 'sessionId'"}
            )
        state = session_store.get(session_id)
        if not state:
            return JSONResponse(status_code=404, content={"error": "Session not found"})
        state["latestAnswer"] = answer
        state["next"] = "submit_answer"
        result = interview_graph.invoke(state)
        session_store[session_id] = result

        return JSONResponse(content={
            "message": "Answer submitted",
            "new_state": result
        })

    except Exception as e:
        print("❌ Error in /submit-answer:", str(e))
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to submit answer", "details": str(e)}
        )


@router.post("/handle-timeout")
async def handle_timeout(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")
        partial_answer = data.get("partialAnswer")

        if not session_id:
            return JSONResponse(status_code=400, content={"error": "Missing sessionId"})

        state = session_store.get(session_id)
        if not state:
            return JSONResponse(status_code=404, content={"error": "Session not found"})

        state["latestAnswer"] = partial_answer or "[No answer - timeout]"
        state["next"] = "handle_timeout"
        # print("📦 Timeout state before invoke:", state)
        result = interview_graph.invoke(state)
        session_store[session_id] = result

        return JSONResponse({
            "code": 200,
            "message": "Timeout handled successfully",
            "data": result
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    
@router.post("/end-interview")
async def end_interview_route(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")

        if not session_id:
            return JSONResponse(status_code=400, content={"error": "Missing sessionId"})

        state = session_store.get(session_id)
        if not state:
            return JSONResponse(status_code=404, content={"error": "Session not found"})

        state["next"] = "end_interview"
        result = interview_graph.invoke(state)
        session_store[session_id] = result

        return JSONResponse({
            "code": 200,
            "message": "Interview ended successfully",
            "data": result
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


