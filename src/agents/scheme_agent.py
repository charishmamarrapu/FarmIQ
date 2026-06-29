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

Which government schemes is this farmer eligible for?
"""

        # Retrieve relevant context from the vector database
        context = retrieve_context(query)

        # Create prompt for Gemini
        prompt = f"""
You are an expert in Indian agricultural government schemes.

Using ONLY the information provided in the context below, answer the farmer's question.

Provide your answer in the following format:

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

        # Get response from Gemini
        response = get_llm_response(prompt)

        return response