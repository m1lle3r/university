from typing import Any


class User:

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def select(self, objects: dict[str, Any]) -> tuple:
        operation_id = self.await_value(
            lambda value: value.isdigit(),
            "Число должно быть целым!",
            "Выберите действие"
        )

        if not (0 <= int(operation_id) < len(objects)):
            print(f"Число должно быть в диапазоне [0; {len(objects) - 1}]")
            return None, None

        return operation_id, objects[operation_id]

    @staticmethod
    def await_value(validator, error_message: str, view_text: str):
        while True:
            entered_value = input(f'{view_text}: ')
            if validator(entered_value):
                return entered_value
            print(error_message)

    def set_work_dir(self, new_dir: str):
        self.work_dir = new_dir

    def get_work_dir(self) -> str:
        return self.work_dir
