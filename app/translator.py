from googletrans import Translator
from app.config import DEFAULT_SOURCE_LANG, DEFAULT_TARGET_LANG

def translate_text(text):
    translator = Translator()
    src = DEFAULT_SOURCE_LANG
    # Quick heuristic: if Swedish chars, translate to English
    if any(char in text.lower() for char in "åäö"):
        dest = "en"
    else:
        dest = "sv"
    return translator.translate(text, src=src, dest=dest).text