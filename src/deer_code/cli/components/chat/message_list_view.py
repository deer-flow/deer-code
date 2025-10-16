from langchain.schema import BaseMessage
from textual.containers import VerticalScroll

from .message_item_view import MessageItemView


class MessageListView(VerticalScroll):
    """Scrollable message list container"""

    DEFAULT_CSS = """
    MessageListView {
        height: 1fr;
        padding: 1 0;
        background: $surface;
    }
    """

    messages: list[BaseMessage] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_focus = True

    def add_message(self, message: BaseMessage) -> None:
        """Add a new message to the list"""
        display_header = True
        if len(self.messages) == 0:
            display_header = True
        else:
            last_message = self.messages[-1]
            if last_message:
                if last_message.type == message.type:
                    display_header = False
        self.messages.append(message)
        message_item_view = MessageItemView(message, display_header=display_header)
        self.mount(message_item_view)
        self.scroll_end(animate=True)
