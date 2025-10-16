from langchain.schema import AIMessage, BaseMessage
from langchain.schema.messages import ToolMessage
from textual.app import ComposeResult
from textual.containers import Vertical

from .chat_input import ChatInput
from .message_list_view import MessageListView


class ChatView(Vertical):
    """Complete chat interface with scrollable messages and input"""

    DEFAULT_CSS = """
    ChatView {
        width: 1fr;
        background: $surface;
        padding: 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the chat interface"""
        yield MessageListView(id="message-list")
        yield ChatInput(
            id="chat-input", placeholder="Type a message and press Enter..."
        )

    def on_mount(self) -> None:
        """Initialize chat with welcome message"""
        self.add_message(
            AIMessage(
                content="Hello! I'm DeerCode Agent. I can help you write and execute code."
            )
        )
        self.focus_input()

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the chat"""
        message_list = self.query_one("#message-list", MessageListView)
        if not isinstance(message, ToolMessage):
            message_list.add_message(message)

    def focus_input(self) -> None:
        """Focus the input field"""
        chat_input = self.query_one("#chat-input", ChatInput)
        chat_input.focus()
