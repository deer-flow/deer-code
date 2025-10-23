import fnmatch
from pathlib import Path
from typing import Optional

from langchain.tools import ToolRuntime, tool

from deer_code.tools.reminders import generate_reminders

from .ignore import DEFAULT_IGNORE_PATTERNS


@tool("ls", parse_docstring=True)
def ls_tool(
    runtime: ToolRuntime,
    path: str,
    match: Optional[list[str]] = None,
    ignore: Optional[list[str]] = None,
):
    """Lists files and directories in a given path. Optionally provide an array of glob patterns to match and ignore.

    Args:
        path: The absolute path to list files and directories from. Relative paths are **not** allowed.
        match: An optional array of glob patterns to match.
        ignore: An optional array of glob patterns to ignore.
    """
    _path = Path(path)
    if not _path.is_absolute():
        return f"Error: the path {path} is not an absolute path. Please provide an absolute path."
    if not _path.exists():
        return f"Error: the path {path} does not exist. Please provide a valid path."

    if not _path.is_dir():
        return f"Error: the path {path} is not a directory. Please provide a valid directory path."

    # Get all items in the directory
    try:
        items = list(_path.iterdir())
    except PermissionError:
        return f"Error: permission denied to access the path {path}."

    # Sort items: directories first, then files, both alphabetically
    items.sort(key=lambda x: (x.is_file(), x.name.lower()))

    # Apply match patterns if provided
    if match:
        filtered_items = []
        for item in items:
            for pattern in match:
                if fnmatch.fnmatch(item.name, pattern):
                    filtered_items.append(item)
                    break
        items = filtered_items

    ignore = (ignore or []) + DEFAULT_IGNORE_PATTERNS
    filtered_items = []
    for item in items:
        should_ignore = False
        for pattern in ignore:
            if fnmatch.fnmatch(item.name, pattern):
                should_ignore = True
                break
        if not should_ignore:
            filtered_items.append(item)
    items = filtered_items

    reminders = generate_reminders(runtime)

    # Format the output
    if not items:
        return f"No items found in {path}.{reminders}"

    result_lines = []
    for item in items:
        if item.is_dir():
            result_lines.append(item.name + "/")
        else:
            result_lines.append(item.name)

    return (
        f"Here's the result in {path}: \n```\n"
        + "\n".join(result_lines)
        + f"\n```{reminders}"
    )


if __name__ == "__main__":
    print(
        ls_tool.invoke(
            {
                "path": "/Users/henry/Desktop/next-js-demo",
                "ignore": ["*.js*"],
            }
        )
    )
