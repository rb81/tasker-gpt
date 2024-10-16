from .objective import Objective
from .tasks import Tasks
from .execute_tasks import ExecuteTasks

import logging
logger = logging.getLogger(__name__)

def process_objective(objective, logger):
    logger.info(f"Processing objective: {objective}")
    
    # Review and set the objective
    final_objective = Objective(objective).set_objective()
    logger.info(f"Final objective: {final_objective}")

    # Generate tasks
    tasks = Tasks(final_objective).generate_tasks()
    logger.info(f"Generated tasks: {tasks}")

    # Execute tasks
    execute_tasks = ExecuteTasks(final_objective, tasks)
    result = execute_tasks.execute()

    logger.info("Process Complete")
    logger.info(f"Result: {result}")

    return result
