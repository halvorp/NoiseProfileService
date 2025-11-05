import ahocorasick

def filter_standalone_artifacts(text: str, noise_model: ahocorasick.Automaton) -> str:
    """
    Layer 2: Finds and removes standalone statistical artifacts.
    It preserves patterns that are embedded within larger, meaningful tokens.
    """
    if not text:
        return ""

    # This set will store the start and end indices of standalone noise patterns
    standalone_noise_indices = set()

    for end_index, found_value in noise_model.iter(text):
        start_index = end_index - len(found_value) + 1

        # [NEW VALIDATION STEP]
        # Check the character before the pattern
        is_preceded_by_alphanum = False
        if start_index > 0:
            preceding_char = text[start_index - 1]
            if preceding_char.isalnum():
                is_preceded_by_alphanum = True

        # Check the character after the pattern
        is_followed_by_alphanum = False
        if end_index + 1 < len(text):
            following_char = text[end_index + 1]
            if following_char.isalnum():
                is_followed_by_alphanum = True

        # If the pattern is embedded within a word, skip it.
        if is_preceded_by_alphanum and is_followed_by_alphanum:
            continue

        # Otherwise, it's standalone noise. Record its indices for removal.
        standalone_noise_indices.add((start_index, end_index + 1))

    # Build the new string, excluding the standalone noise segments
    clean_parts = []
    last_end = 0
    for start, end in sorted(list(standalone_noise_indices)):
        clean_parts.append(text[last_end:start])
        clean_parts.append(" ")  # Replacement token
        last_end = end

    clean_parts.append(text[last_end:])

    return "".join(clean_parts)
