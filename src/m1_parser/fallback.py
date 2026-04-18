import spacy

nlp = spacy.load("en_core_web_sm")


def fallback_parse(text: str):
    doc = nlp(text)

    objects = []
    relations = []

    nouns = [token.text for token in doc if token.pos_ == "NOUN"]

    for i, noun in enumerate(nouns):
        objects.append({
            "id": f"obj_{i}",
            "name": noun,
            "attributes": {}
        })

    # naive relation (extend later)
    if len(nouns) >= 2:
        relations.append({
            "subject": "obj_0",
            "predicate": "related_to",
            "object": "obj_1"
        })

    return {
        "objects": objects,
        "relations": relations,
        "confidence": {obj["id"]: 0.5 for obj in objects}
    }