from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from .conceptual_noise_model_loader import load_noise_model
from pipeline.conceptual_layer_1_markup import strip_markup
from pipeline.conceptual_layer_2_artifacts import filter_standalone_artifacts
from pipeline.conceptual_layer_3_whitespace import normalize_whitespace

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
    """Orchestrates the sanitization pipeline."""
    if noise_model is None:
        raise HTTPException(status_code=500, detail="Noise model not loaded.")

    # Layer 1: Deterministic Markup Stripping
    text_no_markup = strip_markup(request.text)

    # Layer 2: Token-Aware Artifact Filtering
    text_no_artifacts = filter_standalone_artifacts(text_no_markup, noise_model)

    # Layer 3: Whitespace Normalization
    sanitized_text = normalize_whitespace(text_no_artifacts)

    return SanitizationResponse(sanitized_text=sanitized_text)
