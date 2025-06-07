
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.graph import StateGraph
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from workflow import build_graph
from langgraph.types import Command
from langgraph.types import StateSnapshot


def execute_ai_interview_agent(workflow, inputs: dict):
    config = {
        "configurable": {
            "thread_id": uuid.uuid4(), 
            "user_id": "Interviewer"
        },
        # "model_name": "claude-3-5-sonnet",
        "model_name": "gpt-4o",
        # "model_name": "deepseek-v3",
    }

    # start the interview, generate the first question
    events = workflow.stream(inputs, config=config, stream_mode="values")
    for event in events:
        pass

    snapshot: StateSnapshot = workflow.get_state(config)
    while snapshot.next:        
        
        # show the question to user
        feedback = snapshot.values["feedback"]
        print("AI :> " + feedback)

        # get the user answer
        user_input = input('User :> ')

        # resume the interview workflow
        # pass user answer and get the result
        # then generate next question
        events = workflow.invoke(Command(resume="Go ahead", update={"user_answer": user_input}), config=config)
        for event in events:
            pass

        # get the snapshot state (next question is in the snapshot)
        snapshot = workflow.get_state(config)



if __name__ == "__main__":
    workflow = build_graph()

    inputs = {
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "messages": [],
        "job_title": "React Web Developer",
        "knowledge_points": "React, JavaScript, TypeScript, React Router, React State Management, Redux, React Hooks, React Context API, React Performance Optimization",
        "interview_time": 3,
        "language": "English",
        "difficulty": "Easy"
    }
    execute_ai_interview_agent(workflow, inputs)