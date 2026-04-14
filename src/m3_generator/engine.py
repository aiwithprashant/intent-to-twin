from pathlib import Path
from utils.io import load_json, save_json

from src.m3_generator.prompt import build_prompt
from src.m3_generator.diffusion import MultiViewGenerator
from src.m3_generator.reconstruction import ReconstructionEngine


class GenerationEngine:
    def __init__(self, output_dir, logger):
        self.output_dir = Path(output_dir) / "m3"
        self.logger = logger

        self.generator = MultiViewGenerator()
        self.reconstructor = ReconstructionEngine()

    def run(self, scene_graph_path, constraints_path):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        image_dir = self.output_dir / "images"
        mesh_path = self.output_dir / "mesh" / "scene.ply"

        if mesh_path.exists():
            self.logger.info("[M3] Output exists, skipping")
            return

        self.logger.info("[M3] Loading inputs")

        scene_graph = load_json(scene_graph_path)
        constraints = load_json(constraints_path)["constraints"]

        self.logger.info("[M3] Building prompt")

        prompt = build_prompt(scene_graph, constraints)

        self.logger.info(f"[M3] Prompt: {prompt}")

        self.logger.info("[M3] Generating multi-view images")

        image_paths = self.generator.generate(prompt, image_dir)

        self.logger.info(f"[M3] Generated images: {image_paths}")

        self.logger.info("[M3] Reconstructing 3D mesh")

        mesh = self.reconstructor.reconstruct(image_paths, mesh_path)

        self.logger.info(f"[M3] Mesh saved: {mesh}")