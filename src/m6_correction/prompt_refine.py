def refine_prompt(original_prompt, errors):
    refined = original_prompt

    for e in errors:
        if e["type"] == "containment":
            refined += " Ensure objects are properly contained within structures."

    return refined