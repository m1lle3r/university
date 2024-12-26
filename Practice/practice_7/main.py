import os
import PySimpleGUI as sg
from docx import Document
from PIL import Image
from fpdf import FPDF

def convert_docx_to_pdf(input_path, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    doc = Document(input_path)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for paragraph in doc.paragraphs:
        pdf.multi_cell(0, 10, paragraph.text)
    pdf.output(output_path)

def compress_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", optimize=True, quality=50)

def main():
    layout = [
        [sg.Text("Select Folder"), sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Listbox(values=[], enable_events=True, size=(50, 20), key="-FILE LIST-")],
        [sg.Button("Process Selected Files"), sg.Exit()]
    ]

    window = sg.Window("File Processor", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            if os.path.isdir(folder):
                file_list = os.listdir(folder)
                filtered_files = [
                    f for f in file_list if f.endswith((".docx", ".pdf", ".png", ".jpg", ".jpeg"))
                ]
                window["-FILE LIST-"].update(filtered_files)

        if event == "Process Selected Files":
            selected_files = values["-FILE LIST-"]
            folder = values["-FOLDER-"]
            if not selected_files:
                sg.popup("No files selected!")
                continue

            for file_name in selected_files:
                file_path = os.path.join(folder, file_name)

                if file_name.endswith(".docx"):
                    output_pdf = os.path.splitext(file_path)[0] + ".pdf"
                    convert_docx_to_pdf(file_path, output_pdf)
                    sg.popup(f"Converted {file_name} to PDF.")

                elif file_name.endswith((".png", ".jpg", ".jpeg")):
                    output_image = os.path.splitext(file_path)[0] + "_compressed.jpg"
                    compress_image(file_path, output_image)
                    sg.popup(f"Compressed {file_name}.")

    window.close()

if __name__ == "__main__":
    main()
