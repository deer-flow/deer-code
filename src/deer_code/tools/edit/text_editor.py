from pathlib import Path
from typing import Literal

TextEditorCommand = Literal[
    "view",
    "create",
    "str_replace",
    "insert",
]


class TextEditor:
    """A standalone text editor tool for AI agents to interact with files.

    This tool allows viewing, creating, and editing files with proper error handling
    and suggestions to help AI agents learn from mistakes.
    """

    def validate_path(self, command: TextEditorCommand, path: Path):
        """Check that the path is absolute.

        Args:
            command: The command to execute.
            path: The path to the file or directory.

        Raises:
            ValueError: If path is not absolute.
        """
        if not path.is_absolute():
            suggested_path = Path("") / path
            raise ValueError(
                f"The path {path} is not an absolute path, it should start with `/`. Do you mean {suggested_path}?"
            )

    def view(self, path: Path, view_range: list[int] | None = None):
        """View the content of a file.

        Args:
            path: The absolute path to the file.
            view_range: Optional list of two integers [start, end] for line range.
                Line numbers are 1-indexed. Use -1 for end line to read to EOF.

        Returns:
            str: The file content with line numbers.

        Raises:
            ValueError: If file doesn't exist, is not a file, or view_range is invalid.
        """
        if not path.exists():
            raise ValueError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        file_content = self.read_file(path)
        init_line = 1
        if view_range:
            if len(view_range) != 2 or not all(isinstance(i, int) for i in view_range):
                raise ValueError(
                    "Invalid `view_range`. It should be a list of two integers."
                )
            file_lines = file_content.split("\n")
            n_lines_file = len(file_lines)
            init_line, final_line = view_range

            # Validate the start line
            if init_line < 1 or init_line > n_lines_file:
                raise ValueError(
                    f"Invalid `view_range`: {view_range}. The start line `{init_line}` should be within the range of lines in the file: {[1, n_lines_file]}"
                )

            # Validate the end line
            if final_line != -1 and (
                final_line < init_line or final_line > n_lines_file
            ):
                if final_line > n_lines_file:
                    final_line = n_lines_file
                else:
                    raise ValueError(
                        f"Invalid `view_range`: {view_range}. The end line `{final_line}` should be -1 or "
                        f"within the range of lines in the file: {[init_line, n_lines_file]}"
                    )

            # Slice the file content based on the view range
            if final_line == -1:
                file_content = "\n".join(file_lines[init_line - 1 :])
            else:
                file_content = "\n".join(file_lines[init_line - 1 : final_line])

        return self._content_with_line_numbers(file_content, init_line=init_line)

    def str_replace(self, path: Path, old_str: str, new_str: str | None):
        """Replace all occurrences of old_str with new_str in the file.

        Args:
            path: The path to the file.
            old_str: The string to be replaced.
            new_str: The replacement string. If None, old_str will be removed.

        Returns:
            int: The count of replacements.

        Raises:
            ValueError: If file doesn't exist, is not a file, or old_str not found.
        """
        if not path.exists():
            raise ValueError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        # Read the file content
        file_content = self.read_file(path)

        # Check if old_str exists in the file
        if old_str not in file_content:
            raise ValueError(f"String '{old_str}' not found in file: {path}")

        # Perform the replacement
        if new_str is None:
            new_str = ""

        new_content = file_content.replace(old_str, new_str)

        # Count occurrences for the result message
        occurrences = file_content.count(old_str)

        # Write the modified content back to the file
        self.write_file(path, new_content)

        return occurrences

    def insert(self, path: Path, insert_line: int, new_str: str):
        """Insert text at a specific line in the file.

        Args:
            path: The path to the file to modify.
            insert_line: The line number after which to insert (0 for beginning).
            new_str: The text to insert.

        Raises:
            ValueError: If file doesn't exist, is not a file, or insert_line is invalid.
        """
        if not path.exists():
            raise ValueError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        # Read the file content
        file_content = self.read_file(path)
        lines = file_content.splitlines()

        # Validate insert_line
        if insert_line < 0:
            raise ValueError(
                f"Invalid insert_line: {insert_line}. Line number must be >= 0."
            )

        if insert_line > len(lines):
            raise ValueError(
                f"Invalid insert_line: {insert_line}. Line number cannot be greater than the number of lines in the file ({len(lines)})."
            )

        # Insert the new text
        if insert_line == 0:
            # Insert at the beginning of the file
            lines.insert(0, new_str)
        else:
            # Insert after the specified line (insert_line is 1-indexed for insertion)
            lines.insert(insert_line, new_str)

        # Join the lines back together
        new_content = "\n".join(lines)

        # Write the modified content back to the file
        self.write_file(path, new_content)

    def read_file(self, path: Path):
        """Read the content of a file.

        Args:
            path: The path to the file to read.

        Returns:
            str: The file content.

        Raises:
            ValueError: If file cannot be read.
        """
        try:
            return path.read_text()
        except Exception as e:
            raise ValueError(f"Error reading {path}: {e}")

    def write_file(self, path: Path, content: str):
        """Write content to a file.

        Args:
            path: The path to the file to write.
            content: The content to write.

        Raises:
            ValueError: If file cannot be written.
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        except Exception as e:
            raise ValueError(f"Error writing to {path}: {e}")

    def _content_with_line_numbers(
        self,
        file_content: str,
        init_line: int = 1,
    ):
        lines = file_content.splitlines()
        lines = [f"{i + init_line:>3} {line}" for i, line in enumerate(lines)]
        file_content = "\n".join(lines)
        return file_content
