from langdetect import detect
from googletrans import Translator
from bs4 import BeautifulSoup
import requests

translator = Translator()
API_URL = 'https://folkets-lexikon.csc.kth.se/folkets/service'

def fetch_html(word, lang='sv', interface='en'):
    params = {'word': word, 'lang': lang, 'interface': interface}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.text


def get_formatted_entry(word):
    """
    Fetch and format a Swedish word entry from Folkets lexikon.
    Returns a structured raw text summary with all available information.
    """
    html = fetch_html(word)
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    if not paragraphs:
        return None

    entries = []
    for p in paragraphs:
        # Remove images to avoid alt-text clutter
        for img in p.find_all('img'):
            img.decompose()
        # Extract text lines with line breaks
        text = p.get_text(separator='\n')
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            continue
        # Indent secondary lines for readability
        formatted = []
        for idx, line in enumerate(lines):
            if idx == 0:
                formatted.append(line)
            else:
                formatted.append('  ' + line)
        entries.append('\n'.join(formatted))

    # Join all paragraph entries with a blank line
    return '\n\n'.join(entries)


def translate_text(text):
    """
    Detect language and translate text. For single Swedish words, use Folkets lookup.
    """
    try:
        src = detect(text)
        dest = 'en' if src == 'sv' else 'sv'
        if src == 'sv' and len(text.strip().split()) == 1:
            entry = get_formatted_entry(text.strip())
            if entry:
                return entry
        return translator.translate(text, src=src, dest=dest).text
    except Exception as e:
        return f"[Error] {e}"
