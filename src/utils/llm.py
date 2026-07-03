import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm_response(prompt: str, language: str = "English") -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Add language instruction to prompt
    full_prompt = prompt + f"""

IMPORTANT: Answer in {language} language ONLY.
If language is Telugu, write the COMPLETE answer
in Telugu script. Do not mix English and Telugu.
Give detailed explanation in {language}.
"""
    response = llm.invoke(full_prompt)
    return response.content