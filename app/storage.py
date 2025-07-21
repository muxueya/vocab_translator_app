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
    if any(entry["original"] == original for entry in wordbook):
        return False
    wordbook.append({"original": original, "translated": translated})
    with open(WORD_BOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(wordbook, f, ensure_ascii=False, indent=2)
    return True

def export_wordbook_to_anki(filename=None):
    """
    Export the wordbook as a tab-delimited text file with Anki import headers,
    so it can be directly imported as Basic cards into Anki.
    Each note must be on one line; we strip out any stray newlines in HTML.
    """
    if filename is None:
        filename = ANKI_EXPORT_PATH
    wordbook = load_wordbook()
    try:
        with open(filename, "w", encoding="utf-8") as f:
            # === Anki import headers ===
            f.write("#separator:Tab\n")
            f.write("#columns:Word\tDefinition\n")
            f.write("#notetype:Basic\n")
            f.write("#deck:Vocabulary\n")
            # ===========================
            for entry in wordbook:
                original = entry["original"]
                definition = entry["translated"]

                # === CHANGES START ===
                # 1) Strip literal newlines so each record stays on one line
                definition = definition.replace("\r", "").replace("\n", "")

                # 2) (Optional) collapse multiple spaces to a single space
                # import re
                # definition = re.sub(r"\s+", " ", definition)

                # 3) If your HTML came from QTextEdit.toHtml(), you may want
                #    to remove the surrounding HTML header/footer:
                #    definition = re.sub(r"^.*<body[^>]*>|</body>.*$", "", definition)
                # === CHANGES END ===

                f.write(f"{original}\t{definition}\n")

        print(f"[✓] Exported {len(wordbook)} entries to {filename}")
    except Exception as e:
        raise RuntimeError(f"Failed to export to Anki: {e}")
