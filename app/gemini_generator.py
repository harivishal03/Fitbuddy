import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_workout_gemini(age, weight, goal, intensity):

    model = genai.GenerativeModel("gemini-3.5-flash-lite")

    prompt = f"""
Create a detailed 7-day workout plan.

Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

Include:
- Warm-up
- Main workout
- Cooldown
"""

    response = model.generate_content(prompt)

    return response.text