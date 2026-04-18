def build_prompt(scene_graph, constraints):
    objects = []

    for obj in scene_graph["objects"]:
        desc = obj["name"]

        # include positional hint if exists
        pos = obj.get("attributes", {}).get("position")
        if pos:
            desc += f" at position {pos}"

        objects.append(desc)

    prompt = f"A realistic 3D scene with: {', '.join(objects)}."

    for c in constraints:
        if "door" in c.get("rule", ""):
            prompt += " A door embedded in a wall."

    return prompt