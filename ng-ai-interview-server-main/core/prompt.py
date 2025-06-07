from langchain.prompts import PromptTemplate

# Question Prompt
question_prompt = PromptTemplate(
    input_variables=["role", "level"],
    template="""
        You are an AI interviewer. Ask a technical question for a {role} role at {level} level. 
        The question must:
        - Be appropriate for the {level} level.
        - Increase in complexity, depth, and real-world application as the level goes from entry to senior.
        - Be specific to the practical responsibilities typically expected at that level.

        Respond strictly in the following JSON format (with proper double quotes and valid JSON):
        {{
        "acknowledgement": "<short message to start the interview or appreciate previous answer>",
        "question": "<Your question here>",
        "estimatedTime": {{
            "minutes": <number of minutes>,
            "seconds": <number of seconds>
        }}  
        }}
    """
)

# Hint Prompt
hint_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
        You are an AI assistant helping a candidate in an interview.
        Given the following technical interview question, provide a concise and helpful hint that guides the candidate toward the correct answer without giving away the full solution.

        Question: {question}

        Format:
        Hint: <your hint here>
    """
)

# Feedback Prompt
feedback_prompt = PromptTemplate(
    input_variables=["history"],
    template="""
        You are an AI feedback generator. The following is a series of interview questions and the candidate's answers.
        {history}

        Based on the entire conversation above, provide comprehensive feedback to the candidate and make it short:
        {{
        "strengths": "<Highlight what the candidate did well across their responses>",

        "communication": "<Evaluate their confidence, clarity, and communication style>",

        "suggestions": "<Provide final suggestions to help them perform better in future interviews>"
        }}
    """
)

# Timeout Decision Prompt
timeout_decision_prompt = PromptTemplate(
    input_variables=["question", "partialAnswer", "history"],
    template="""
        The candidate failed to answer the question within the time limit. You are an AI interview assistant.
        Here is the last question:
        "{question}"

        Partial or no answer given:
        "{partialAnswer}"

        Interview history:
        {history}

        Based on this, choose the most appropriate next step:
        - "give_hint" — if the candidate may benefit from a small clue.
        - "carry_on_answering" — if the answer seems partially complete or the candidate just needs more time.
        - "stop_answering" — if it's best to move on to the next question.

        Respond with **only one word** (no explanation or formatting):
        give_hint | carry_on_answering | stop_answering
    """
)
