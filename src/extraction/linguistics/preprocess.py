"""This is the module that contains preprocessing functions for the news text.
"""

import spacy

tokenizer = spacy.load("en_core_web_sm")

def get_paragraphs(text):
    """Split texts into pargraphs.

    Args:
        text: A string that contains the whole news text.

    Returns:
        A list of strings that represents each paragraph.
    """
    return list(map(str.strip ,text.lower().split("\n")))

def filter_paragraphs(paragraphs, keyword):
    """Filter all paragraphs in the news to extract only paragraphs related to the keyword.

    Args:
        paragraphs: A list of paragraphs.
        tokenizer: The spacy tokenizer.
        keyword: A string that represents the keyword used to query the news.

    Returns:
        A list of filtered paragraphs.
    """
    results = []
    for paragraph in paragraphs:
        tokens = tokenizer(paragraph)
        words = set()
        for token in tokens:
            words.add(token.text)
        if keyword in words:
            results.append(paragraph)

    return results