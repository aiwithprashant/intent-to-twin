from pathlib import Path

from utils.io import save_json
from src.m1_parser.fallback import fallback_parse
from src.m1_parser.schema import SceneGraph
from src.m1_parser.llm_provider import HuggingFaceLLM, OpenAILLM
from src.m1_parser.prompt import PROMPT_TEMPLATE


class IntentParser:
    def __init__(self, config, output_dir, logger):
        self.output_dir = Path(output_dir) / "m1"
        self.logger = logger

        provider = config.get("m1.llm_provider")

        if provider == "huggingface":
            self.llm = HuggingFaceLLM(
                model_name=config.get("huggingface.model"),
                max_tokens=config.get("huggingface.max_new_tokens")
            )
        elif provider == "openai":
            self.llm = OpenAILLM(
                model_name=config.get("openai.model")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def run(self, text: str):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_file = self.output_dir / "scene_graph.json"

        if output_file.exists():
            self.logger.info("M1 output exists, skipping")
            return

        prompt = PROMPT_TEMPLATE.format(input_text=text)

        try:
            self.logger.info("Running LLM parser")
            result = self.llm.generate(prompt)

        except Exception as e:
            self.logger.warning(f"LLM failed: {e}, using fallback")
            result = fallback_parse(text)

        graph = SceneGraph(**result)

        save_json(graph.dict(), output_file)

        self.logger.info(f"Scene graph saved: {output_file}")