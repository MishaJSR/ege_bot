import os
from os import listdir
from os.path import isfile, join
from docx import Document

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def get_all_files_in_directory(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

# Пример использования
directory_path = os.getcwd() + '\\loader\\human'
all_files = get_all_files_in_directory(directory_path)
for file in all_files:
    text = extract_text_from_docx(file)
    res = text.split("\n\n")
    chapter = "Человек и общество"
    under_chapter = None
    for el in res:
        description = None
        answer_mode = None
        answers = ""
        answer = None
        about = None
        addition = None
        pp = el.split("\n")
        if len(pp) == 1:
            under_chapter = pp[0]
        else:
            description = pp[0]
            if "Пояснение. " in pp:
                index_about = pp.index("Пояснение. ")
                for answers_text in pp[1:index_about]:
                    answers += answers_text.replace(")", ".") + '\n'
                about = pp[index_about + 1].replace(")", ".")
                answer = pp[-1].split("Ответ:")[1].replace(".", "")
            else:
                for answers_text in pp[1:-1]:
                    answers += answers_text.replace(")", ".") + '\n'
                answer = pp[-1].split("Ответ:")[1].replace(".", "")
                pass
            print("Описание\n", description)
            print("Ответы\n", answers)
            print("Пояснение\n", about)
            print("Ответ\n", answer)
            print("\n\n")