from .prompts import Prompts
from .llm_openai import LLMOpenAI
import json
from .response_formats import ObjectiveDetermination, ObjectiveRevision

import logging
logger = logging.getLogger(__name__)

class Objective:
    def __init__(self, objective):
        self.prompts = Prompts()
        self.llm = LLMOpenAI()
        self.objective = objective

    def set_initial_context(self):
        # Set the initial context for the objective review
        return [
            {"role": "system", "content": self.prompts.load("objective_review")},
            {"role": "user", "content": self.objective},
        ]
    
    def set_revision_context(self, explanation):
        # Set the context for revising the objective based on the provided explanation
        return [
            {"role": "system", "content": self.prompts.load("objective_revision")},
            {"role": "user", "content": "# Objective\n\n" + self.objective + "\n\n# Steps to Revise\n\n" + explanation},
        ]

    def set_objective(self):
        logger.info("Reviewing Objective")
        # Determine if the objective is valid or needs revision
        messages = self.set_initial_context()  # Get the initial context
        result = json.loads(self.llm.call(messages, ObjectiveDetermination))  # Call the LLM API
        logger.debug(result)

        if result["determination"] is True:
            logger.info("Objective Approved")
            # If the objective is valid, return it
            return self.objective
        else:
            logger.info("Revising Objective")
            # If the objective needs revision, set the revision context and call the LLM API again
            messages = self.set_revision_context(result["explanation"])
            result = json.loads(self.llm.call(messages, ObjectiveRevision))
            logger.debug(result)
            
            return result["revised_objective"]