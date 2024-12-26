import os
import PySimpleGUI as sg
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
        except Exception as e:
            print(f"Ошибка при удалении {file}: {e}")


# Основная логика программы
def main():
    layout = [
        [sg.Text("Выберите файлы"), sg.Input(key="-FILES-", enable_events=True), sg.FilesBrowse()],
        [sg.Listbox(values=[], enable_events=True, size=(50, 20), key="-FILE LIST-")],
        [sg.Button("Обработать выбранные файлы"), sg.Button("Удалить файлы"), sg.Exit()]
    ]

    window = sg.Window("Файловый процессор", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        # При выборе файлов отображаем их в списке
        if event == "-FILES-":
            file_list = values["-FILES-"].split(";")  # Получаем список файлов
            filtered_files = [
                f for f in file_list if f.endswith((".docx", ".pdf", ".png", ".jpg", ".jpeg"))
            ]
            window["-FILE LIST-"].update(filtered_files)

        # При нажатии на кнопку "Обработать выбранные файлы"
        if event == "Обработать выбранные файлы":
            selected_files = values["-FILE LIST-"]
            if not selected_files:
                sg.popup("Не выбраны файлы!")
                continue

            for file_path in selected_files:
                if file_path.endswith(".docx"):
                    output_pdf = os.path.splitext(file_path)[0] + ".pdf"
                    convert_docx_to_pdf(file_path, output_pdf)
                    sg.popup(f"Файл {file_path} конвертирован в PDF.")

                elif file_path.endswith(".pdf"):
                    output_docx = os.path.splitext(file_path)[0] + ".docx"
                    convert_pdf_to_docx(file_path, output_docx)
                    sg.popup(f"Файл {file_path} конвертирован в DOCX.")

                elif file_path.endswith((".png", ".jpg", ".jpeg")):
                    output_image = os.path.splitext(file_path)[0] + "_compressed.jpg"
                    compress_image(file_path, output_image)
                    sg.popup(f"Файл {file_path} сжат.")

        # При нажатии на кнопку "Удалить файлы"
        if event == "Удалить файлы":
            selected_files = values["-FILE LIST-"]
            if not selected_files:
                sg.popup("Не выбраны файлы для удаления!")
                continue

            delete_files(selected_files)
            sg.popup(f"Файлы {', '.join(selected_files)} удалены.")

    window.close()


if __name__ == "__main__":
    main()
