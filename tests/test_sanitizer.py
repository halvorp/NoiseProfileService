import unittest
import json
from pathlib import Path
from corpus_analyzer.conceptual_char_ngram_builder import generate_char_ngrams
from corpus_analyzer.conceptual_frequency_analyzer import identify_noise_patterns
from noise_filter.conceptual_noise_model_loader import load_noise_model
from noise_filter.conceptual_filter_workflow import SanitizationRequest, sanitize_text
from fastapi.testclient import TestClient
from noise_filter.conceptual_filter_workflow import app

class TestSanitizer(unittest.TestCase):

    def test_ngram_generation(self):
        texts = ["abcde"]
        ngrams = generate_char_ngrams(texts, n_min=3, n_max=3)
        self.assertEqual(ngrams["abc"], 1)
        self.assertEqual(ngrams["bcd"], 1)
        self.assertEqual(ngrams["cde"], 1)

    def test_noise_identification(self):
        ngram_counts = {"_______": 100, "abc": 10, "\n \n \n": 100}
        noise = identify_noise_patterns(ngram_counts)
        self.assertIn("_______", noise)
        self.assertIn("\n \n \n", noise)
        self.assertNotIn("abc", noise)

    def test_sanitization_workflow(self):
        # Create a dummy noise profile
        with open("conceptual_noise_profile.json", "w") as f:
            json.dump(["_______", "******"], f)

        with TestClient(app) as client:
            # Test case 1: Basic sanitization
            response = client.post("/sanitize", json={"text": "Hello _______ world ******"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["sanitized_text"], "Hello world ")

            # Test case 2: Preserve newlines
            response = client.post("/sanitize", json={"text": "Hello\nworld ******"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["sanitized_text"], "Hello\nworld ")

if __name__ == "__main__":
    unittest.main()
