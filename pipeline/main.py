import argparse
import torch
from pathlib import Path

from utils.config import Config
from utils.logger import setup_logger
from pipeline.resume_manager import ResumeManager
from pipeline.stage_runner import StageRunner

from src.m1_parser.parser import IntentParser


def set_seed(seed):
    torch.manual_seed(seed)


def main(config_path):
    print(">>> ENTERED MAIN <<<")

    config = Config(config_path)

    root_path = config.get("paths.root")

    outputs_path = str(Path(root_path) / config.get("paths.outputs"))
    logs_path = str(Path(root_path) / config.get("paths.logs"))

    logger = setup_logger(logs_path)
    resume = ResumeManager(outputs_path)
    runner = StageRunner(config, resume, logger)

    set_seed(config.get("experiment.seed"))

    print(">>> INITIALIZING M1 <<<")

    parser_module = IntentParser(
        config=config,
        output_dir=outputs_path,
        logger=logger
    )

    input_text = "a room with a door, window and pipe"

    print(">>> ABOUT TO RUN M1 <<<")

    runner.run_stage("m1", lambda: parser_module.run(input_text))

    print(">>> PIPELINE FINISHED <<<")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)

    args = parser.parse_args()
    main(args.config)