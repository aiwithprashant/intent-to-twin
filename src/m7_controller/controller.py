from pathlib import Path
from utils.io import load_json

from src.m7_controller.finalizer import Finalizer
from src.m7_controller.updater import SceneUpdater


class LoopController:
    def __init__(self, config, base_output_dir, logger):
        self.max_iter = config.get("experiment.max_iterations")
        self.base_dir = Path(base_output_dir)
        self.logger = logger

    def should_stop(self, errors, iteration):
        if len(errors) == 0:
            self.logger.info("[M7] No errors → stopping")
            return True

        if iteration >= self.max_iter:
            self.logger.info("[M7] Max iterations reached → stopping")
            return True

        return False

    def run(
        self,
        scene_graph_path,
        constraints_path,
        generation_engine,
        state_builder,
        feedback_engine,
        correction_engine
    ):
        self.logger.info("[M7] Starting iterative loop")

        updater = SceneUpdater(self.logger)

        current_scene_graph = scene_graph_path

        for i in range(self.max_iter):

            self.logger.info(f"[M7] Iteration {i}")

            iter_dir = self.base_dir / f"iter_{i}"
            iter_dir.mkdir(parents=True, exist_ok=True)

            # ---- dynamic paths ----
            generation_engine.output_dir = iter_dir / "m3"
            state_builder.output_dir = iter_dir / "m4"
            feedback_engine.output_dir = iter_dir / "m5"
            correction_engine.output_dir = iter_dir / "m6"

            # ---- M3 ----
            mesh_path = str(iter_dir / "m3/mesh/scene.ply")

            generation_engine.run(current_scene_graph, constraints_path)

            # ---- M4 ----
            state_builder.run(
                current_scene_graph,
                constraints_path,
                mesh_path
            )

            twin_state_path = str(iter_dir / "m4/twin_state.json")

            # ---- M5 ----
            feedback_engine.run(twin_state_path)

            errors_path = str(iter_dir / "m5/errors.json")
            errors = load_json(errors_path)

            # ---- STOP CHECK ----
            if self.should_stop(errors, i):
                self.logger.info(f"[M7] Converged at iteration {i}")
                break

            # ---- M6 ----
            correction_engine.run(twin_state_path, errors_path)

            updated_state_path = str(iter_dir / "m6/updated_state.json")

            # ---- UPDATE SCENE GRAPH (ADAPTIVE LOOP) ----
            next_scene_graph_path = str(iter_dir / "scene_graph_updated.json")

            current_scene_graph = updater.update_scene_graph(
                current_scene_graph,
                updated_state_path,
                next_scene_graph_path
            )

        # ---- FINALIZATION ----
        finalizer = Finalizer(self.base_dir, self.logger)
        finalizer.run()