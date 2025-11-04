from pathlib import Path
import json
from utils.conceptual_text_io import read_text_files
from corpus_analyzer.conceptual_char_ngram_builder import generate_char_ngrams
from corpus_analyzer.conceptual_frequency_analyzer import identify_noise_patterns

def main():
    """Orchestrates the offline noise profile generation."""
    corpus_dir = Path("corpus")
    texts = read_text_files(corpus_dir)

    if not texts:
        print("No text files found in the corpus directory. Skipping profile generation.")
        return

    ngram_counts = generate_char_ngrams(texts)
    noise_patterns = identify_noise_patterns(ngram_counts)

    with open("conceptual_noise_profile.json", "w") as f:
        json.dump(noise_patterns, f, indent=2)

    print(f"Generated noise profile with {len(noise_patterns)} patterns.")

if __name__ == "__main__":
    main()
