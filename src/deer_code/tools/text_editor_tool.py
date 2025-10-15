from pathlib import Path

from langchain.tools import tool

from deer_code.editors import TextEditor


@tool("text_editor", parse_docstring=True)
def text_editor_tool(
    command: str,
    path: str,
    file_text: str | None = None,
    view_range: list[int] | None = None,
    old_str: str | None = None,
    new_str: str | None = None,
    insert_line: int | None = None,
):
    """
    A text editor tool supports view, create, str_replace, insert.

    Args:
        command: One of "view", "create", "str_replace", "insert".
        path: The absolute path to the file. Only absolute paths are supported.
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
    if command == "view":
        return f"Here's the result of running `cat -n` on {_path}:\n\n```\n{editor.view(_path, view_range)}\n```\n"
    elif command == "str_replace" and old_str is not None and new_str is not None:
        occurrences = editor.str_replace(_path, old_str, new_str)
        return f"Successfully replaced {occurrences} occurrences of {old_str} with {new_str} in {_path}."
    elif command == "insert" and insert_line is not None and new_str is not None:
        editor.insert(_path, insert_line, new_str)
        return f"Successfully inserted text at line {insert_line} in {path}."
    elif command == "create":
        if _path.exists():
            raise ValueError(
                f"File already exists at: {_path}. Cannot overwrite files using command `create`."
            )
        if _path.is_dir():
            raise ValueError(
                f"The path {_path} is a directory. Please provide a valid file path."
            )
        editor.write_file(_path, file_text if file_text is not None else "")
        return f"File successfully created at {_path}.\n\nIMPORTANT: Next, update the TODO list using `todo_write` immediately."
    else:
        raise ValueError(f"Invalid command: {command}")
