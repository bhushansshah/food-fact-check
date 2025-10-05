MINERAL_PROMPT = """
You are given the name of a mineral found in food products. 
Your task is to extract the below fields about the mineral mentioned.

Fields:
- is_safe: 1 if the mineral is generally safe at normal levels, 0 if unsafe.
- is_safe_in_excess: 1 if harmful in excess amounts, 0 if not.
- is_macro_mineral: 1 if it is a macro mineral (needed in large amounts like calcium, potassium), else 0.
- is_natural: 1 if typically found in natural food sources, 0 if usually synthetic or fortified.
- is_controversial: 1 if there is debate/health concern about this mineral, 0 if not.
- is_commonly_used_in_marketing: 1 if food companies often highlight this mineral for marketing claims, 0 if not.
- is_synthetic: 1 if it is typically made artificially in food processing, 0 otherwise.
- is_success: 1 if the mineral is recognized and fields are filled, 0 if not recognized.

Input Mineral: "{mineral_name}"

Important Note: Respond strictly in JSON format following the exact structure shown.
If the mentioned mineral is not recognized, then respond with "is_success": 0 and set all other fields to 0.

Output format (must follow exactly):
```json
{{
  "is_safe": 0 or 1,
  "is_safe_in_excess": 0 or 1,
  "is_macro_mineral": 0 or 1,
  "is_natural": 0 or 1,
  "is_controversial": 0 or 1,
  "is_commonly_used_in_marketing": 0 or 1,
  "is_synthetic": 0 or 1,
  "is_success": 0 or 1
}}
```
"""

ADDITIVE_PROMPT = """
You are given the name of a food additive. 
Your task is to extract the below fields. 

Fields:
- is_preservative: 1 if the additive functions as a preservative, 0 if not.
- is_colorant: 1 if it is used as a coloring agent, 0 if not.
- is_sweetener: 1 if it is used as a sweetener, 0 if not.
- is_emulsifier: 1 if it is used as an emulsifier/stabilizer, 0 if not.
- is_flavor_enhancer: 1 if it is used to enhance flavor, 0 if not.
- is_antioxidant: 1 if it functions as an antioxidant, 0 if not.
- is_natural: 1 if usually derived from natural sources, 0 if not.
- is_controversial: 1 if debated/linked with health risks, 0 if not.
- is_commonly_used_in_marketing: 1 if often highlighted on packaging (e.g., "no artificial colors"), 0 if not.
- is_synthetic: 1 if typically produced artificially in the food industry, 0 otherwise.
- is_natural: 1 if usually derived from natural sources, 0 if not.
- is_success: 1 if the additive is recognized and fields are filled, 0 if not recognized.

Input Additive: "{additive_name}"

Important Note: Respond strictly in JSON format following the exact structure shown.
If the mentioned additive is not recognized, then respond with "is_success": 0 and set all other fields to 0.

Output format (must follow exactly):
```json
{{
  "is_preservative": 0 or 1,
  "is_colorant": 0 or 1,
  "is_sweetener": 0 or 1,
  "is_emulsifier": 0 or 1,
  "is_flavor_enhancer": 0 or 1,
  "is_antioxidant": 0 or 1,
  "is_natural": 0 or 1,
  "is_controversial": 0 or 1,
  "is_commonly_used_in_marketing": 0 or 1,
  "is_synthetic": 0 or 1,
  "is_natural": 0 or 1,
  "is_success": 0 or 1
}}
```
"""


INGREDIENT_PROMPT = """
You are given the name of a food ingredient. 
Your task is to extract the below mentioned fields. 

Fields:
- is_plant_based: 1 if derived from plants, 0 otherwise.
- is_animal_based: 1 if derived from animals, 0 otherwise.
- is_allergen: 1 if commonly known allergen (e.g., milk, peanuts), 0 otherwise.
- is_processed: 1 if significantly processed/refined, 0 if whole/unprocessed.
- is_whole_food: 1 if it is a whole/raw food ingredient (like rice, apple), 0 otherwise.
- is_natural: 1 if typically natural, 0 if artificial.
- is_controversial: 1 if debated or linked with health risks, 0 if not.
- is_commonly_used_in_marketing: 1 if often used in product marketing (e.g., "made with real oats"), 0 if not.
- is_antioxidant: 1 if known to have antioxidant properties, 0 otherwise.
- is_synthetic: 1 if usually artificial or lab-produced, 0 otherwise.
- is_natural: 1 if usually derived from natural sources, 0 if not.
- is_success: 0 or 1 if the ingredient is recognized and fields are filled, 0 if not recognized.

Input Ingredient: "{ingredient_name}"

Important Note: Respond strictly in JSON format following the exact structure shown.
If the mentioned ingredient is not recognized, then respond with all fields set to 0.

Output format (must follow exactly):
```json
{{
  "is_plant_based": 0 or 1,
  "is_animal_based": 0 or 1,
  "is_allergen": 0 or 1,
  "is_processed": 0 or 1,
  "is_whole_food": 0 or 1,
  "is_natural": 0 or 1,
  "is_controversial": 0 or 1,
  "is_commonly_used_in_marketing": 0 or 1,
  "is_antioxidant": 0 or 1,
  "is_synthetic": 0 or 1,
  "is_natural": 0 or 1,
  "is_success": 0 or 1
}}
```
"""
