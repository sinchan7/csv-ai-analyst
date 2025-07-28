import os
import google.generativeai as genai

# Initialize Gemini with API Key
def init_gemini():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Send prompt to Gemini
def query_llm(prompt: str, model="gemini-1.5-flash") -> str:
    init_gemini()
    model = genai.GenerativeModel(model_name=model)
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # --- Clean the response from markdown formatting ---
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")  # remove backticks
        lines = raw_text.splitlines()
        if lines and lines[0].lower().startswith("python"):
            lines = lines[1:]  # remove ```python line
        raw_text = "\n".join(lines).strip()

    return raw_text
