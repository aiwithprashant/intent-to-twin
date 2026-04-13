from pathlib import Path


class ResumeManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def stage_done(self, stage_name: str) -> bool:
        return (self.base_dir / stage_name / ".done").exists()

    def mark_stage_done(self, stage_name: str):
        (self.base_dir / stage_name).mkdir(parents=True, exist_ok=True)
        (self.base_dir / stage_name / ".done").touch()

    def get_last_iteration(self) -> int:
        iter_dirs = list(self.base_dir.glob("iter_*"))
        if not iter_dirs:
            return -1

        indices = [int(d.name.split("_")[1]) for d in iter_dirs]
        return max(indices)