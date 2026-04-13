class StageRunner:
    def __init__(self, config, resume_manager, logger):
        self.config = config
        self.resume = resume_manager
        self.logger = logger

    def run_stage(self, name, func):
        self.logger.info(f"========== STAGE: {name} ==========")

        if self.resume.stage_done(name):
            self.logger.info(f"[SKIP] {name} already completed")
            return

        try:
            self.logger.info(f"[START] {name}")
            func()
            self.resume.mark_stage_done(name)
            self.logger.info(f"[DONE] {name}")

        except Exception as e:
            self.logger.error(f"[FAIL] {name}: {e}")
            raise