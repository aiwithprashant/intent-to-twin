def extract_priors(mapped_entities):
    priors = []

    for entity in mapped_entities:
        cls = entity["ifc_class"]

        if cls == "IfcDoor":
            priors.append({
                "target": entity["id"],
                "height_range": [2.0, 2.2],
                "width_range": [0.8, 1.2]
            })

        if cls == "IfcWall":
            priors.append({
                "target": entity["id"],
                "thickness_range": [0.1, 0.3]
            })

    return priors