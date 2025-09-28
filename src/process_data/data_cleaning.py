import argparse
from datasets import load_from_disk
import json

def build_image_url(code, key, rev, size="400"):
    """Build OpenFoodFacts image URL from code and rev."""
    code_str = str(code)
    # split into 3-3-3-4
    parts = [code_str[i:i+3] for i in range(0, len(code_str)-4, 3)]
    parts.append(code_str[len(parts)*3:])
    path = "/".join(p for p in parts if p)  # join non-empty chunks
    return f"https://images.openfoodfacts.org/images/products/{path}/{key}.{rev}.{size}.jpg"

def process_openfoodfacts(input_dataset_path, output_dataset_path, columns_to_keep, additives_mapping):
    # Load dataset
    dataset = load_from_disk(input_dataset_path)

    def has_required_fields(example):
        # --- Check required fields ---
        required_fields = ["brands", "code", "ingredients_text", "nutriments", "product_name"]
        for field in required_fields:
            value = example.get(field, None)
            if value is None or (isinstance(value, (list, str, dict)) and len(value) == 0):
                return False

        return True

    dataset = dataset.filter(has_required_fields)

    # Step 2: create image_url column
    def add_image_url(example):
        images = example["images"]
        code = example.get("code")
        url = None
        for img in images:
            if (
                img.get("key", "").startswith("front_")
                and img.get("imgid") is not None
                and img.get("rev") is not None
                and img.get("sizes")
            ):
                rev = img["rev"]
                key = img["key"]
                # pick preferred size: full if exists, else first available
                size = "full" if "full" in img["sizes"] else max(list(img["sizes"].keys()))
                url = build_image_url(code, key, rev, size)
                break
        example["image_url"] = url
        return example
    
    def add_additives(example):
        additives_tags = example.get("additives_tags", [])
        if additives_tags is None:
            additives_tags = []
        example["additives"] = [tag.replace("en:", "") + additives_mapping.get(tag.replace("en:", ""), "") for tag in additives_tags if tag.startswith("en:")]
        return example

    dataset = dataset.map(add_image_url)
    dataset = dataset.map(add_additives)
    # Step 3: keep only required columns + new image_url
    keep = set(columns_to_keep + ["image_url", "additives"])
    dataset = dataset.remove_columns([col for col in dataset.column_names if col not in keep])

    # Save dataset
    dataset.save_to_disk(output_dataset_path)
    print(f"Processed dataset saved to {output_dataset_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process OpenFoodFacts dataset.")
    parser.add_argument("--input_dir", required=True, help="Path to the input dataset directory.")
    parser.add_argument("--output_dir", required=True, help="Directory to save the processed dataset.")
    parser.add_argument("--additives_mapping", required=True, help="Path to the additives mapping JSON file.")
    args = parser.parse_args()
    additives_mapping_path = args.additives_mapping

    with open(additives_mapping_path, 'r') as f:
        additives_mapping = json.load(f)
        print(f"Loaded additives mapping with {len(additives_mapping)} entries.")

    columns_to_keep = [
        "code", "additives_n", "additives_tags", "brands", "compared_to_category",
        "images", "ingredients_tags", "ingredients_text", "ingredients_analysis_tags",
        "lang", "languages_tags", "nutriments", "product_name",
        "vitamins_tags", "minerals_tags", "nutrient_levels_tags"
    ]
    process_openfoodfacts(args.input_dir, args.output_dir, columns_to_keep, additives_mapping)
