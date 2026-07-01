import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class MarketPriceAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.api_key = os.getenv("DATA_GOV_API_KEY")

    def get_mandi_price(self, crop: str, state: str = "Andhra Pradesh"):
        """Fetch live mandi price from data.gov.in"""
        try:
            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                "api-key": self.api_key,
                "format": "json",
                "filters[State]": state,
                "filters[Commodity]": crop,
                "limit": 5
            }
            response = requests.get(url, params=params)
            data = response.json()
            return data.get("records", [])
        except Exception as e:
            print(f"Mandi API error: {e}")
            return []

    def ask(self, crop: str, district: str, language: str = "English"):
        # Step 1 - Get live prices
        prices = self.get_mandi_price(crop)

        # Step 2 - Get context from vector store
        docs = self.vs.similarity_search(
            f"{crop} price market {district}", k=3
        )
        context = "\n\n".join([d.page_content for d in docs])

        # Step 3 - Build prompt
        price_text = str(prices) if prices else "Live price data unavailable"

        prompt = f"""You are a market price advisor for farmers
in Andhra Pradesh and Telangana.

Live Mandi Price Data:
{price_text}

Historical Context from Documents:
{context}

Farmer wants to know about {crop} prices in {district}.
Give current price information and a clear
sell or hold recommendation.
Answer in {language} in simple language
a farmer can understand.
"""
        # Step 4 - Get answer from Gemini
        response = self.llm.invoke(prompt)
        return response.content

# Test it
if __name__ == "__main__":
    agent = MarketPriceAgent()
    answer = agent.ask("Paddy", "Krishna", "English")
    print("\n💰 Market Price Advisory:")
    print(answer)