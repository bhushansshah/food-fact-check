import json
import argparse
from datasets import load_from_disk

def extract_tags(dataset_path, output_json_path):
    # Load dataset
    dataset = load_from_disk(dataset_path)

    ingredients_set = set()
    additives_set = set()
    minerals_set = set()
    nutriments_set = set()
    counter = 0
    for example in dataset:
        # --- Ingredients ---
        for ing in example.get("ingredients_tags", []) or []:
            lang = ing.split(":")[0]
            if lang == "en":  # only keep English ingredients
                ingredients_set.add(ing)

        # --- Additives ---
        for add in example.get("additives_tags", []) or []:
            lang = add.split(":")[0]
            if lang == "en":  # only keep English additives
                additives_set.add(add)

        # --- Minerals ---
        for min_ in example.get("minerals_tags", []) or []:
            lang = min_.split(":")[0]
            if lang == "en":  # only keep English minerals
                minerals_set.add(min_)

        # --- Nutriments ---
        for nutri in example.get("nutriments", []) or []:
            name = nutri.get('name', None)
            if name:
                nutriments_set.add(name)
        counter += 1
        if counter % 1000 == 0:
            print(f"Processed {counter} examples...")

    # Add additives + minerals to ingredients if not already there
    ingredients_set.update(additives_set)
    ingredients_set.update(minerals_set)

    result = {
        "ingredients": sorted(ingredients_set),
        "additives": sorted(additives_set),
        "minerals": sorted(minerals_set),
        "nutriments": sorted(nutriments_set),
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Tags extracted and saved to {output_json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ingredient/additive/mineral/nutrient tags from OpenFoodFacts dataset.")
    parser.add_argument("--dataset_path", required=True, help="Path to the saved dataset (load_from_disk).")
    parser.add_argument("--output_json", required=True, help="Path to save the extracted JSON file.")
    args = parser.parse_args()

    extract_tags(args.dataset_path, args.output_json)
