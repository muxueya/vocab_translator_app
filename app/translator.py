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
    Fetch and return an HTML fragment of Folkets lexikon entries for a single word,
    replacing flag images with emojis.
    """
    html = fetch_html(word)
    soup = BeautifulSoup(html, 'html.parser')

    # === CHANGES: handle flag images ===
    for img in soup.find_all('img'):
        src = img.get('src', '').lower()
        alt = img.get('alt', '').lower()
        # English flag?
        if 'eng' in alt or 'english' in src:
            img.replace_with('🇬🇧')
        # Swedish flag?
        elif 'sv' in alt or 'swedish' in src or 'svenska' in alt:
            img.replace_with('🇸🇪')
        else:
            # All other images removed
            img.decompose()
    # === END CHANGES ===

    paragraphs = soup.find_all('p')
    if not paragraphs:
        return None

    # Join their raw HTML together
    entry_html = ''.join(str(p) for p in paragraphs)
    return entry_html



def translate_text(text):
    """
    Detect language and translate text using Google Translate.
    """
    try:
        src = detect(text)
        dest = 'en' if src == 'sv' else 'sv'
        return translator.translate(text, src=src, dest=dest).text
    except Exception as e:
        return f"[Error] {e}"
