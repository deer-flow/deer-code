from typing import Annotated

from langchain.messages import ToolMessage
from langchain.tools import InjectedToolCallId, tool
from langgraph.graph.state import Command

from .types import TodoItem


@tool("todo_write", parse_docstring=True)
def todo_write_tool(
    todos: list[TodoItem], tool_call_id: Annotated[str, InjectedToolCallId]
):
    """Update the entire TODO list with the latest items.

    Args:
        todos: A list of TodoItem objects.
    """
    # Do nothing, but save the latest to-dos to the state.
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(
                    f"Successfully updated the TODO list with {len(todos)} items.",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
