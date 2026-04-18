def extract_constraints(mapped_entities):
    constraints = []

    classes = {e["id"]: e["ifc_class"] for e in mapped_entities}

    for obj_id, cls in classes.items():

        if cls == "IfcDoor":
            constraints.append({
                "type": "containment",
                "rule": "door must be inside wall",
                "target": obj_id,
                "required_parent": "IfcWall"
            })

        if cls == "IfcWindow":
            constraints.append({
                "type": "containment",
                "rule": "window must be inside wall",
                "target": obj_id,
                "required_parent": "IfcWall"
            })

        if cls == "IfcPipeSegment":
            constraints.append({
                "type": "connectivity",
                "rule": "pipe must connect to structure",
                "target": obj_id
            })

    return constraints