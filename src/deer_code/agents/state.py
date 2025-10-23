from langgraph.graph import MessagesState
from pydantic import Field

from deer_code.tools.todo.types import TodoItem


class CodingAgentState(MessagesState):
    todos: list[TodoItem] = Field(default_factory=list)
