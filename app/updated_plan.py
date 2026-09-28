import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def update_workout_plan(original_plan, feedback):

    model = genai.GenerativeModel("gemini-3.5-flash-lite")

    prompt = f"""
Original workout plan:

{original_plan}

User feedback:

{feedback}

Generate an improved version.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(e)
        return "Gemini quota exceeded. Please try again after some time."