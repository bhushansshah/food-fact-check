import json
import argparse


def extract_ingredients(tags):
    ingredients = {}
    for key, value in tags.items():
        if value >= 50:  # only keep ingredients that appear at least 50 times
            # remove "en:" prefix
            ingredient = key.replace("en:", "")
            ingredients[ingredient] = value

    extracted_ingredients_dict = sorted(ingredients.items(), key=lambda item: item[1], reverse=True)
    extracted_ingredients = [item[0] for item in extracted_ingredients_dict]
    return extracted_ingredients

def map_additives(mapping, additives):
    mapped = []
    for additive in additives:
        additive_tag = additive.lower().replace("en:", "")
        if additive_tag in mapping:
            mapped.append(additive_tag + " " + mapping[additive_tag])
        else:
            mapped.append(additive_tag)
    return mapped

def map_minerals(minerals):
    mapped = []
    for mineral in minerals:
        mineral = mineral.lower().replace("en:", "")
        mapped.append(mineral)
    return mapped

def process_ingredients(input_json, output_json, additives_mapping_path="/Users/bhushanshah/Documents/food-fact-check/data/processed/additives_mapping.json"):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(additives_mapping_path, "r", encoding="utf-8") as f:
        additives_mapping = json.load(f)

    ingredients_tags = data.get("ingredients", [])
    additives = data.get("additives", [])
    processed = extract_ingredients(ingredients_tags)

    data['ingredients'] = processed
    data['additives'] = map_additives(additives_mapping, additives)
    data['minerals'] = map_minerals(data.get("minerals", []))
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Processed {len(processed)} ingredients and mapped additives and saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean OpenFoodFacts ingredient tags with NLTK")
    parser.add_argument("--input_json", required=True, help="Path to input JSON file containing raw tags")
    parser.add_argument("--output_json", required=True, help="Path to save processed JSON file")
    args = parser.parse_args()

    process_ingredients(args.input_json, args.output_json)
