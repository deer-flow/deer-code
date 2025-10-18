from typing import Optional

from langchain.tools import tool

from deer_code.project import project

from .bash_terminal import BashTerminal

keep_alive_terminal: BashTerminal | None = None


@tool("bash", parse_docstring=True)
def bash_tool(command: str, reset_cwd: Optional[bool] = False):
    """Execute a standard bash command in a keep-alive shell, and return the output if successful or error message if failed.

    Args:
        command: The command to execute.
        reset_cwd: Whether to reset the current working directory to the project root directory.
    """
    global keep_alive_terminal
    if keep_alive_terminal is None:
        keep_alive_terminal = BashTerminal(project.root_dir)
    elif reset_cwd:
        keep_alive_terminal.close()
        keep_alive_terminal = BashTerminal(project.root_dir)
    return f"```\n{keep_alive_terminal.execute(command)}\n```"
