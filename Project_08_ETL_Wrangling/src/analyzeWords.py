import re
import pandas as pd
import numpy as np


def analyzeWords(words):
    """
    Analyzes a Series of words and returns various statistics.

    Args:
        words: pandas Series of words

    Returns:
        Dictionary containing letter counts, max length, size counts,
        and information about words with 'oo' and 6+ characters
    """
    # Clean the data - remove nulls, strip whitespace, remove empty strings
    cleaned = words.dropna().astype(str).str.strip()
    cleaned = cleaned[cleaned.str.len() > 0]
    lowercase = cleaned.str.lower()

    # Handle empty input
    if cleaned.empty:
        empty_letters = {letter: 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
        return {
            "letter_counts": empty_letters,
            "max_char": 0,
            "size_counts": {},
            "oo_count": 0,
            "oo_words": pd.Series(dtype=object),
            "words_6plus": pd.Series(dtype=object),
            "words_6plus_count": 0,
        }

    # Count words starting with each letter using regex
    letter_counts = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        pattern = '^' + letter
        matches = lowercase.str.match(pattern)
        letter_counts[letter] = int(matches.sum())

    # Find the longest word
    word_lengths = cleaned.str.len()
    max_char = int(word_lengths.max())

    # Count words of each length
    size_counts = {}
    for length in range(1, max_char + 1):
        count = (word_lengths == length).sum()
        size_counts[length] = int(count)

    # Find words containing 'oo' using regex
    oo_pattern = 'oo'
    has_oo = lowercase.str.contains(oo_pattern, regex=True)
    oo_count = int(has_oo.sum())
    # Changed from w_clean[mask_oo].reset_index(drop=True)
    oo_words = lowercase[has_oo].sort_values()
    #  Keep original index AND use lowercase


    # Find words with 6 or more characters
    is_long = word_lengths >= 6
    words_6plus_count = int(is_long.sum())
    # Keep original index AND use lowercase
    words_6plus = lowercase[is_long].sort_values()

    # Return all results as a dictionary
    return {
        "letter_counts": letter_counts,
        "max_char": max_char,
        "size_counts": size_counts,
        "oo_count": oo_count,
        "oo_words": oo_words,
        "words_6plus": words_6plus,
        "words_6plus_count": words_6plus_count,
    }