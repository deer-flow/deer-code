import os


class Project:
    """A project is a directory that contains a project."""

    _root_dir: str

    def __init__(self, path: str):
        self._root_dir = path

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    def root_dir(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Project root directory {path} does not exist")
        if not os.path.isdir(path):
            raise NotADirectoryError(
                f"Project root directory {path} is not a directory"
            )
        self._root_dir = path


project = Project(os.getcwd())
