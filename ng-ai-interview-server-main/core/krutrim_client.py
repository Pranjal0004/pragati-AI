# core/krutrim_client.py
import os
import requests
import openai

API_URL = "https://cloud.olakrutrim.com/v1/chat/completions"
API_KEY = os.getenv("KRUTRIM_API_KEY")  

def get_krutrim_response(messages, is_feedback=False, context_prompt=""):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "Llama-4-Maverick-17B-128E-Instruct",
        "messages": []
    }

    if not is_feedback:
        payload["messages"].append({
            "role": "system",
            "content": context_prompt or "You are an AI assistant."
        })

    payload["messages"].extend(messages)

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        text = response.text

        try:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except Exception as json_err:
            print("Invalid JSON received:\n", text)
            raise ValueError("Krutrim API did not return valid JSON") from json_err

    except requests.RequestException as req_err:
        print("Request failed:", str(req_err))
        raise

