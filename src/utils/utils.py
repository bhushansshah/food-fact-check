from markdown_it import MarkdownIt
import json

def extract_json_from_markdown(md_text: str) -> dict:
    md = MarkdownIt()
    try:
        tokens = md.parse(md_text)
        for token in tokens:
            if token.type == "fence" and token.info.strip() == "json":
                return json.loads(token.content)
    except Exception as e:
        print(f"Error parsing markdown: {e}")
    
    return {"is_success": 0}