class Project:
    def __init__(self, path: str):
        self._root_dir = path

    @property
    def root_dir(self):
        return self._root_dir
