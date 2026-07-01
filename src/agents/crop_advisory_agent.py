import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class CropAdvisoryAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def ask(self, question: str, language: str = "English", district: str = ""):
        # Step 1 - Retrieve relevant chunks
        search_query = f"{question} {district}" if district else question
        docs = self.vs.similarity_search(search_query, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # Step 2 - Build prompt
        prompt = f"""You are an expert agricultural advisor
for farmers in Andhra Pradesh and Telangana.

Use the following document context to answer the farmer's question.
Give a COMPLETE and DETAILED answer covering:
1. Which specific crops are recommended
2. Why these crops are suitable for the district and season
3. Key cultivation tips (sowing time, soil, irrigation)
4. Expected yield or benefits

Farmer's District: {district}

Context:
{context}

Farmer Question: {question}

Important instructions:
- Give specific crop names not general terms
- Give practical advice a farmer can act on immediately
- Do NOT say the document mentions or it suggests
- Do NOT ask for more information
- Answer directly and confidently in {language}
- Keep answer clear and easy to understand
"""
        # Step 3 - Get answer from Groq
        response = self.llm.invoke(prompt)
        return response.content

# Test it
if __name__ == "__main__":
    agent = CropAdvisoryAgent()
    answer = agent.ask(
        "What is the best crop to grow in Kharif season?",
        language="English",
        district="Guntur"
    )
    print("\n🌾 Crop Advisory:")
    print(answer)