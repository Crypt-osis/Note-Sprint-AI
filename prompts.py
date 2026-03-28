def build_prompt(user_text, difficulty, num_questions):
    return f"""
You are an academic study assistant.

Analyze the following study material and return ONLY valid JSON.

The JSON format must be:

{{
  "title": "Short topic title",
  "summary": [
    {{
      "heading": "Heading name",
      "points": ["point 1", "point 2", "point 3"]
    }}
  ],
  "keyTerms": [
    {{
      "term": "Important term",
      "definition": "Simple definition"
    }}
  ],
  "quiz": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option text"
    }}
  ]
}}

Rules:
- Difficulty level: {difficulty}
- Number of quiz questions: {num_questions}
- Make the summary concise and exam-friendly
- Use clear bullet-point style
- Key terms should be useful for revision
- Questions must be based only on the provided text
- Return ONLY JSON
- Do not include markdown
- Do not include explanation before or after JSON

Study Material:
\"\"\"
{user_text}
\"\"\"
"""