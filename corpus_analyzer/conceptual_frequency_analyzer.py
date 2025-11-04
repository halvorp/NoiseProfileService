from typing import Dict, List
import numpy as np

def identify_noise_patterns(
    ngram_counts: Dict[str, int],
    frequency_percentile: float = 99.9,
    unique_char_threshold: int = 3
) -> List[str]:
    """Identifies noise patterns from n-gram counts based on frequency and complexity."""
    if not ngram_counts:
        return []

    frequencies = np.array(list(ngram_counts.values()))
    if len(frequencies) == 0:
        return []

    freq_threshold = np.percentile(frequencies, frequency_percentile)

    noise_patterns = []
    for ngram, count in ngram_counts.items():
        if count >= freq_threshold:
            unique_chars = len(set(ngram))
            if unique_chars <= unique_char_threshold:
                noise_patterns.append(ngram)

    return noise_patterns
