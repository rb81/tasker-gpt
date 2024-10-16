import json
from .prompts import Prompts
from .llm_openai import LLMOpenAI
from .response_formats import TaskExecution, AssistantResponse

import logging
logger = logging.getLogger(__name__)

class ExecuteTasks:
    def __init__(self, objective, tasks, max_loops=10):
        self.objective = objective
        self.tasks = tasks
        self.prompts = Prompts()
        self.max_loops = max_loops
        self.llm = LLMOpenAI()

    def set_initial_context(self):
        return [
            {"role": "system", "content": self.prompts.load("execute_task_instructions")},
            {"role": "system", "content": f"### Objective:\n\n{self.objective}\n\n### Related Tasks:\n\n{json.dumps(self.tasks, indent=2)}"},
        ]

    def execute(self):

        results = []
        final = []

        for task in self.tasks:
            messages = self.set_initial_context()
            messages.append({"role": "user", "content": f"### Current Task to Execute:\n\n{task}"})
            
            logger.info(f"Executing task: {task}")
            
            loop_count = 0
            while loop_count < self.max_loops:
                # Check if this is the last iteration
                if loop_count == self.max_loops - 2:
                    logger.debug("Max Loops Almost Reached, Warning LLM to Complete Task")
                    messages.append({"role": "system", "content": "This is the last message in the exchange. Please use the information you have to complete the task."})

                response = self.llm.call(messages, TaskExecution)
                response_data = json.loads(response)
                if response_data.get("completed"):
                    logger.info("Task Execution Complete, Moving to Next Task")
                    results.append({"task": task, "output": response_data.get("output")})
                    logger.debug(response_data)
                    break
                
                support_messages = [
                    {"role": "system", "content": self.prompts.load("support_instructions")},
                    {"role": "user", "content": response_data.get("instructions")}
                ]

                logger.info("Requesting Additional Support for Task")
                support_response = self.llm.call(support_messages, AssistantResponse)
                support_response_data = json.loads(support_response)
                logger.info("Support Response Received")
                logger.debug(support_response_data)
                messages.append({"role": "assistant", "content": support_response_data.get("response")})

                loop_count += 1

            if loop_count == self.max_loops:
                logger.warning(f"Warning: Max loops ({self.max_loops}) reached for task: {task}")

        final.append({"role": "system", "content": self.prompts.load("final_execution")})
        final.append({"role": "user", "content": f"### Objective:\n\n{self.objective}\n\n### Tasks:\n\n{json.dumps(self.tasks, indent=2)}\n\n### Results:\n\n{json.dumps(results, indent=2)}"})
        final_response = self.llm.call(final, AssistantResponse)
        final_result = json.loads(final_response).get("response")

        logger.info("Final Execution Complete")
        logger.debug(final_result)
    
        return final_result
