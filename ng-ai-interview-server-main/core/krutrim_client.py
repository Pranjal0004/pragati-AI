# core/krutrim_client.py
import os
import requests
import openai

# API_URL = "https://cloud.olakrutrim.com/v1/chat/completions"
# API_KEY = os.getenv("KRUTRIM_API_KEY")  

# def get_krutrim_response(messages, is_feedback=False, context_prompt=""):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#     }

#     payload = {
#         "model": "Llama-4-Scout-17B-16E-Instruct",
#         "messages": []
#     }

#     if not is_feedback:
#         payload["messages"].append({
#             "role": "system",
#             "content": context_prompt or "You are an AI assistant."
#         })

#     payload["messages"].extend(messages)

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         text = response.text

#         try:
#             data = response.json()
#             return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
#         except Exception as json_err:
#             print("Invalid JSON received:\n", text)
#             raise ValueError("Krutrim API did not return valid JSON") from json_err

#     except requests.RequestException as req_err:
#         print("Request failed:", str(req_err))
#         raise

API_KEY = "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" 
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_openrouter_response(messages, is_feedback=False, context_prompt=""):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # Or any other OpenRouter-supported model
        "messages": []
    }

    if not is_feedback:
        payload["messages"].append({
            "role": "system",
            "content": context_prompt or "You are a helpful assistant."
        })

    payload["messages"].extend(messages)

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

    except requests.RequestException as req_err:
        print("Request failed:", str(req_err))
        raise

    except Exception as json_err:
        print("Invalid JSON received:\n", response.text)
        raise ValueError("OpenRouter API did not return valid JSON") from json_err
