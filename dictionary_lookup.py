#!/usr/bin/env python3
"""
Simple script to look up Swedish words using the Dictionary API (https://dictionaryapi.dev/).
"""
import requests
import sys

def lookup(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/sv/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"No entry found for '{word}'.")
        return
    data = response.json()
    for entry in data:
        print(f"Word: {entry.get('word', word)}")
        for meaning in entry.get('meanings', []):
            part_of_speech = meaning.get('partOfSpeech', '')
            for definition in meaning.get('definitions', []):
                print(f"  ({part_of_speech}) {definition.get('definition')}")
                example = definition.get('example')
                if example:
                    print(f"     e.g.: {example}")
        print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = input("Enter a Swedish word to look up: ")
    lookup(word)
