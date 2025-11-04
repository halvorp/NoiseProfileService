import ahocorasick
import json
from pathlib import Path
from typing import List

def load_noise_model(profile_path: Path) -> ahocorasick.Automaton:
    """Loads the noise profile and compiles it into an Aho-Corasick automaton."""
    with open(profile_path, "r") as f:
        noise_patterns = json.load(f)

    automaton = ahocorasick.Automaton()
    for pattern in noise_patterns:
        automaton.add_word(pattern, pattern)

    automaton.make_automaton()
    return automaton
