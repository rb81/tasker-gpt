import os

import logging
logger = logging.getLogger(__name__)

class Prompts:
    def __init__(self):
        self.prompt_files = {
            "objective_review": "app/prompts/objective_review.md",
            "objective_revision": "app/prompts/objective_revision.md",
            "task_review_decision": "app/prompts/task_review_decision.md",
            "task_list": "app/prompts/task_list.md",
            "determination": "app/prompts/determination.md",
            "task_review_system_prompt": "app/prompts/task_review_system_prompt.md",
            "task_revision": "app/prompts/task_revision.md",
            "final_execution": "app/prompts/final_execution.md",
            "execute_task_instructions": "app/prompts/execute_task_instructions.md",
            "support_instructions": "app/prompts/support_instructions.md",
        }

    def load(self, prompt_name):
        file_path = self.prompt_files.get(prompt_name)
        if not file_path:
            logger.warning(f"Prompt name '{prompt_name}' not found.")
            return ""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        logger.warning(f"Prompt file '{file_path}' does not exist.")
        return ""