from pathlib import Path
from utils.io import load_json, save_json


class SceneUpdater:
    def __init__(self, logger):
        self.logger = logger

    def update_scene_graph(self, original_scene_path, updated_state_path, output_path):
        self.logger.info("[M7] Updating scene graph for next iteration")

        scene = load_json(original_scene_path)
        updated_state = load_json(updated_state_path)

        updated_objects = {obj["id"]: obj for obj in updated_state["objects"]}

        # update objects
        for obj in scene["objects"]:
            obj_id = obj["id"]

            if obj_id in updated_objects:
                updated_obj = updated_objects[obj_id]

                # propagate position / attributes
                obj["attributes"] = obj.get("attributes", {})
                obj["attributes"]["position"] = updated_obj.get("position", [0, 0, 0])

        save_json(scene, output_path)

        self.logger.info(f"[M7] Scene graph updated: {output_path}")

        return output_path