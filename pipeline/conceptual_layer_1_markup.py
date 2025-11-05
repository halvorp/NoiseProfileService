import re
import html

def strip_markup(text: str) -> str:
    """
    Layer 1: Deterministically strips HTML markup from a text.
    1. Un-escapes HTML entities (e.g., &lt; -> <).
    2. Strips all resulting <...> tags.
    """
    # 1. Un-escape HTML entities
    text_unscaped = html.unescape(text)

    # 2. Strip all resulting <...> tags, replacing them with a space
    text_no_markup = re.sub(r'<[^>]+>', ' ', text_unscaped)

    return text_no_markup
