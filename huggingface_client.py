from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set in the environment variables.")

client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

def send_to_huggingface_api_with_client(messages):
    """Send extracted text to the Hugging Face API using InferenceClient."""
    # messages = [
    #     {"role": user, "content": text}
    # ]
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
        max_tokens=500
    )
    return completion.choices[0].message
