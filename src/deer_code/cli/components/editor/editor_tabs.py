from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Markdown, TabbedContent, TabPane

from .code_view import CodeView


class EditorTabs(TabbedContent):
    DEFAULT_CSS = """
    EditorTabs {
        height: 1fr;
    }
    """

    tab_map: dict[str, TabPane] = {}

    def open_file(self, path: str, file_text: str = None):
        tab = self._find_tab_by_path(path)
        if tab is None:
            tab = EditorTab(path)
            self.tab_map[path] = tab
            self.add_pane(tab)
        self.active = tab.id
        tab.update(file_text)
        return tab

    def open_welcome(self):
        tab = TabPane(title="Welcome", id="welcome-tab")
        markdown = Markdown(Path("docs/welcome.md").read_text(), id="welcome-view")
        self.add_pane(tab)
        tab.mount(markdown)
        self.active = tab.id

    def _find_tab_by_path(self, path: str) -> TabPane | None:
        return self.tab_map.get(path)


class EditorTab(TabPane):
    def __init__(self, path: str, **kwargs):
        title = extract_filename(path)
        super().__init__(title=title, **kwargs)
        self.path = path

    def compose(self) -> ComposeResult:
        yield CodeView(id="code-view")

    def update(self, file_text: str | None = None):
        code_view = self.query_one("#code-view", CodeView)
        if file_text is not None:
            code_view.update_code(file_text, self.path)
        else:
            with open(self.path, "r") as file:
                code = file.read()
                code_view.update_code(code, self.path)


def extract_filename(path: str) -> str:
    _path = Path(path)
    return _path.name
