import google.generativeai as genai
import os

# Read API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def get_llm_response(prompt):
    response = model.generate_content(prompt)
    return response.text