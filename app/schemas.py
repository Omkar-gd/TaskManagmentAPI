from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date, datetime

# Schema for creating a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["Low", "Medium", "High"] = "Medium"
    status: Literal["Pending", "In Progress", "Completed"] = "Pending"
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["Low", "Medium", "High"]] = None
    status: Optional[Literal["Pending", "In Progress", "Completed"]] = None
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None

# Schema for returning a task
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    assigned_to: Optional[str]
    due_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}


def sumTwo(a:int,b:int):
    return a+b

print(sumTwo(10,2))
