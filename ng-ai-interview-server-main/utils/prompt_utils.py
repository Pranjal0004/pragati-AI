import os

def load_prompt(file_path: str) -> str:
    """Load a prompt from a file."""
    prompt_file_path = os.path.join(os.path.dirname(__file__), '..', 'agent', file_path)
    with open(prompt_file_path, 'r', encoding='utf-8') as file:
        return file.read()