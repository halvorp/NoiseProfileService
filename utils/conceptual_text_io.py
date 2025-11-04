from pathlib import Path
import codecs
from typing import List

def read_text_files(directory: Path) -> List[str]:
    """Reads all text files from a directory and returns their content."""
    texts = []
    for filepath in directory.glob("*.txt"):
        with codecs.open(filepath, "r", encoding="utf-8") as f:
            texts.append(f.read())
    return texts
