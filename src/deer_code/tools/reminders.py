from langchain.tools import ToolRuntime

from deer_code.tools.todo.types import TodoStatus


def generate_reminders(runtime: ToolRuntime):
    todos = runtime.state.get("todos")
    unfinished_todos = []
    if todos is not None:
        for todo in todos:
            if (
                todo.status != TodoStatus.completed
                and todo.status != TodoStatus.cancelled
            ):
                unfinished_todos.append(todo)

    reminders = []
    if len(unfinished_todos) > 0:
        reminders.append(
            f"- {len(unfinished_todos)} todo{'' if len(unfinished_todos) == 1 else 's'} are not completed. Before you present the final result to the user, **make sure** all the todos are completed."
        )
        reminders.append(
            "- Immediately update the TODO list using the `todo_write` tool."
        )
    return "\n\nIMPORTANT:\n" + "\n".join(reminders) if len(reminders) > 0 else ""
