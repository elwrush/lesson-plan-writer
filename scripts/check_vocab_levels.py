import argparse
import json
import sys
import urllib.request
from pathlib import Path

OXFORD_URL = "https://raw.githubusercontent.com/tyypgzl/Oxford-5000-words/main/full-word.json"
CACHE_PATH = Path(__file__).parent / ".oxford5000_cache.json"


def load_oxford():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    print("Downloading Oxford 5000...", file=sys.stderr)
    data = urllib.request.urlopen(OXFORD_URL).read()
    entries = json.loads(data)
    lookup = {}
    for w in entries:
        key = w["value"]["word"].lower().strip()
        t = w["value"].get("type", "")
        lvl = w["value"].get("level", "?")
        lookup.setdefault(key, []).append({"type": t, "level": lvl})
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(lookup, f)
    return lookup


def check_vocab(text, min_level="B2", max_words=5):
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lookup = load_oxford()

    level_order = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    min_rank = level_order.get(min_level, 4)

    results = []
    seen_lemmas = set()

    for token in doc:
        if token.is_punct or token.is_space or token.is_stop:
            continue
        lemma = token.lemma_.lower()
        if lemma in seen_lemmas:
            continue
        if lemma not in lookup:
            continue

        for entry in lookup[lemma]:
            entry_rank = level_order.get(entry["level"], 0)
            if entry_rank >= min_rank:
                seen_lemmas.add(lemma)
                results.append(
                    {
                        "word_form": token.text.lower(),
                        "lemma": lemma,
                        "pos": token.pos_,
                        "oxford_level": entry["level"],
                        "oxford_type": entry["type"],
                    }
                )
                break

    results.sort(key=lambda r: (level_order.get(r["oxford_level"], 0), r["lemma"]))

    if max_words:
        results = results[:max_words]

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check vocabulary CEFR levels using spaCy lemmatization + Oxford 5000"
    )
    parser.add_argument("text", nargs="?", help="Text to analyse (or use --file)")
    parser.add_argument("--file", "-f", type=Path, help="File to read text from")
    parser.add_argument(
        "--min-level",
        default="B2",
        choices=["A1", "A2", "B1", "B2", "C1", "C2"],
        help="Minimum CEFR level to report (default: B2)",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=0,
        help="Maximum words to return (0 = all)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        parser.error("Provide text or --file")

    results = check_vocab(text, args.min_level, args.max_words or 0)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(
                f"  {r['word_form']:20s} -> {r['lemma']:20s} {r['oxford_level']:4s} ({r['oxford_type']})"
            )
        print(f"\n  Total: {len(results)} words at {args.min_level}+")


if __name__ == "__main__":
    main()
