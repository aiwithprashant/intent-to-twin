class StageRunner:
    def __init__(self, config, resume_manager, logger):
        self.config = config
        self.resume = resume_manager
        self.logger = logger

    def run_stage(self, name, func):
        if self.resume.stage_done(name):
            self.logger.info(f"[SKIP] {name} already completed")
            return

        self.logger.info(f"[RUN] {name}")
        func()

        self.resume.mark_stage_done(name)
        self.logger.info(f"[DONE] {name}")