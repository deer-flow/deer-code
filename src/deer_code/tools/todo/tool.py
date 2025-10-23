from typing import Annotated

from langchain.messages import ToolMessage
from langchain.tools import InjectedToolCallId, tool
from langgraph.graph.state import Command

from .types import TodoItem, TodoStatus


@tool("todo_write", parse_docstring=True)
def todo_write_tool(
    todos: list[TodoItem], tool_call_id: Annotated[str, InjectedToolCallId]
):
    """Update the entire TODO list with the latest items.

    Args:
        todos: A list of TodoItem objects.
    """
    # Do nothing, but save the latest to-dos to the state.

    unfinished_todos = []
    for todo in todos:
        if todo.status != TodoStatus.completed and todo.status != TodoStatus.cancelled:
            unfinished_todos.append(todo)

    message = f"Successfully updated the TODO list with {len(todos)} items."
    if len(unfinished_todos) > 0:
        message += f" {len(unfinished_todos)} todo{' is' if len(unfinished_todos) == 1 else 's are'} not completed."
    else:
        message += " All todos are completed."

    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(
                    message,
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
