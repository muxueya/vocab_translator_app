from googletrans import Translator
from langdetect import detect
from app.config import DEFAULT_SOURCE_LANG

translator = Translator()


def translate_text(text):
    try:
        src_lang = detect(text)
        dest_lang = "en" if src_lang == "sv" else "sv"
        return translator.translate(text, src=src_lang, dest=dest_lang).text
    except Exception as e:
        return f"[Translation Error] {e}"
