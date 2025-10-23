from pathlib import Path
from typing import Optional

from langchain.tools import ToolRuntime, tool

from deer_code.tools.reminders import generate_reminders

from .text_editor import TextEditor


@tool("text_editor", parse_docstring=True)
def text_editor_tool(
    runtime: ToolRuntime,
    command: str,
    path: str,
    file_text: Optional[str] = None,
    view_range: Optional[list[int]] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None,
    insert_line: Optional[int] = None,
):
    """
    A text editor tool supports view, create, str_replace, insert.

    - `view` again when you fail to perform `str_replace` or `insert`.
    - `create` can also be used to overwrite an existing file.
    - `str_replace` can also be used to delete text in the file.

    Args:
        command: One of "view", "create", "str_replace", "insert".
        path: The absolute path to the file. Only absolute paths are supported. Automatically create the directories if it doesn't exist.
        file_text: Only applies for the "create" command. The text to write to the file.
        view_range:
            Only applies for the "view" command.
            An array of two integers specifying the start and end line numbers to view.
            Line numbers are 1-indexed, and -1 for the end line means read to the end of the file.
        old_str: Only applies for the "str_replace" command. The text to replace (must match exactly, including whitespace and indentation).
        new_str: Only applies for the "str_replace" and "insert" commands. The new text to insert in place of the old text.
        insert_line: Only applies for the "insert" command. The line number after which to insert the text (0 for beginning of file).
    """
    editor = TextEditor()
    _path = Path(path)
    editor.validate_path(command, _path)
    reminders = generate_reminders(runtime)
    try:
        if command == "view":
            return f"Here's the result of running `cat -n` on {_path}:\n\n```\n{editor.view(_path, view_range)}\n```{reminders}"
        elif command == "str_replace" and old_str is not None and new_str is not None:
            occurrences = editor.str_replace(_path, old_str, new_str)
            return f"Successfully replaced {occurrences} occurrences in {_path}.{reminders}"
        elif command == "insert" and insert_line is not None and new_str is not None:
            editor.insert(_path, insert_line, new_str)
            return f"Successfully inserted text at line {insert_line} in {path}.{reminders}"
        elif command == "create":
            if _path.is_dir():
                return f"Error: the path {_path} is a directory. Please provide a valid file path.{reminders}"
            editor.write_file(_path, file_text if file_text is not None else "")
            return f"File successfully created at {_path}.{reminders}"
        else:
            return f"Error: invalid command: {command}"
    except Exception as e:
        return f"Error: {e}"
