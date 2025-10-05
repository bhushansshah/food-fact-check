from markdown_it import MarkdownIt
import json

def extract_json_from_markdown(md_text: str) -> dict:
    md = MarkdownIt()
    tokens = md.parse(md_text)
    for token in tokens:
        if token.type == "fence" and token.info.strip() == "json":
            try:
                return json.loads(token.content)
            except Exception:
                return {"is_success": 0}
    return {"is_success": 0}