import torch
from diffusers import StableDiffusionPipeline
from pathlib import Path


class MultiViewGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16
        ).to("cuda")

    def generate(self, prompt, output_dir):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        views = ["front", "side", "top"]

        image_paths = []

        for i, view in enumerate(views):
            full_prompt = f"{prompt}, {view} view"

            image = self.pipe(full_prompt).images[0]

            path = Path(output_dir) / f"view_{i}.png"
            image.save(path)

            image_paths.append(str(path))

        return image_paths