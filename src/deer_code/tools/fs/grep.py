import subprocess
from typing import Literal, Optional

from langchain.tools import tool

from .ignore import DEFAULT_IGNORE_PATTERNS


@tool("grep", parse_docstring=True)
def grep_tool(
    pattern: str,
    path: Optional[str] = None,
    glob: Optional[str] = None,
    output_mode: Literal[
        "content", "files_with_matches", "count"
    ] = "files_with_matches",
    B: Optional[int] = None,
    A: Optional[int] = None,
    C: Optional[int] = None,
    n: Optional[bool] = None,
    i: Optional[bool] = None,
    type: Optional[str] = None,
    head_limit: Optional[int] = None,
    multiline: Optional[bool] = False,
) -> str:
    """A powerful search tool built on ripgrep for searching file contents with regex patterns.

    ALWAYS use this tool for search tasks. NEVER invoke `grep` or `rg` as a Bash command.
    Supports full regex syntax, file filtering, and various output modes.

    Args:
        pattern: The regular expression pattern to search for in file contents.
                Uses ripgrep syntax - literal braces need escaping (e.g., `interface\\{\\}` for `interface{}`).
        path: File or directory to search in. Defaults to current working directory if not specified.
        glob: Glob pattern to filter files (e.g., "*.js", "*.{ts,tsx}").
        output_mode: Output mode - "content" shows matching lines with optional context,
                    "files_with_matches" shows only file paths (default),
                    "count" shows match counts per file.
        B: Number of lines to show before each match. Only works with output_mode="content".
        A: Number of lines to show after each match. Only works with output_mode="content".
        C: Number of lines to show before and after each match. Only works with output_mode="content".
        n: Show line numbers in output. Only works with output_mode="content".
        i: Enable case insensitive search.
        type: File type to search (e.g., "js", "py", "rust", "go", "java").
             More efficient than glob for standard file types.
        head_limit: Limit output to first N lines/entries. Works across all output modes.
        multiline: Enable multiline mode where patterns can span lines and . matches newlines.
                  Default is False (single-line matching only).

    Returns:
        Search results as a string, formatted according to the output_mode.
    """
    # Build ripgrep command
    cmd = ["rg"]

    # Add pattern
    cmd.append(pattern)

    # Add path if specified
    search_path = path if path else "."
    cmd.append(search_path)

    # Add output mode flags
    if output_mode == "files_with_matches":
        cmd.append("-l")
    elif output_mode == "count":
        cmd.append("-c")
    # content mode is default, no flag needed

    # Add context flags (only for content mode)
    if output_mode == "content":
        if C is not None:
            cmd.extend(["-C", str(C)])
        else:
            if B is not None:
                cmd.extend(["-B", str(B)])
            if A is not None:
                cmd.extend(["-A", str(A)])
        if n:
            cmd.append("-n")

    # Add case insensitive flag
    if i:
        cmd.append("-i")

    # Add file type filter
    if type:
        cmd.extend(["--type", type])

    # Add glob pattern
    if glob:
        cmd.extend(["--glob", glob])

    # Apply default ignore patterns
    for ignore_pattern in DEFAULT_IGNORE_PATTERNS:
        cmd.extend(["--glob", f"!{ignore_pattern}"])

    # Add multiline mode
    if multiline:
        cmd.extend(["-U", "--multiline-dotall"])

    # Execute ripgrep
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't raise on non-zero exit (no matches found)
        )

        # Check for errors (exit code 2 indicates error, 1 means no matches)
        if result.returncode == 2 or result.stderr:
            return f"Error: {result.stderr.strip()}"

        output = result.stdout

        # Apply head limit if specified
        if head_limit and output:
            lines = output.splitlines()
            output = "\n".join(lines[:head_limit])

        # Format the result
        if output:
            return f"Here's the result in {search_path}:\n\n```\n{output}\n```"
        else:
            return "No matches found."

    except Exception as e:
        return f"Error: {str(e)}"
