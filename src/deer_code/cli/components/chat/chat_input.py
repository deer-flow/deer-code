from textual.widgets import Input


class ChatInput(Input):
    """Custom input for chat with no border"""

    DEFAULT_CSS = """
    ChatInput {
        dock: bottom;
        margin: 1 2;
        padding: 1 2;
        background: $panel;
        border: none;
        width: 100%;
        height: auto;
    }

    ChatInput:focus {
        border: none;
        background: $panel;
    }

    ChatInput > .input--placeholder {
        color: $text-muted;
        text-style: dim;
    }
    """
