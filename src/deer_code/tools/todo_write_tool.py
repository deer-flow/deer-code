from langchain.agents import tool

from deer_code.todo.types import TodoItem, TodoStatus


@tool("todo_write", parse_docstring=True)
def todo_write_tool(items: list[TodoItem]):
    """Update the entire TODO list with the latest items.

    Args:
        items: A list of TodoItem objects.
    """
    with open("TODO.md", "w") as f:
        content = "\n".join(
            [
                f"[{'x' if item.status == TodoStatus.completed else ' '}] {item.content}"
                for item in items
            ]
        )
        f.write(f"# TODOs\n\n{content}\n")
    return f"Successfully updated the TODO list with {len(items)} items."
