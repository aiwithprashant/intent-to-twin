from pathlib import Path
from utils.io import load_json, save_json

from src.m4_state.schema import TwinState, TwinObject, TwinRelation
from src.m4_state.geometry import extract_geometry


class TwinStateBuilder:
    def __init__(self, output_dir, logger):
        self.output_dir = Path(output_dir) / "m4"
        self.logger = logger

    def run(self, scene_graph_path, constraints_path, mesh_path):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.output_dir / "twin_state.json"

        if output_file.exists():
            self.logger.info("[M4] Output exists, skipping")
            return

        self.logger.info("[M4] Loading inputs")

        scene_graph = load_json(scene_graph_path)
        constraints_data = load_json(constraints_path)

        objects = scene_graph["objects"]
        relations = scene_graph["relations"]

        mapped_entities = constraints_data["mapped_entities"]
        constraints = constraints_data["constraints"]

        self.logger.info("[M4] Building object states")

        object_map = {e["id"]: e["ifc_class"] for e in mapped_entities}

        twin_objects = []

        for obj in objects:
            twin_objects.append(
                TwinObject(
                    id=obj["id"],
                    name=obj["name"],
                    ifc_class=object_map.get(obj["id"], "Unknown")
                )
            )

        self.logger.info("[M4] Building relations")

        twin_relations = [
            TwinRelation(**rel) for rel in relations
        ]

        self.logger.info("[M4] Extracting geometry")

        geometry = extract_geometry(mesh_path)

        self.logger.info("[M4] Building confidence scores")

        confidence = scene_graph.get("confidence", {})

        state = TwinState(
            objects=twin_objects,
            relations=twin_relations,
            geometry=geometry,
            constraints=constraints,
            confidence=confidence
        )

        save_json(state.dict(), output_file, logger=self.logger)

        self.logger.info("[M4] TwinState created successfully")