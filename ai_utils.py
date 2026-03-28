import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import build_prompt

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_study_pack(user_text, difficulty, num_questions):
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = build_prompt(user_text, difficulty, num_questions)

    response = model.generate_content(prompt)
    content = response.text.strip()

    # Remove markdown code block if Gemini adds it
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)
