import json
from openai import OpenAI

client = OpenAI()


SYSTEM_PROMPT = """
You are a structured scene parser.

Convert user input into JSON with:
- objects (with id, name, attributes)
- relations (subject, predicate, object)
- confidence scores

Return STRICT JSON only.
"""


def parse_with_llm(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")