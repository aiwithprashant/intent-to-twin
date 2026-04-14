from pathlib import Path
import shutil
from utils.io import load_json, save_json


class Finalizer:
    def __init__(self, base_output_dir, logger):
        self.base_dir = Path(base_output_dir)
        self.final_dir = self.base_dir / "final"
        self.logger = logger

    def run(self):
        self.final_dir.mkdir(parents=True, exist_ok=True)

        # detect last iteration
        iter_dirs = sorted(self.base_dir.glob("iter_*"))
        last_iter = iter_dirs[-1]

        self.logger.info(f"[FINAL] Using iteration: {last_iter.name}")

        # ---- Final Mesh ----
        mesh_src = last_iter / "m3/mesh/scene.ply"
        mesh_dst = self.final_dir / "final_twin.ply"

        shutil.copy(mesh_src, mesh_dst)

        # ---- Final TwinState ----
        state_src = last_iter / "m4/twin_state.json"
        state_dst = self.final_dir / "twin_state_final.json"

        shutil.copy(state_src, state_dst)

        # ---- Build evaluation report ----
        error_counts = []

        for d in iter_dirs:
            errors_file = d / "m5/errors.json"
            if errors_file.exists():
                errors = load_json(errors_file)
                error_counts.append(len(errors))

        report = {
            "iterations": len(iter_dirs),
            "error_reduction": error_counts,
            "final_status": "converged" if error_counts[-1] == 0 else "partial"
        }

        report_path = self.final_dir / "evaluation_report.json"
        save_json(report, report_path, logger=self.logger)

        self.logger.info("[FINAL] Final outputs generated")