from pathlib import Path
from utils.io import load_json, save_json

from evaluation.metrics import (
    compute_error_reduction,
    compute_validity,
    compute_convergence,
    compute_constraint_satisfaction
)


class Evaluator:
    def __init__(self, base_output_dir, logger):
        self.base_dir = Path(base_output_dir)
        self.logger = logger

    def run(self):
        self.logger.info("[EVAL] Starting evaluation")

        iter_dirs = sorted(self.base_dir.glob("iter_*"))

        error_counts = []
        final_errors = []
        constraints = []
        num_objects = 0

        for d in iter_dirs:
            errors_path = d / "m5/errors.json"
            state_path = d / "m4/twin_state.json"

            if errors_path.exists():
                errors = load_json(errors_path)
                error_counts.append(len(errors))

            if state_path.exists():
                state = load_json(state_path)
                final_errors = errors
                constraints = state.get("constraints", [])
                num_objects = len(state.get("objects", []))

        metrics = {
            "error_reduction": compute_error_reduction(error_counts),
            "final_validity": compute_validity(final_errors, num_objects),
            "convergence_steps": compute_convergence(len(iter_dirs)),
            "constraint_satisfaction": compute_constraint_satisfaction(
                final_errors,
                constraints
            )
        }

        output_path = self.base_dir / "final" / "metrics.json"

        save_json(metrics, output_path, logger=self.logger)

        self.logger.info(f"[EVAL] Metrics computed: {metrics}")