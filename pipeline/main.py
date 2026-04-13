import argparse
import torch

from utils.config import Config
from utils.logger import setup_logger
from pipeline.resume_manager import ResumeManager
from pipeline.stage_runner import StageRunner
from src.m1_parser.parser import IntentParser


def set_seed(seed):
    torch.manual_seed(seed)


def main(config_path):
    config = Config(config_path)

    logger = setup_logger(config.get("paths.logs"))
    resume = ResumeManager(config.get("paths.outputs"))
    runner = StageRunner(config, resume, logger)

    set_seed(config.get("experiment.seed"))

    # Placeholder stages (we will replace with real modules)
    parser_module = IntentParser(
        config=config,
        output_dir=config.get("paths.outputs"),
        logger=logger
    )

    runner.run_stage("m1", lambda: parser_module.run(input_text))
    runner.run_stage("m2", lambda: print("Running M2"))
    runner.run_stage("m3", lambda: print("Running M3"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)

    args = parser.parse_args()
    main(args.config)