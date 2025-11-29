from typing import List, Optional
from pydantic import BaseModel, Field

class SubTask(BaseModel):
    id: str = Field(..., description="Unique identifier for the subtask")
    description: str = Field(..., description="Clear instruction of what needs to be done")
    agent: str = Field(..., description="The agent responsible for this task (Data, Insight, Creative)")
    dependencies: List[str] = Field(default_factory=list, description="IDs of tasks that must be completed first")

class Plan(BaseModel):
    goal: str = Field(..., description="The overall objective of the plan")
    tasks: List[SubTask] = Field(..., description="List of subtasks to achieve the goal")
    reasoning: str = Field(..., description="Explanation of why this plan was chosen")
