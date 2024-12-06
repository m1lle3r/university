from feature import Feature
from utils.render import ConsoleRender
from user import User
import os

functions = {
    "0": lambda feature: feature.change_directory(),
    "1": lambda feature: feature.convert_to_docx(),
    "2": lambda feature: feature.convert_to_pdf(),
    "3": lambda feature: feature.compress_image(),
    "4": lambda feature: feature.delete_group_files()
}

options = [
    'Сменить каталог',
    'Преобразовать PDF -> Docx',
    'Преобразовать Docx -> PDF',
    'Сжать изображение',
    'Удалить цепочку файлов',
    'Выход'
]
user_instance = User(os.getcwd())
executor = Feature(user_instance)

ConsoleRender.render_line('\n'.join([f"{index}. {option}" for index, option in enumerate(options[:5])]))

while True:
    task = user_instance.select(functions)[1]
    if task:
        task(executor)
