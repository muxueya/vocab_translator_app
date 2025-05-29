#!/usr/bin/env python3
"""
Simple script to look up words using Folkets lexikon web service.
"""
import requests
import sys

API_URL = 'https://folkets-lexikon.csc.kth.se/folkets/service'


def lookup(word, lang='sv', interface='sv'):
    """
    Fetch and print raw HTML result for a given word.

    :param word: the word to look up
    :param lang: source language ('sv', 'en', or 'both')
    :param interface: interface language for headings ('sv' or 'en')
    """
    params = {
        'word': word,
        'lang': lang,
        'interface': interface
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    # Print raw HTML; you can extend this to parse HTML with BeautifulSoup
    print(response.text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        word = input("Enter a word to look up: ")
    else:
        word = sys.argv[1]

    # Optional: change source and interface languages
    # For Swedish-English lookup with English headings:
    # lookup(word, lang='sv', interface='en')
    lookup(word)
