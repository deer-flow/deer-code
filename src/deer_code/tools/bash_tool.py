from langchain.tools import tool

from deer_code import project
from deer_code.terminals import BashTerminal

keep_alive_terminal = BashTerminal()


@tool("bash", parse_docstring=True)
def bash_tool(command: str, reset_cwd: bool = False):
    """Execute a standard bash command in a keep-alive shell, and return the output if successful or error message if failed.

    Args:
        command: The command to execute.
        reset_cwd: Whether to reset the current working directory to the project root directory.
    """
    global keep_alive_terminal
    if reset_cwd:
        if keep_alive_terminal:
            keep_alive_terminal.close()
        keep_alive_terminal = BashTerminal(project.root_dir)
    return keep_alive_terminal.execute(command)
