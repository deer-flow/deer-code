import sys
from pathlib import Path

from dotenv import load_dotenv

from deer_code.cli.app import ConsoleApp

from .project import project

load_dotenv()


def main():
    """Main entry point for deer-code."""
    if len(sys.argv) > 1:
        project.root_dir = Path(sys.argv[1])
    app = ConsoleApp()
    app.run()


if __name__ == "__main__":
    main()
