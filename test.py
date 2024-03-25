import tkinter as tk
import sqlite3
from tkinter import ttk

def on_button_click():
    exam = entry_exam.get()
    chapter = entry_chapter.get()
    description = entry_description.get("1.0", "end-1c")
    a1 = entry_a1.get()
    a2 = entry_a2.get()
    a3 = entry_a3.get()
    a4 = entry_a4.get()
    a5 = entry_a5.get()
    a6 = entry_a6.get()
    res_a = []
    res_a.append(a1)
    res_a.append(a2)
    res_a.append(a3)
    res_a.append(a4)
    res_a.append(a5)
    res_a.append(a6)
    res_str = ''
    for el in res_a:
        if el != '':
            res_str += el + '` '
    res_str = res_str[:-2]
    a = entry_a.get()
    updated = '2024-03-19 11:44:19'
    about = entry_about.get("1.0", "end-1c")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    data = (exam, chapter, description, 'Квиз', res_str, a, about, updated)
    c.execute('INSERT INTO task (exam, chapter, description, answer_mode, answers, answer, about, updated) VALUES (?,?,?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()
    entry_exam.set(values[0])
    entry_chapter.set(chapter)
    entry_description.delete("1.0", tk.END)
    entry_a.delete(0, tk.END)
    entry_about.delete("1.0", tk.END)
    entry_a1.delete(0, tk.END)
    entry_a2.delete(0, tk.END)
    entry_a3.delete(0, tk.END)
    entry_a4.delete(0, tk.END)
    entry_a5.delete(0, tk.END)
    entry_a6.delete(0, tk.END)


def paste_text(event):
    entry_exam.delete(0, tk.END)
    entry_exam.insert(0, root.clipboard_get())

# Создаем графический интерфейс
root = tk.Tk()
root.title("Простое приложение")

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Создаем поле ввода
label = tk.Label(root, text="Экзамен")
label.pack()
values = ['Основная часть']
values2 = ['Человек и общество', 'Экономика', 'Социальные отношения', 'Политика', 'Право']
entry_exam = ttk.Combobox(root, values=values)
entry_exam.pack()
label = tk.Label(root, text="Глава")
label.pack()
entry_chapter = ttk.Combobox(root, values=values2)
entry_chapter.pack()
label = tk.Label(root, text="Описание")
label.pack()
entry_description = tk.Text(root, height=8, width=80)
entry_description.pack()
label = tk.Label(root, text="Ответ 1")
label.pack()
entry_a1 = tk.Entry(root, width=30)
entry_a1.pack()
label = tk.Label(root, text="Ответ 2")
label.pack()
entry_a2 = tk.Entry(root, width=30)
entry_a2.pack()
label = tk.Label(root, text="Ответ 3")
label.pack()
entry_a3 = tk.Entry(root, width=30)
entry_a3.pack()
label = tk.Label(root, text="Ответ 4")
label.pack()
entry_a4 = tk.Entry(root, width=30)
entry_a4.pack()
label = tk.Label(root, text="Ответ 5")
label.pack()
entry_a5 = tk.Entry(root, width=30)
entry_a5.pack()
label = tk.Label(root, text="Ответ 6")
label.pack()
entry_a6 = tk.Entry(root, width=30)
entry_a6.pack()
label = tk.Label(root, text="Ответ на задание")
label.pack()
entry_a = tk.Entry(root, width=30)
entry_a.pack()
label = tk.Label(root, text="Пояснение")
label.pack()
entry_about = tk.Text(root, height=8, width=80)
entry_about.pack()


# Создаем кнопку
button = tk.Button(root, text="Добавить в базу данных", command=on_button_click)
button.pack()

# Создаем метку для вывода результата
label = tk.Label(root, text="")
label.pack()

# Запускаем цикл обработки событий
root.mainloop()