PROMPT_TEMPLATE = """
Convert the following text into a structured scene graph JSON.

Return ONLY valid JSON.

Schema:
{
  "objects": [
    {"id": "obj_0", "name": "", "attributes": {}}
  ],
  "relations": [
    {"subject": "", "predicate": "", "object": ""}
  ],
  "confidence": {
    "obj_0": 0.0
  }
}

Text:
"{input_text}"
"""