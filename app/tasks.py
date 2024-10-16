import json
from .prompts import Prompts
from .llm_openai import LLMOpenAI
from .response_formats import TaskList, TaskDetermination

import logging
logger = logging.getLogger(__name__)

class Tasks:
    def __init__(self, final_objective):
        # Initialize the Tasks class with the given final objective
        self.final_objective = final_objective
        self.llm = LLMOpenAI()  # Initialize the LLMOpenAI class
        self.prompts = Prompts()  # Load prompts

    def set_initial_context(self):
        # Set the initial context for generating the task list
        return [
            {"role": "system", "content": self.prompts.load("task_list")},
            {"role": "user", "content": self.final_objective},
        ]
    
    def set_revision_context(self, tasks):
        # Set the context for reviewing and revising the task list
        return [
            {"role": "system", "content": self.prompts.load("task_review_system_prompt")},
            {"role": "user", "content": self.prompts.load("task_review_decision")},
            {"role": "user", "content": f"Objective: {self.final_objective}\n\nInitial tasks:\n" + "\n".join(f"- {task}" for task in tasks)},
        ]
    
    def review_tasks(self, tasks):
        logger.info("Reviewing Tasks")
        # Review the generated tasks and revise if necessary
        context = self.set_revision_context(tasks)
        while True:
            # Call the OpenAI API and get the result
            result = json.loads(self.llm.call(context, TaskDetermination))
            logger.debug(result)
            
            # Append the API's response to the context
            context.append({
                "role": "assistant",
                "content": json.dumps(result)
            })

            if result["approved"]:
                logger.info("Tasks Approved")
                # If the tasks are approved, return them
                return tasks
            else:
                logger.info("Revising Tasks")
                # If the tasks need revision, append revision request to context
                context.append({
                    "role": "user",
                    "content": self.prompts.load("task_revision")
                })

                # Call the OpenAI API to get revised tasks
                revised_tasks = json.loads(self.llm.call(context, TaskList))
                tasks = revised_tasks["task_list"]
                logger.debug(revised_tasks)
                
                # Append the revised tasks to the context
                context.append({
                    "role": "assistant",
                    "content": f"Revised tasks:\n" + "\n".join(f"- {task}" for task in tasks)
                })

    def generate_tasks(self):
        logger.info("Generating Tasks")
        
        # Generate the initial task list and review it
        messages = self.set_initial_context()
        result = json.loads(self.llm.call(messages, TaskList))
        logger.debug(result)
        
        return self.review_tasks(result["task_list"])