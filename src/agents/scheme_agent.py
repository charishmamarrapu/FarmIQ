import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.retriever import retrieve_context
from utils.llm import get_llm_response


class SchemeAgent:
    def __init__(self):
        self.name = "Scheme Agent"

    def ask(self, land_size, income, district, language="English"):
        # Build the farmer query
        query = f"""
Land Size: {land_size} acres
Annual Income: ₹{income}
District: {district}
Language: {language}

Which government schemes is this farmer eligible for based on the given details?
"""

        # Retrieve relevant context from the vector database
        context = retrieve_context(query)

        # Create prompt for Groq
        prompt = f"""
You are an expert in Indian agricultural government schemes.

Use ONLY the information provided in the context below to answer the farmer's question.

Provide the answer in the following format:

1. Scheme Name
2. Benefits
3. Eligibility
4. Required Documents
5. Application Process

If the context does not contain enough information, clearly mention that.

========================
Context:
{context}
========================

Farmer Query:
{query}
"""

        # Get response from LLM
        response = get_llm_response(prompt, language)

        return response


# Test it
if __name__ == "__main__":
    agent = SchemeAgent()
    result = agent.ask(
        land_size=2,
        income=50000,
        district="Guntur",
        language="English"
    )
    print("\n🏛️ Scheme Advisory:")
    print(result)