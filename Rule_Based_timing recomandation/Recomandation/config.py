import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

groq_api_key = os.getenv("GROQ_API_KEY")

# print("groq API",groq_api_key)
