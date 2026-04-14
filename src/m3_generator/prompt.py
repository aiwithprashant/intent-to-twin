def build_prompt(scene_graph, constraints):
    objects = [obj["name"] for obj in scene_graph["objects"]]

    prompt = f"A realistic 3D scene with: {', '.join(objects)}."

    # Add constraint hints
    for c in constraints:
        if "door" in c.get("rule", ""):
            prompt += " A door embedded in a wall."

    return prompt