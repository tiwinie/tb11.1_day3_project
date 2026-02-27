from google.adk.agents import Agent
from google.adk.tools import google_search



import requests

API_KEY = "60d7b980f7da638967fed7f0aaf80f84"  # Your real OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---")  # Log tool execution
    city_normalized = city.strip()

    params = {
        "q": city_normalized,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            city_name = data["name"]

            return {
                "status": "success",
                "report": f"The weather in {city_name} is {weather} with a temperature of {temp}°C."
            }
        else:
            return {
                "status": "error",
                "error_message": data.get("message", "Unknown error occurred.")
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
        
        
Weather_agent = Agent(
    name="Weather_agent",
    model="gemini-2.0-flash",
    description="Weather agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get Weather of the city asked by using tool
    """,
    tools=[get_weather],
)