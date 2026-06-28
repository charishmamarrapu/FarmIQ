from src.rag.retriever import retrieve_context
from src.utils.llm import get_llm_response

class SchemeAgent:
    def __init__(self):
        self.name = "Scheme Agent"

    def run(self, query):
        context = retrieve_context(query)

        prompt = f"""
You are an agricultural government schemes expert.

Using ONLY the provided context, answer the farmer's question.

Include:
1. Scheme Name
2. Benefits
3. Eligibility
4. Required Documents
5. Application Process

If information is unavailable, clearly state that.

Context:
{context}

Question:
{query}
"""

        response = get_llm_response(prompt)

        return {
            "agent": self.name,
            "response": response
        }