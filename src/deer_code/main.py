import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from deer_code.project import Project

load_dotenv()

project = Project(os.getcwd())


def main():
    """Main entry point for deer-code."""
    global project
    if len(sys.argv) < 2:
        project = Project(os.getcwd())
    else:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"Error: Path {path} does not exist")
            sys.exit(1)
        if not path.is_dir():
            print(f"Error: Path {path} is not a directory")
            sys.exit(1)
        project = Project(path.resolve())
    print(f"Project root: {project.root_dir}")


if __name__ == "__main__":
    main()
