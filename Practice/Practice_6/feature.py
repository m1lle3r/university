import os

from PIL import Image
from docx.api import Document
from pdf2docx import Converter
from user import User
from utils.file_manager import FileManager
from utils.render import ConsoleRender


class Feature:

    def __init__(self, entity: User):
        self.entity = entity
        self.path = entity.get_work_dir()
        self.file_manager = FileManager()

        if not os.path.exists(self.path):
            raise FileNotFoundError("Файл/директория не найден(-а)")

    def change_directory(self):
        new_path = self.entity.await_value(
            lambda path: os.path.isdir(path),
            "Путь не ведет до папки",
            "Введите путь до директории"
        )
        self.entity.set_work_dir(new_path)
        self.path = new_path
        os.chdir(new_path)
        print(f"Вы успешно сменили директорию на {new_path}")

    def compress_image(self):
        files = self.file_manager.get_path_files_by_extensions(self.path, "jpeg", 'jpg', 'png', 'gif')
        self._display_files(files)

        file_id = self.entity.await_value(
            lambda value: value.isdigit() or value == '*',
            "Индекс должен быть числом или *",
            "Выберите файл для сжатия (* - все)"
        )

        if file_id != '*' and (0 <= int(file_id) >= len(files)):
            print(f"Индекс должен быть в диапазоне [0, {len(files) - 1}] или *")
            return

        quality = int(self.entity.await_value(
            lambda value: value.isdigit(),
            "Процент сжатия должен быть числом",
            "Введите качество (0-100)"
        ))

        if 0 <= quality <= 100:
            image_tool = self.__ImageToolWrapper()
            if file_id == '*':
                for file in files:
                    image_tool.save_with_argument(self.path, file, quality)
            else:
                image_tool.save_with_argument(self.path, files[int(file_id)], quality)

    def convert_to_pdf(self):
        self._convert_file("docx", "pdf", Document)

    def convert_to_docx(self):
        self._convert_file("pdf", "docx", Converter)

    def _convert_file(self, from_ext, to_ext, converter):
        files = self.file_manager.get_path_files_by_extension(self.path, from_ext)
        self._display_files(files)

        file_id = int(self.entity.await_value(
            lambda value: str(value).isnumeric(),
            f"Индекс должен быть числом",
            f"Выберите номер файла для конвертации"
        ))

        if 0 <= file_id >= len(files):
            print(f"Индекс должен быть в диапазоне [0, {len(files) - 1}]")
            return

        file = files[file_id]
        try:
            if from_ext == "docx":
                doc = converter(self.path + fr'\{file}')
                doc.save(self.path + fr'\{file[:-4]}.pdf')
            else:
                provider = converter(self.path + fr'\{file}')
                provider.convert(self.path + fr"\converted-{file[:-3]}.docx")
            print(f"Файл успешно конвертирован в {to_ext}")
        except Exception:
            print(f"Ошибка при конвертации ({from_ext} -> {to_ext})")

    def delete_group_files(self):
        actions = [
            ("Все файлы, начинающиеся на подстроку", self._delete_startswith_substring),
            ("Все файлы, заканчивающиеся на подстроку", self._delete_endswith_substring),
            ("Все файлы, содержащие подстроку", self._delete_contains_substring),
            ("Все файлы по расширению", self._delete_with_extension_substring)
        ]
        self._display_actions(actions)

        action_id = int(self.entity.await_value(
            lambda value: value.isdigit(),
            "Индекс должен быть числом",
            "Выберите действие"
        ))

        if action_id < 0 or action_id >= len(actions):
            print(f"Индекс действия должен быть в диапазоне [0, {len(actions) - 1}]")
            return

        argument = self.entity.await_value(
            lambda value: value.strip(),
            "Аргумент не может быть пустым",
            "Введите аргумент для действия"
        )

        actions[action_id][1](argument)

    def _display_files(self, files):
        ConsoleRender.render_line('\n'.join([f"{index}. {file}" for index, file in enumerate(files)]))

    def _display_actions(self, actions):
        ConsoleRender.render_line('\n'.join([f"{index}. {desc}" for index, (desc, _) in enumerate(actions)]))

    def _delete_startswith_substring(self, substring: str):
        self._delete_files(self.file_manager.get_path_files_with_substring(self.path, substring, True))

    def _delete_endswith_substring(self, substring: str):
        self._delete_files(self.file_manager.get_path_files_with_substring(self.path, substring))

    def _delete_contains_substring(self, substring: str):
        self._delete_files(self.file_manager.get_path_files_contains_substring(self.path, substring))

    def _delete_with_extension_substring(self, extension: str):
        self._delete_files(self.file_manager.get_path_files_by_extension(self.path, extension))

    def _delete_files(self, files):
        for file in files:
            os.remove(self.path + fr'\{file}')
            print(f"Удален файл: {file}")

    class __ImageToolWrapper:

        @staticmethod
        def save_with_argument(input_path: str, file: str, quality: int):
            try:
                image_file = Image.open(input_path + fr'\{file}')
                image_file.save(input_path + fr'\compressed-{file}', quality=quality)
            except Exception:
                print("Ошибка при сохранении изображения")
