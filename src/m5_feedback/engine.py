from pathlib import Path
from utils.io import load_json, save_json

from src.m5_feedback.detectors import (
    detect_floating_objects,
    detect_invalid_containment,
    detect_missing_relations
)


class FeedbackEngine:
    def __init__(self, output_dir, logger):
        self.output_dir = Path(output_dir) / "m5"
        self.logger = logger

    def run(self, twin_state_path):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.output_dir / "errors.json"

        if output_file.exists():
            self.logger.info("[M5] Output exists, skipping")
            return

        self.logger.info("[M5] Loading TwinState")

        state = load_json(twin_state_path)

        objects = state["objects"]
        relations = state["relations"]
        constraints = state["constraints"]

        self.logger.info("[M5] Running error detection")

        errors = []
        errors += detect_floating_objects(objects)
        errors += detect_invalid_containment(objects, constraints)
        errors += detect_missing_relations(relations, constraints)

        self.logger.info(f"[M5] Total errors detected: {len(errors)}")

        save_json(errors, output_file, logger=self.logger)

        self.logger.info("[M5] Error report generated")