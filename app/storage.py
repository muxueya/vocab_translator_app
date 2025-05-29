import json
import os
from app.config import WORD_BOOK_PATH, ANKI_EXPORT_PATH

def load_wordbook():
    if not os.path.exists(WORD_BOOK_PATH):
        return []
    try:
        with open(WORD_BOOK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_to_wordbook(original, translated):
    wordbook = load_wordbook()
    wordbook.append({"original": original, "translated": translated})
    with open(WORD_BOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(wordbook, f, ensure_ascii=False, indent=2)

def export_wordbook_to_anki(filename=None):
    if filename is None:
        filename = ANKI_EXPORT_PATH
    wordbook = load_wordbook()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for entry in wordbook:
                f.write(f"{entry['original']}\t{entry['translated']}\n")
        print(f"[✓] Exported {len(wordbook)} entries to {filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to export to Anki: {e}")

