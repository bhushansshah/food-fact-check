import json
import argparse
from datasets import load_from_disk

def extract_tags(dataset_path, output_json_path):
    # Load dataset
    dataset = load_from_disk(dataset_path)

    ingredients_dict = {}
    additives_set = set()
    minerals_set = set()
    nutriments_set = set()
    counter = 0
    for example in dataset:
        # --- Ingredients ---
        # for ing in example.get("ingredients_text", []) or []:
        #     lang = ing.split(":")[0]
        #     if lang == "en":  # only keep English ingredients
        #         ingredients_set.add(ing)
        for ing in example.get("ingredients_tags", []) or []:
            if ing.startswith("en:"):
                if ingredients_dict.get(ing) is None:
                    ingredients_dict[ing] = 1
                else:
                    ingredients_dict[ing] += 1

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

    #Add additives and minerals to ingredients_dict
    for add in additives_set:
        if ingredients_dict.get(add) is None:
            ingredients_dict[add] = 1

    for min_ in minerals_set:
        if ingredients_dict.get(min_) is None:
            ingredients_dict[min_] = 1

    print("The length of ingredients - ", len(ingredients_dict))
    result = {
        "ingredients": ingredients_dict,
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
