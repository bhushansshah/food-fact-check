import re
import json
import argparse
import nltk
nltk.download("punkt_tab")
nltk.download("maxent_ne_chunker_tab")
nltk.download("words")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag, ne_chunk

def clean_tag(tag):
    """Remove language prefix, numbers, and normalize text."""
    # only keep en: tags
    if not tag.startswith("en:"):
        return None
    text = tag[3:]  # remove "en:"
    text = re.sub(r"\d+", "", text)  # remove digits
    text = text.replace("-", " ").strip()
    return text if text else None

def extract_ingredients(tags):
    stop_words = set(stopwords.words("english"))
    ingredients = set()
    counter = 0
    for tag in tags:
        cleaned = clean_tag(tag)
        if not cleaned:
            continue

        tokens = word_tokenize(cleaned)
        tokens = [t for t in tokens if t.lower() not in stop_words]

        if not tokens:
            continue

        # POS tagging
        pos_tags = pos_tag(tokens)

        # Named Entity Recognition
        chunks = ne_chunk(pos_tags, binary=True)

        # collect words labeled as NE or NOUNS
        for word, pos in pos_tags:
            if pos.startswith("NN"):  # noun
                ingredients.add(word.lower())
        
        counter += 1
        if counter % 1000 == 0:
            print(f"Processed {counter} tags...")

    return sorted(ingredients)

def process_ingredients(input_json, output_json):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_tags = data.get("ingredients", [])
    processed = extract_ingredients(raw_tags)

    result = {"ingredients": processed}

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Processed {len(processed)} ingredients saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean OpenFoodFacts ingredient tags with NLTK")
    parser.add_argument("--input_json", required=True, help="Path to input JSON file containing raw tags")
    parser.add_argument("--output_json", required=True, help="Path to save processed JSON file")
    args = parser.parse_args()

    process_ingredients(args.input_json, args.output_json)
