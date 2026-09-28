import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_nutrition_tip_with_flash(goal):

    model = genai.GenerativeModel("gemini-3.5-flash-lite")

    prompt = f"""
Give one nutrition or recovery tip
for this fitness goal:

{goal}
"""

    response = model.generate_content(prompt)

    return response.text