import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class FertilizerAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def ask(
        self,
        crop: str,
        land_size: float,
        soil_type: str,
        district: str,
        language: str = "English"
    ):
        # Step 1 - Retrieve fertilizer chunks
        query = (
            f"fertilizer recommendation {crop} cultivation "
            f"NPK dosage soil {soil_type} district {district}"
        )
        docs = self.vs.similarity_search(query, k=4)
        context = (
            "\n\n".join([d.page_content for d in docs])
            if docs
            else "No relevant fertilizer guidance found in the knowledge base."
        )

        # Step 2 - Build prompt
        prompt = f"""
You are an expert agricultural fertilizer advisor for farmers in Andhra Pradesh and Telangana.

Provide the best fertilizer recommendation for this farmer using ONLY the agricultural document context below.

Farmer Details:
- Crop: {crop}
- Land Size: {land_size} acres
- Soil Type: {soil_type}
- District: {district}

Agricultural Document Context:
{context}

Provide a DETAILED fertilizer plan including:
1. Recommended Fertilizers (NPK — Nitrogen, Phosphorus, Potassium)
2. Quantity needed per acre and total for {land_size} acres
3. When to apply (basal dose, top dressing schedule)
4. Estimated cost (approximate, if available in context)
5. Important tips for {crop} in {soil_type} soil

Answer in {language} in simple language a farmer can understand.
Give specific quantities in kg per acre whenever possible.
Do NOT ask for more information — give the best recommendation from the provided context.

IMPORTANT:
- Answer in {language} language ONLY.
- If language is Telugu, write the complete answer in Telugu script.
- Do not mix English and Telugu.
"""

        response = self.llm.invoke(prompt)
        return response.content


# Test it
if __name__ == "__main__":
    agent = FertilizerAgent()
    answer = agent.ask(
        crop="Paddy",
        land_size=2.0,
        soil_type="Clay Loam",
        district="Guntur",
        language="English"
    )
    print("\n🌱 Fertilizer Advisory:")
    print(answer)