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
        about = ""
        addition = None
        pp = el.split("\n")
        ind_pp = 0
        if len(pp) == 1:
            under_chapter = pp[0]
        else:
            if len(pp[0]) == 0:
                ind_pp = 1
            description = pp[ind_pp]
            if "Пояснение. " in pp:
                index_about = pp.index("Пояснение. ")
                for answers_text in pp[ind_pp+1:index_about]:
                    answers += answers_text.replace(")", ".") + '\n'
                for ab_el in pp[index_about + 1:-1]:
                    about += ab_el.replace(")", ".")
                answer = pp[-1].split("Ответ:")[1].replace(".", "")
            else:
                for answers_text in pp[ind_pp+1:-1]:
                    answers += answers_text.replace(")", ".") + '\n'
                answer = pp[-1].split("Ответ:")[1].replace(".", "")
            if about == "":
                about = None
            if description[0].isdigit():
                if description[1].isdigit():
                    description = description[4:]
                else:
                    description = description[3:]
            print("Документ\n", under_chapter)