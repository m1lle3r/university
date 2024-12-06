import os


class FileManager:

    def _check_directory(self, path: str):
        if not os.path.isdir(path):
            raise NotADirectoryError("Путь не ведет до директории")

    def get_path_files_by_extension(self, path: str, extension: str):
        self._check_directory(path)
        return [name for name in os.listdir(path) if name.endswith(extension)]

    def get_path_files_with_substring(self, path: str, substring: str, start: bool = False):
        self._check_directory(path)
        return [name for name in os.listdir(path) if (name.startswith(substring) if start else name.endswith(substring))]

    def get_path_files_contains_substring(self, path: str, substring: str):
        self._check_directory(path)
        return [name for name in os.listdir(path) if substring in name]

    def get_path_files_by_extensions(self, path: str, *extensions):
        self._check_directory(path)
        files = []
        for file in os.listdir(path):
            if any(file.endswith(ext) for ext in extensions):
                files.append(file)
        return files
