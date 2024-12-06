class ConsoleRender:

    @staticmethod
    def render_with_builder(builder, objects: list):
        print(builder(len(objects), objects))

    @staticmethod
    def render(objects: list):
        print(objects)

    @staticmethod
    def render_line(line: str):
        print(line)