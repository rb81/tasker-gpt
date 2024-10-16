from pydantic import BaseModel
from typing import Optional

class ObjectiveDetermination(BaseModel):
    determination: bool
    explanation: str

class ObjectiveRevision(BaseModel):
    revised_objective: str

class TaskList(BaseModel):
    task_list: list[str]

class TaskDetermination(BaseModel):
    approved: bool
    feedback: Optional[str] = None

class TaskExecution(BaseModel):
    instructions: Optional[str] = None
    output: Optional[str] = None
    completed: bool

class AssistantResponse(BaseModel):
    response: str