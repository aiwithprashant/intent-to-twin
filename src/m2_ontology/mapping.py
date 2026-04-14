IFC_ENTITY_MAP = {
    "wall": "IfcWall",
    "door": "IfcDoor",
    "window": "IfcWindow",
    "pipe": "IfcPipeSegment",
    "room": "IfcSpace",
    "floor": "IfcSlab"
}


def map_entities(objects):
    mapped = []

    for obj in objects:
        name = obj["name"].lower()

        if name in IFC_ENTITY_MAP:
            mapped.append({
                "id": obj["id"],
                "name": name,
                "ifc_class": IFC_ENTITY_MAP[name]
            })

    return mapped