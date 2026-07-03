import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import base64

load_dotenv()

class PestDiseaseAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def ask(self, crop: str, symptoms: str,
            language: str = "English") -> str:
        # Step 1 - Retrieve pest management chunks
        query = f"{crop} pest disease {symptoms} treatment control"
        docs = self.vs.similarity_search(query, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # Step 2 - Build prompt
        prompt = f"""You are a pest and disease expert
for farmers in Andhra Pradesh and Telangana.

Use ONLY the following agricultural document context to answer.

Context from Pest Management Documents:
{context}

Farmer's Crop: {crop}
Symptoms Described: {symptoms}

Provide a DETAILED answer including:
1. Likely Pest or Disease Name
2. Why you think this is the issue
3. Treatment/Control measures
4. Preventive measures for future
5. When to consult an expert

IMPORTANT: Answer in {language} language ONLY.
If language is Telugu, write the COMPLETE answer
in Telugu script. Do not mix English and Telugu.
Give detailed explanation in {language}.
"""
        response = self.llm.invoke(prompt)
        return response.content

    def analyze_image(self, crop: str, image_description: str,
                      language: str = "English") -> str:
        """Analyze crop disease from image description"""
        # Step 1 - Retrieve relevant chunks
        query = f"{crop} pest disease symptoms treatment"
        docs = self.vs.similarity_search(query, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # Step 2 - Build prompt with image description
        prompt = f"""You are a pest and disease expert
for farmers in Andhra Pradesh and Telangana.

A farmer has uploaded a photo of their {crop} crop.
Image shows: {image_description}

Use the following agricultural document context:
{context}

Based on the visual symptoms described, provide:
1. Likely Pest or Disease Name
2. Confidence level (High/Medium/Low)
3. Visual symptoms that match
4. Treatment/Control measures
5. Preventive measures
6. Urgency level (Immediate/Soon/Monitor)

IMPORTANT: Answer in {language} language ONLY.
If language is Telugu, write the COMPLETE answer
in Telugu script. Do not mix English and Telugu.
Give detailed explanation in {language}.
"""
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