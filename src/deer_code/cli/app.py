import re

from langchain.schema import AIMessage, BaseMessage, HumanMessage
from langchain.schema.messages import ToolMessage
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, TabbedContent, TabPane

from deer_code.agents import coding_agent
from deer_code.project import project

from .components import ChatView, EditorTabs, TerminalView, TodoListView
from .theme import DEER_DARK_THEME


class ConsoleApp(App):
    TITLE = "🦌 DeerCode"

    CSS = """
    Screen {
        layout: horizontal;
        background: $background;
    }

    Header {
        background: #161c10;
    }

    Footer {
        background: #181c40;
    }

    #left-panel {
        width: 3fr;
        background: $panel;
    }

    #right-panel {
        width: 4fr;
        background: $boost;
    }

    #editor-view {
        height: 70%;
    }

    #bottom-right-tabs {
        height: 30%;
        background: $panel;
    }

    #bottom-right-tabs TabPane {
        padding: 0;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    _is_busy = False

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    def set_busy(self, is_busy: bool) -> None:
        self._is_busy = is_busy

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Vertical(id="left-panel"):
            yield ChatView(id="chat-view")
        with Vertical(id="right-panel"):
            yield EditorTabs(id="editor-tabs")
            with TabbedContent(id="bottom-right-tabs"):
                with TabPane(id="terminal-tab", title="Terminal"):
                    yield TerminalView(id="terminal-view")
                with TabPane(id="todo-tab", title="Todo"):
                    yield TodoListView(id="todo-list-view")
        yield Footer(id="footer")

    def on_mount(self) -> None:
        self.register_theme(DEER_DARK_THEME)
        self.theme = "deer-dark"
        self.sub_title = project.root_dir

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if not self.is_busy and event.input.id == "chat-input":
            user_input = event.value.strip()
            if user_input:
                event.input.value = ""
                user_message = HumanMessage(content=user_input)
                await self._handle_user_input(user_message)

    async def _handle_user_input(self, user_message: HumanMessage) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        editor_tabs = self.query_one("#editor-tabs", EditorTabs)
        bottom_right_tabs = self.query_one("#bottom-right-tabs", TabbedContent)
        terminal_view = self.query_one("#terminal-view", TerminalView)
        todo_list_view = self.query_one("#todo-list-view", TodoListView)
        chat_view.add_message(user_message)
        self.set_busy(True)
        bash_tool_call_ids: list[str] = []
        async for chunk in coding_agent.astream(
            {"messages": [user_message]},
            stream_mode="updates",
            config={"recursion_limit": 100},
        ):
            roles = chunk.keys()
            for role in roles:
                messages: list[BaseMessage] = chunk[role].get("messages", [])
                for message in messages:
                    chat_view.add_message(message)
                    if isinstance(message, AIMessage) and message.tool_calls:
                        for tool_call in message.tool_calls:
                            if tool_call["name"] == "bash":
                                bash_tool_call_ids.append(tool_call["id"])
                                terminal_view.write(f"$ {tool_call["args"]["command"]}")
                                bottom_right_tabs.active = "terminal-tab"
                            elif tool_call["name"] == "todo_write":
                                bottom_right_tabs.active = "todo-tab"
                                todo_list_view.update_items(tool_call["args"]["items"])
                            elif tool_call["name"] == "text_editor":
                                command = tool_call["args"]["command"]
                                if command == "create":
                                    editor_tabs.open_file(
                                        tool_call["args"]["path"],
                                        tool_call["args"]["file_text"],
                                    )
                                else:
                                    editor_tabs.open_file(tool_call["args"]["path"])
                    if isinstance(message, ToolMessage):
                        if message.tool_call_id in bash_tool_call_ids:
                            output = self._extract_code(message.content)
                            terminal_view.write(
                                output if output.strip() != "" else "\n(empty)\n",
                                muted=True,
                            )
                            bash_tool_call_ids.remove(message.tool_call_id)
        self.set_busy(False)
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

    def _extract_code(self, text: str) -> str:
        match = re.search(r"```(.*)```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text


app = ConsoleApp()

if __name__ == "__main__":
    app.run()
