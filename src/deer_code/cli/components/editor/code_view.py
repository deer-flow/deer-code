from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static

from deer_code.cli.theme import DEER_DARK_THEME


class CodeView(VerticalScroll):
    """Code view component with syntax highlighting"""

    DEFAULT_CSS = """
    CodeView {
        height: 1fr;
    }

    CodeView #code-content {
        padding: 1 1;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = "# Welcome to DeerCode\n# Code will be displayed here\n\ndef hello_world():\n    print('Hello, World!')"
        self.file_path = None

    def compose(self) -> ComposeResult:
        yield Static(id="code-content")

    def update_code(self, code: str, file_path: str = None) -> None:
        """Update code content and optionally the file path"""
        self.code = code
        self.file_path = file_path

        # Auto-detect language from file path or default to python
        if file_path:
            lexer = Syntax.guess_lexer(file_path, code)
        else:
            lexer = "text"

        # Create syntax highlighted content
        syntax = Syntax(
            code,
            lexer,
            theme="monokai",
            line_numbers=True,
            word_wrap=False,
            indent_guides=False,
            background_color=DEER_DARK_THEME.boost,
        )

        content_widget = self.query_one("#code-content", Static)
        content_widget.update(syntax)
