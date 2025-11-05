import re

def normalize_whitespace(text: str) -> str:
    """
    Layer 3: Normalizes whitespace in a text.
    Collapses multiple spaces into a single space and strips leading/trailing whitespace.
    """
    # Collapse multiple spaces into a single space, without affecting newlines
    text_with_collapsed_spaces = re.sub(r' +', ' ', text)

    # Strip leading/trailing whitespace
    return text_with_collapsed_spaces.strip()
