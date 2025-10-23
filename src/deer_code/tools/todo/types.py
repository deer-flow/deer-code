from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class TodoStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class TodoPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoItem(BaseModel):
    """Representation of a TODO item."""

    id: int = Field(..., ge=0)
    title: str = Field(..., min_length=1)
    priority: TodoPriority = Field(default=TodoPriority.medium)
    status: TodoStatus = Field(default=TodoStatus.pending)
