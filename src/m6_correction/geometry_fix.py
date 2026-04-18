def fix_floating_object(obj):
    obj["position"][2] = 0.0  # snap to ground
    return obj


def apply_geometry_fixes(objects, errors):
    updated_objects = []

    error_map = {e["object"]: e for e in errors}

    for obj in objects:
        obj_id = obj["id"]

        if obj_id in error_map:
            error = error_map[obj_id]

            if error["type"] == "floating":
                obj = fix_floating_object(obj)

        updated_objects.append(obj)

    return updated_objects