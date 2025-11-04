from collections import Counter
from typing import List, Dict

def generate_char_ngrams(texts: List[str], n_min: int = 3, n_max: int = 20) -> Dict[str, int]:
    """Generates character n-grams from a list of texts."""
    ngram_counts = Counter()
    for text in texts:
        for n in range(n_min, n_max + 1):
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                ngram_counts[ngram] += 1
    return ngram_counts
