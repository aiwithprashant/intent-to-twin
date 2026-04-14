from pathlib import Path
from utils.io import load_json, save_json

from src.m2_ontology.mapping import map_entities
from src.m2_ontology.constraints import extract_constraints
from src.m2_ontology.priors import extract_priors


class OntologyEngine:
    def __init__(self, output_dir, logger):
        self.output_dir = Path(output_dir) / "m2"
        self.logger = logger

    def run(self, input_path):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.output_dir / "knowledge_constraints.json"

        if output_file.exists():
            self.logger.info("[M2] Output exists, skipping")
            return

        self.logger.info(f"[M2] Loading scene graph from: {input_path}")

        scene_graph = load_json(input_path)

        objects = scene_graph["objects"]

        self.logger.info("[M2] Mapping entities to IFC")

        mapped = map_entities(objects)

        self.logger.debug(f"[M2] Mapped entities: {mapped}")

        self.logger.info("[M2] Extracting constraints")

        constraints = extract_constraints(mapped)

        self.logger.info("[M2] Extracting priors")

        priors = extract_priors(mapped)

        output = {
            "mapped_entities": mapped,
            "constraints": constraints,
            "priors": priors,
            "relations": scene_graph.get("relations", [])
        }

        save_json(output, output_file, logger=self.logger)

        self.logger.info("[M2] Knowledge constraints generated")