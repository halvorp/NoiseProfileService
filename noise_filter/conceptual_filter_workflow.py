import re
import html
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from .conceptual_noise_model_loader import load_noise_model

app = FastAPI()
noise_model = None

@app.on_event("startup")
def startup_event():
    global noise_model
    profile_path = Path("conceptual_noise_profile.json")
    if not profile_path.exists():
        raise RuntimeError("Noise profile not found. Please run the offline analysis first.")
    noise_model = load_noise_model(profile_path)

class SanitizationRequest(BaseModel):
    text: str

class SanitizationResponse(BaseModel):
    sanitized_text: str

@app.post("/sanitize", response_model=SanitizationResponse)
def sanitize_text(request: SanitizationRequest):
    """Sanitizes a text by first stripping markup, then removing noise patterns."""
    if noise_model is None:
        raise HTTPException(status_code=500, detail="Noise model not loaded.")

    # 1. Un-escape HTML entities (e.g., &lt; -> <)
    text_unscaped = html.unescape(request.text)

    # 2. Strip all resulting <...> tags.
    text_no_markup = re.sub(r'<[^>]+>', ' ', text_unscaped)

    # 3. Run the Aho-Corasick automaton on the markup-free text
    clean_parts = []
    last_end = 0
    for end_index, found_value in noise_model.iter(text_no_markup):
        start_index = end_index - len(found_value) + 1
        clean_parts.append(text_no_markup[last_end:start_index])
        clean_parts.append(" ")  # Replacement token
        last_end = end_index + 1

    clean_parts.append(text_no_markup[last_end:])
    almost_clean_text = "".join(clean_parts)

    # 4. Collapse multiple spaces
    sanitized_text = re.sub(r' +', ' ', almost_clean_text)

    return SanitizationResponse(sanitized_text=sanitized_text.strip())
