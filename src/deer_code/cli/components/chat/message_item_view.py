import json

from langchain.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    ToolCall,
    ToolMessage,
)
from textual.app import ComposeResult
from textual.widgets import Markdown, Static


class MessageItemView(Static):
    """Single message item in the chat"""

    DEFAULT_CSS = """
    MessageItemView {
        width: 100%;
        height: auto;
        padding: 1;
        content-align: left top;
    }

    MessageItemView .message-header {
        color: $text-muted;
        text-style: dim;
        width: 100%;
    }

    MessageItemView.tool_calls_only {
        padding: 0 1;
    }

    MessageItemView .tool_call {
        color: $text-muted;
        text-style: dim;
        width: 100%;
    }

    MessageItemView .margin_top_1.tool_call {
        margin-top: 1;
    }

    MessageItemView #markdown {
        padding: 0 1 0 3;
        margin: 0;
    }
    """

    def __init__(self, message: AnyMessage, display_header: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.add_class(message.type)
        self.display_header = display_header

    def compose(self) -> ComposeResult:
        """Compose the message item"""
        if self.display_header:
            header = None
            if isinstance(self.message, HumanMessage):
                header = "[bold cyan]👤 You[/bold cyan]"
            elif isinstance(self.message, AIMessage):
                header = "[bold green]🦌 DeerCode[/bold green]"
            if header:
                yield Static(header, classes="message-header")
        text_content = self.message.content.strip() if self.message.content else ""
        final_action = (
            isinstance(self.message, AIMessage)
            and text_content != ""
            and (not self.message.tool_calls or len(self.message.tool_calls) == 0)
        )
        if (
            not isinstance(self.message, ToolMessage)
            and text_content is not None
            and text_content != ""
        ):
            yield Markdown(
                text_content,
                id="markdown",
                classes=f"message-content{' final' if final_action else ''}",
            )
        if isinstance(self.message, AIMessage):
            if self.message.tool_calls:
                if text_content == "" and not self.display_header:
                    self.add_class("tool_calls_only")
                for tool_call in self.message.tool_calls:
                    margin_top = 0
                    if text_content and tool_call == self.message.tool_calls[0]:
                        margin_top = 1
                    yield Static(
                        self.render_tool_call(tool_call),
                        classes=f"tool_call margin_top_{margin_top}",
                    )

    def render_tool_call(self, tool_call: ToolCall) -> str:
        name = tool_call["name"]
        if name == "bash":
            return "💻 Execute command: " + tool_call["args"]["command"]
        elif name == "tree":
            return "🔍 Explore project structure: " + (
                tool_call["args"]["path"]
                if tool_call["args"].get("path")
                else "."
                + (
                    " --max-depth=" + tool_call["args"]["max_depth"]
                    if tool_call["args"].get("max_depth")
                    else ""
                )
            )
        elif name == "grep":
            return (
                "🔍 Search files: "
                + tool_call["args"]["pattern"]
                + " in "
                + (tool_call["args"]["path"] if tool_call["args"].get("path") else ".")
            )
        elif name == "ls":
            return (
                "🗂️ List files: "
                + tool_call["args"]["path"]
                + " with "
                + tool_call["args"]["match"]
            )
        elif name == "text_editor":
            command = tool_call["args"]["command"]
            if command == "view":
                return "👁️  View file: " + tool_call["args"]["path"]
            elif command == "create":
                return "✏️  Create file: " + tool_call["args"]["path"]
            elif command == "str_replace":
                return "✏️  Replace text in file: " + tool_call["args"]["path"]
            elif command == "insert":
                return "✏️  Insert text into file: " + tool_call["args"]["path"]
            else:
                return "Unknown command: " + command
        elif name == "todo_write":
            return "📌 Update to-do list"
        return f"🛠️  Use MCP tool: {name}({json.dumps(tool_call['args'])})"
