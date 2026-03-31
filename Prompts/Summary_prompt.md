SYSTEM_PROMPT = """You are AcademicMind, an expert study assistant trained on Indian university curricula.
Your sole job is to analyze study material and return structured JSON for revision aids.

OUTPUT CONTRACT:
- Return ONLY a single valid JSON object. No markdown. No code fences. No explanation.
- Do not add any text before or after the JSON.
- All string values must be plain text (no markdown inside values).
- If the input is too short or unclear, still return the JSON with best-effort content.

JSON SCHEMA (strict):
{
  "title": string,                          // 3–8 word topic title inferred from the text
  "summary": [                              // 3–6 topic-grouped sections
    {
      "heading": string,                    // concise section heading
      "points": [string, ...]               // 3–6 crisp, exam-ready bullet points
    }
  ],
  "keyTerms": [                             // 5–10 must-know terms
    {
      "term": string,
      "definition": string                  // one sentence, jargon-free
    }
  ],
  "quiz": [                                 // exactly num_questions MCQs
    {
      "question": string,
      "options": [string, string, string, string],   // always exactly 4 options
      "answer": string                      // must exactly match one of the 4 options
    }
  ]
}"""


DIFFICULTY_PROFILES = {
    "Easy": (
        "EASY difficulty: Questions test direct recall of facts and definitions. "
        "One obviously correct answer, three clearly wrong distractors. "
        "Use simple language. Avoid negatives (e.g. 'which is NOT...')."
    ),
    "Medium": (
        "MEDIUM difficulty: Questions test understanding and application. "
        "All four options should be plausible; only one is unambiguously correct. "
        "Include some inference-based and 'best answer' style questions."
    ),
    "Hard": (
        "HARD difficulty: Questions test deep analysis, comparison, and edge cases. "
        "Distractors should be near-correct and require careful reasoning to eliminate. "
        "Include questions that combine two concepts, test exceptions, or require multi-step thinking."
    ),
}


def build_messages(user_text: str, difficulty: str, num_questions: int) -> list[dict]:
    """
    Returns the messages array for the Anthropic / OpenAI chat API.

    Separating system and user roles:
    - System prompt sets the persona and rigid output contract once.
    - User prompt carries variable data, keeping token count efficient on repeat calls.

    Args:
        user_text:      Raw study material pasted or extracted by the user.
        difficulty:     One of "Easy", "Medium", "Hard".
        num_questions:  Integer between 1 and 20.

    Returns:
        List of message dicts ready for client.messages.create(messages=...)
    """
    if difficulty not in DIFFICULTY_PROFILES:
        difficulty = "Medium"

    num_questions = max(1, min(20, int(num_questions)))

    difficulty_instruction = DIFFICULTY_PROFILES[difficulty]

    user_prompt = f"""Generate a structured study aid from the material below.

PARAMETERS:
- Quiz difficulty: {difficulty}
- {difficulty_instruction}
- Number of quiz questions: {num_questions} (generate exactly this many)
- Summary: group content into logical topic sections with concise, exam-friendly bullet points
- Key terms: prioritise terms a student would encounter in an exam or viva

STUDY MATERIAL:
\"\"\"
{user_text.strip()}
\"\"\"

Remember: return ONLY the JSON object. No extra text."""

    return [
        {"role": "user", "content": user_prompt}
    ]


def build_system_prompt() -> str:
    """Returns the system prompt string for use in the `system` parameter."""
    return SYSTEM_PROMPT


# ── Convenience wrapper for direct single-string prompt APIs ──────────────────

def build_prompt(user_text: str, difficulty: str, num_questions: int) -> str:
    """
    Legacy single-string prompt for APIs that don't support system/user separation.
    Prefer build_messages() + build_system_prompt() when possible.
    """
    messages = build_messages(user_text, difficulty, num_questions)
    return f"{SYSTEM_PROMPT}\n\n{messages[0]['content']}"


# ── Usage example ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_text = """
    Photosynthesis is the process by which green plants, algae, and some bacteria
    convert light energy into chemical energy stored as glucose. It occurs in the
    chloroplasts, using chlorophyll to absorb sunlight. The overall reaction is:
    6CO2 + 6H2O + light energy → C6H12O6 + 6O2.
    The process has two stages: the light-dependent reactions (in the thylakoid membranes)
    and the Calvin cycle (in the stroma). ATP and NADPH produced in the light reactions
    power the Calvin cycle to fix CO2 into sugar.
    """

    # Recommended usage (chat API with system/user separation)
    system = build_system_prompt()
    messages = build_messages(sample_text, difficulty="Medium", num_questions=5)

    print("=== SYSTEM ===")
    print(system)
    print("\n=== USER MESSAGE ===")
    print(messages[0]["content"])
