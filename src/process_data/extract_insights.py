from dotenv import load_dotenv
import os
import json
import argparse
from .prompts import MINERAL_PROMPT, ADDITIVE_PROMPT, INGREDIENT_PROMPT
from .llm_connectors import GeminiConnector  # assuming you put GeminiConnector in this file
import time 
from utils.utils import extract_json_from_markdown
load_dotenv()

LLM_INSIGHTS_PATH = "/Users/bhushanshah/Documents/food-fact-check/data/llm_insights"

api_keys = [
    os.getenv("GOOGLE_GEMINI_API_KEY_1"),
    os.getenv("GOOGLE_GEMINI_API_KEY_2"),
    os.getenv("GOOGLE_GEMINI_API_KEY_3"),
    os.getenv("GOOGLE_GEMINI_API_KEY_4"),
]

def load_constituents(constituents_path):
    with open(constituents_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_insights(insights_path):
    if os.path.exists(insights_path):
        with open(insights_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_insights(insights_path, insights):
    with open(insights_path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)

def get_mineral_insights(connector, constituents, insights, model="gemini-2.5-flash-lite"):
    minerals = constituents.get("minerals", [])
    if "minerals" not in insights:
        insights["minerals"] = {}
    mineral_insights = insights.get("minerals", {})
    i = 0
    parse_num_retry = 0
    max_parse_retries = 2
    no_of_minerals = len(minerals)
    count = len(mineral_insights)
    print(f"Total minerals: {no_of_minerals}, Already have insights for: {count}, Remaining: {no_of_minerals - count}")
    while i < len(minerals):
        mineral = minerals[i]
        if mineral not in mineral_insights:
            print(f"Fetching insights for: {mineral}")
            prompt = MINERAL_PROMPT.format(mineral_name=mineral)
            response_text = connector.generate_content(model=model, prompt=prompt)
            structured = extract_json_from_markdown(response_text)
            if structured is None:
                if parse_num_retry < max_parse_retries:
                    parse_num_retry += 1
                    print(f"Failed to parse response for {mineral}, retrying... ({parse_num_retry}/{max_parse_retries})")
                    continue
                else:
                    print(f"Failed to parse response for {mineral} after {max_parse_retries} retries, skipping.")
            else:
                mineral_insights[mineral] = structured
                count += 1
                if count % 50 == 0:
                    print(f"Fetched insights for {count} minerals so far.")

        i += 1
        parse_num_retry = 0  # reset retry counter for next mineral
        time.sleep(1)  # brief pause to avoid hitting rate limits
    insights["minerals"] = mineral_insights
    return insights

def get_additives_insights(connector, constituents, insights, model="gemini-2.5-flash-lite"):
    additives = constituents.get("additives", [])
    if "additives" not in insights:
        insights["additives"] = {}
    additive_insights = insights.get("additives", {})
    i = 0
    parse_num_retry = 0
    max_parse_retries = 2
    no_of_additives = len(additives)
    count = len(additive_insights) # No of additives we already have insights for.
    print(f"Total additives: {no_of_additives}, Already have insights for: {count}, Remaining: {no_of_additives - count}")
    while i < len(additives):
        additive = additives[i]
        if additive not in additive_insights:
            print(f"Fetching insights for: {additive}")
            prompt = ADDITIVE_PROMPT.format(additive_name=additive)
            response_text = connector.generate_content(model=model, prompt=prompt)
            structured = extract_json_from_markdown(response_text)
            if structured is None:
                if parse_num_retry < max_parse_retries:
                    parse_num_retry += 1
                    print(f"Failed to parse response for {additive}, retrying... ({parse_num_retry}/{max_parse_retries})")
                    continue
                else:
                    print(f"Failed to parse response for {additive} after {max_parse_retries} retries, skipping.")
            else:
                additive_insights[additive] = structured
                count += 1
                if count % 50 == 0:
                    print(f"Fetched insights for {count} additives so far.")

        i += 1
        parse_num_retry = 0  # reset retry counter for next additive
        time.sleep(1)  # brief pause to avoid hitting rate limits
    insights["additives"] = additive_insights
    return insights

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--constituents_path", type=str, required=True, help="Path to constituents.json")
    parser.add_argument("--model", type=str, required=True, help="Model to use for insights")
    parser.add_argument("--type_of_constituent", type=str, required=True, choices=["minerals", "additives", "ingredients"], help="Type of constituent to process('minerals', 'additives', 'ingredients')")
    args = parser.parse_args()

    constituents = load_constituents(args.constituents_path)
    if args.model == 'gemini':
        insights_path = os.path.join(LLM_INSIGHTS_PATH, "gemini", "gemini_insights.json")
        connector = GeminiConnector(api_keys=api_keys)

    insights = load_insights(insights_path)

    if args.type_of_constituent == "minerals":
        insights = get_mineral_insights(connector, constituents, insights)

    elif args.type_of_constituent == "additives":
        insights = get_additives_insights(connector, constituents, insights)

    save_insights(insights_path, insights)
    print("Insights updated and saved ✅")


