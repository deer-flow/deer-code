import fnmatch
from pathlib import Path
from typing import Optional

from langchain.tools import tool

from .ignore import DEFAULT_IGNORE_PATTERNS


def should_ignore(path: Path, ignore_patterns: list[str]) -> bool:
    """Check if a path should be ignored based on ignore patterns."""
    path_str = str(path)
    name = path.name

    for pattern in ignore_patterns:
        # Remove /** or /* suffix for matching
        clean_pattern = pattern.rstrip("/**").rstrip("/*")

        # Match against the name or full path
        if fnmatch.fnmatch(name, clean_pattern) or fnmatch.fnmatch(path_str, pattern):
            return True

    return False


def generate_tree(
    directory: Path,
    prefix: str = "",
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    ignore_patterns: list[str] = None,
) -> list[str]:
    """Recursively generate tree structure."""
    if ignore_patterns is None:
        ignore_patterns = []

    lines = []

    # Check depth limit
    if max_depth is not None and current_depth >= max_depth:
        return lines

    try:
        # Get all entries and sort them (directories first, then files)
        entries = sorted(
            directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())
        )

        # Filter out ignored entries
        entries = [e for e in entries if not should_ignore(e, ignore_patterns)]

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1

            # Determine the tree characters
            if is_last:
                connector = "└── "
                extension = "    "
            else:
                connector = "├── "
                extension = "│   "

            # Add the entry
            if entry.is_dir():
                lines.append(f"{prefix}{connector}{entry.name}/")
                # Recurse into subdirectory
                if max_depth is None or current_depth + 1 < max_depth:
                    sub_lines = generate_tree(
                        entry,
                        prefix + extension,
                        max_depth,
                        current_depth + 1,
                        ignore_patterns,
                    )
                    lines.extend(sub_lines)
            else:
                lines.append(f"{prefix}{connector}{entry.name}")

    except PermissionError:
        lines.append(f"{prefix}[Permission Denied]")

    return lines


@tool("tree", parse_docstring=True)
def tree_tool(
    path: Optional[str] = None,
    max_depth: Optional[int] = 3,
) -> str:
    """Display directory structure in a tree format, similar to the 'tree' command.

    Shows files and directories in a hierarchical tree structure.
    Automatically excludes common ignore patterns (version control, dependencies, build artifacts, etc.).

    Args:
        path: Directory path to display. Defaults to current working directory if not specified.
        max_depth: Maximum depth to traverse. The max_depth should be less than or equal to 3. Defaults to 3.

    Returns:
        A tree-structured view of the directory as a string.
    """
    # Set search path
    search_path = Path(path) if path else Path(".")

    try:
        # Validate path
        if not search_path.exists():
            return f"Error: Path '{search_path}' does not exist."

        if not search_path.is_dir():
            return f"Error: Path '{search_path}' is not a directory."

        # Generate tree
        lines = [str(search_path.resolve()) + "/"]
        tree_lines = generate_tree(
            search_path,
            max_depth=max_depth,
            ignore_patterns=DEFAULT_IGNORE_PATTERNS,
        )
        lines.extend(tree_lines)

        # Count directories and files
        dir_count = sum(1 for line in tree_lines if line.rstrip().endswith("/"))
        file_count = len(tree_lines) - dir_count

        # Add summary
        lines.append("")
        lines.append(f"{dir_count} directories, {file_count} files")

        output = "\n".join(lines)

        # Format the result
        return f"Here's the result in {search_path}:\n\n```\n{output}\n```"

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(tree_tool.invoke({"path": "/Users/henry/Desktop/next-js-demo"}))
