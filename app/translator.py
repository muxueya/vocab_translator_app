from googletrans import Translator
from app.config import DEFAULT_SOURCE_LANG

def translate_text(text):
    translator = Translator()
    src = DEFAULT_SOURCE_LANG
    dest = "en" if any(char in text.lower() for char in "åäö") else "sv"
    return translator.translate(text, src=src, dest=dest).text

