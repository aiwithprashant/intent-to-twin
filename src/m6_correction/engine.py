from pathlib import Path
from utils.io import load_json, save_json

from src.m6_correction.geometry_fix import apply_geometry_fixes
from src.m6_correction.prompt_refine import refine_prompt


class CorrectionEngine:
    def __init__(self, output_dir, logger):
        self.output_dir = Path(output_dir) / "m6"
        self.logger = logger

    def run(self, twin_state_path, errors_path):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = self.output_dir / "updated_state.json"

        if output_file.exists():
            self.logger.info("[M6] Output exists, skipping")
            return

        self.logger.info("[M6] Loading inputs")

        state = load_json(twin_state_path)
        errors = load_json(errors_path)

        objects = state["objects"]

        self.logger.info("[M6] Applying geometry corrections")

        updated_objects = apply_geometry_fixes(objects, errors)

        self.logger.info("[M6] Updating state")

        updated_state = state.copy()
        updated_state["objects"] = updated_objects
        updated_state["applied_fixes"] = errors

        save_json(updated_state, output_file, logger=self.logger)

        self.logger.info("[M6] Correction applied successfully")