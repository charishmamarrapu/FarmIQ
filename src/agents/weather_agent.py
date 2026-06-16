import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import load_vectorstore
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class WeatherAgent:
    def __init__(self):
        self.vs = load_vectorstore()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.weather_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, district: str):
        """Fetch live weather from OpenWeatherMap"""
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": f"{district},IN",
                "appid": self.weather_key,
                "units": "metric",
                "cnt": 5
            }
            response = requests.get(url, params=params)
            data = response.json()
            forecasts = []
            for item in data.get("list", []):
                forecasts.append({
                    "time": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "weather": item["weather"][0]["description"],
                    "rain": item.get("rain", {}).get("3h", 0)
                })
            return forecasts
        except Exception as e:
            print(f"Weather API error: {e}")
            return []

    def ask(self, crop: str, district: str, language: str = "English"):
        # Step 1 - Get live weather
        weather = self.get_weather(district)

        # Step 2 - Get crop weather context from vector store
        docs = self.vs.similarity_search(
            f"weather impact on {crop} crop rainfall damage", k=3
        )
        context = "\n\n".join([d.page_content for d in docs])

        # Step 3 - Build prompt
        weather_text = str(weather) if weather else "Weather data unavailable"

        prompt = f"""You are a weather advisory expert for farmers
in Andhra Pradesh and Telangana.

Live Weather Forecast for {district}:
{weather_text}

Crop Weather Impact from Agricultural Documents:
{context}

The farmer is growing {crop} in {district}.
Analyze the weather forecast and warn about any risks.
Give specific advice on what the farmer should do.
Answer in {language} in simple language a farmer can understand.
"""
        # Step 4 - Get answer from Gemini
        response = self.llm.invoke(prompt)
        return response.content

# Test it
if __name__ == "__main__":
    agent = WeatherAgent()
    answer = agent.ask("Cotton", "Guntur", "English")
    print("\n🌤️ Weather Advisory:")
    print(answer)