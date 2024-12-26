import os
from docx import Document
from PIL import Image
from fpdf import FPDF
from pdf2docx import Converter


# Функция конвертации .docx в .pdf
def convert_docx_to_pdf(input_path, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Устанавливаем шрифт, который поддерживает Unicode
    pdf.add_font('ArialUnicode', '', '/Library/Fonts/Arial Unicode.ttf', uni=True)
    pdf.set_font("ArialUnicode", size=12)

    doc = Document(input_path)

    # Проход по параграфам документа
    for paragraph in doc.paragraphs:
        pdf.multi_cell(0, 10, paragraph.text)  # Многострочный текст

    pdf.output(output_path)


# Функция конвертации .pdf в .docx
def convert_pdf_to_docx(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)  # Конвертирует весь PDF в DOCX
    cv.close()


# Функция сжатия изображения
def compress_image(input_path, output_path):
    with Image.open(input_path) as img:
        img = img.convert("RGB")  # Преобразуем изображение в RGB (если оно в другом цвете)
        img.save(output_path, "JPEG", optimize=True, quality=50)  # Сжимаем и сохраняем в JPEG


# Функция для удаления файлов
def delete_files(files):
    for file in files:
        try:
            os.remove(file)
            print(f"Файл {file} удалён.")
        except Exception as e:
            print(f"Ошибка при удалении {file}: {e}")


# Функция смены директории
def change_directory():
    new_directory = input("Введите новый путь к директории: ")
    if os.path.isdir(new_directory):
        os.chdir(new_directory)
        print(f"Текущая директория изменена на: {new_directory}")
    else:
        print("Указанный путь не существует или не является директорией.")


# Основная логика программы
def main():
    print("Добро пожаловать в файловый процессор!")

    while True:
        print("\nВыберите действие:")
        print("1. Конвертировать .docx в .pdf")
        print("2. Конвертировать .pdf в .docx")
        print("3. Сжать изображение")
        print("4. Удалить файлы")
        print("5. Сменить текущую директорию")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            input_path = input("Введите путь к файлу .docx: ")
            if os.path.isfile(input_path) and input_path.endswith(".docx"):
                output_pdf = os.path.splitext(input_path)[0] + ".pdf"
                convert_docx_to_pdf(input_path, output_pdf)
                print(f"Файл {input_path} успешно конвертирован в {output_pdf}.")
            else:
                print("Неверный путь или файл не существует.")

        elif choice == "2":
            input_path = input("Введите путь к файлу .pdf: ")
            if os.path.isfile(input_path) and input_path.endswith(".pdf"):
                output_docx = os.path.splitext(input_path)[0] + ".docx"
                convert_pdf_to_docx(input_path, output_docx)
                print(f"Файл {input_path} успешно конвертирован в {output_docx}.")
            else:
                print("Неверный путь или файл не существует.")

        elif choice == "3":
            input_path = input("Введите путь к изображению (.png, .jpg, .jpeg): ")
            if os.path.isfile(input_path) and input_path.lower().endswith((".png", ".jpg", ".jpeg")):
                output_image = os.path.splitext(input_path)[0] + "_compressed.jpg"
                compress_image(input_path, output_image)
                print(f"Файл {input_path} успешно сжат.")
            else:
                print("Неверный путь или файл не существует.")

        elif choice == "4":
            files_to_delete = input("Введите пути к файлам, разделённые пробелом, для удаления: ").split()
            files_to_delete = [file.strip() for file in files_to_delete]
            delete_files(files_to_delete)

        elif choice == "5":
            change_directory()

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
