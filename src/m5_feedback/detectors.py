def detect_floating_objects(objects):
    errors = []

    for obj in objects:
        z = obj.get("position", [0, 0, 0])[2]

        if z > 0.5:  # threshold
            errors.append({
                "type": "floating",
                "object": obj["id"],
                "severity": "high",
                "message": "Object is not grounded"
            })

    return errors

def detect_invalid_containment(objects, constraints):
    errors = []

    obj_map = {o["id"]: o for o in objects}

    for c in constraints:
        if c["type"] == "containment":
            target = c["target"]
            required_parent = c["required_parent"]

            # naive check (extend later)
            if target in obj_map:
                parent_found = any(
                    o["ifc_class"] == required_parent
                    for o in objects
                )

                if not parent_found:
                    errors.append({
                        "type": "containment",
                        "object": target,
                        "severity": "high",
                        "message": f"{target} not inside {required_parent}"
                    })

    return errors

def detect_missing_relations(relations, constraints):
    errors = []

    existing = {(r["subject"], r["predicate"], r["object"]) for r in relations}

    for c in constraints:
        if "required_parent" in c:
            found = any(
                c["target"] == r[0] for r in existing
            )

            if not found:
                errors.append({
                    "type": "relation",
                    "object": c["target"],
                    "severity": "medium",
                    "message": "Missing required relation"
                })

    return errors