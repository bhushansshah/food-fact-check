import json
import argparse


def extract_ingredients(tags):
    ingredients = {}
    for key, value in tags.items():
        if value >= 100:  # only keep ingredients that appear at least 100 times
            # remove "en:" prefix
            ingredient = key.replace("en:", "")
            ingredients[ingredient] = value

    extracted_ingredients_dict = sorted(ingredients.items(), key=lambda item: item[1], reverse=True)
    extracted_ingredients = [item[0] for item in extracted_ingredients_dict]
    return extracted_ingredients

def process_ingredients(input_json, output_json):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    ingredients_tags = data.get("ingredients", [])
    processed = extract_ingredients(ingredients_tags)

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
