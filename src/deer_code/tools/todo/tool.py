from langchain.agents import tool

from .types import TodoItem


@tool("todo_write", parse_docstring=True)
def todo_write_tool(items: list[TodoItem]):
    """Update the entire TODO list with the latest items.

    Args:
        items: A list of TodoItem objects.
    """
    return f"Successfully updated the TODO list with {len(items)} items."
