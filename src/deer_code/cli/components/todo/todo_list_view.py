from textual.widgets import Static


class TodoListView(Static):
    """Todo list view component"""

    DEFAULT_CSS = """
    TodoListView {
        color: $text-muted;
        padding: 1 2;
    }
    """

    def on_mount(self) -> None:
        self.update("(No TODO found)")

    def update_items(self, items: list[dict]):
        content = ""
        for item in items:
            status = "\\[x]" if item["status"] == "completed" else "\\[ ]"
            content += f"{status} {item["content"]}\n"
        self.update(content)
