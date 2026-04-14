import argparse
import torch
from pathlib import Path

from utils.config import Config
from utils.logger import setup_logger
from pipeline.resume_manager import ResumeManager
from pipeline.stage_runner import StageRunner

from src.m1_parser.parser import IntentParser
from src.m2_ontology.engine import OntologyEngine
from src.m3_generator.engine import GenerationEngine
from src.m4_state.builder import TwinStateBuilder
from src.m5_feedback.engine import FeedbackEngine
from src.m6_correction.engine import CorrectionEngine
from src.m7_controller.controller import LoopController
from evaluation.evaluator import Evaluator

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

    # ---------------- M1 ----------------
    logger.info("===== M1: Intent Parsing =====")

    parser_module = IntentParser(
        config=config,
        output_dir=outputs_path,
        logger=logger
    )

    input_text = "a room with a door, window and pipe"

    runner.run_stage("m1", lambda: parser_module.run(input_text))

    scene_graph_path = f"{outputs_path}/m1/scene_graph.json"

    # ---------------- M2 ----------------
    logger.info("===== M2: Ontology Engine =====")

    m2 = OntologyEngine(
        output_dir=outputs_path,
        logger=logger
    )

    runner.run_stage("m2", lambda: m2.run(scene_graph_path))

    constraints_path = f"{outputs_path}/m2/knowledge_constraints.json"

    # ---------------- INIT M3–M6 ----------------
    logger.info("===== Initializing M3–M6 Engines =====")

    m3 = GenerationEngine(
        output_dir=outputs_path,
        logger=logger
    )

    m4 = TwinStateBuilder(
        output_dir=outputs_path,
        logger=logger
    )

    m5 = FeedbackEngine(
        output_dir=outputs_path,
        logger=logger
    )

    m6 = CorrectionEngine(
        output_dir=outputs_path,
        logger=logger
    )

    # ---------------- M7 LOOP ----------------
    logger.info("===== M7: Iterative Loop =====")

    controller = LoopController(
        config=config,
        base_output_dir=outputs_path,
        logger=logger
    )

    controller.run(
        scene_graph_path=scene_graph_path,
        constraints_path=constraints_path,
        generation_engine=m3,
        state_builder=m4,
        feedback_engine=m5,
        correction_engine=m6
    )

    logger.info("===== PIPELINE FINISHED =====")
    
    evaluator = Evaluator(outputs_path, logger)
    evaluator.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)

    args = parser.parse_args()
    main(args.config)