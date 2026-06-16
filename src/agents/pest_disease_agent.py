import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class PestDiseaseAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def ask(self, crop: str, symptoms: str, language: str = "English"):
        # Step 1 - Retrieve pest management chunks
        query = f"{crop} pest disease {symptoms} treatment control"
        docs = self.vs.similarity_search(query, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # Step 2 - Build prompt
        prompt = f"""You are a pest and disease expert for farmers
in Andhra Pradesh and Telangana.

Use ONLY the following agricultural document context to answer.

Context from Pest Management Documents:
{context}

Farmer's Crop: {crop}
Symptoms Described: {symptoms}

Identify the likely pest or disease and suggest treatment.
Answer in {language} in simple language a farmer can understand.
"""
        # Step 3 - Get answer from Gemini
        response = self.llm.invoke(prompt)
        return response.content

# Test it
if __name__ == "__main__":
    agent = PestDiseaseAgent()
    answer = agent.ask(
        "Tomato",
        "Leaves are turning yellow and curling",
        "English"
    )
    print("\n🐛 Pest and Disease Advisory:")
    print(answer)