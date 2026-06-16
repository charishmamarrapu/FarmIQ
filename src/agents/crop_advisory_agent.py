import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rag.vectorstore import load_vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class CropAdvisoryAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def ask(self, question: str, language: str = "English"):
        # Step 1 - Retrieve relevant chunks
        docs = self.vs.similarity_search(question, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # Step 2 - Build prompt
        prompt = f"""You are an expert agricultural advisor for farmers
in Andhra Pradesh and Telangana.

Use the following document context to answer.

Context:
{context}

Farmer Question: {question}

Answer in {language} in simple, clear language
a farmer can understand.
"""
        #Step 3 - Get answer from Gemini
        response = self.llm.invoke(prompt)
        return response.content  

# Test it
if __name__ == "__main__":
    agent = CropAdvisoryAgent()

    # Try these different queries
    queries = [
        "What are Kharif crops?",
        "How to grow paddy crop?",
        "What is the irrigation method for rice?",
        "Fertilizer for cotton cultivation",
    ]

    for q in queries:
        print(f"\n🌾 Question: {q}")
        answer = agent.ask(q, language="English")
        print(f"Answer: {answer}")
        print("-"*50)