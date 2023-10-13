import sqlite3
import tkinter as tk
from tkinter import ttk

# Создаем базу данных и таблицу, если их еще нет
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()
conn.close()

def add_employee():
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    salary = entry_salary.get()

    if full_name and phone_number and email and salary:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                       (full_name, phone_number, email, salary))
        conn.commit()
        conn.close()

        clear_entries()
        display_records()
    else:
        error_label.config(text="Заполните все поля!")

def update_employee():
    item_id = entry_id.get()
    updated_full_name = entry_full_name.get()
    updated_phone_number = entry_phone_number.get()
    updated_email = entry_email.get()
    updated_salary = entry_salary.get()

    if item_id and updated_full_name and updated_phone_number and updated_email and updated_salary:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?",
                       (updated_full_name, updated_phone_number, updated_email, updated_salary, item_id))
        conn.commit()
        conn.close()

        clear_entries()
        display_records()
    else:
        error_label.config(text="Заполните все поля для обновления")

def delete_employee():
    item_id = entry_id.get()

    if item_id:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (item_id,))
        conn.commit()
        conn.close()

        clear_entries()
        display_records()
    else:
        error_label.config(text="Введите ID сотрудника для удаления")

def search_employee():
    search_term = search_entry.get()
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE full_name LIKE ?", ('%' + search_term + '%',))
    records = cursor.fetchall()
    conn.close()

    for record in tree.get_children():
        tree.delete(record)

    for row in records:
        tree.insert("", "end", values=row)

def clear_entries():
    entry_full_name.delete(0, "end")
    entry_phone_number.delete(0, "end")
    entry_email.delete(0, "end")
    entry_salary.delete(0, "end")

def display_records():
    for record in tree.get_children():
        tree.delete(record)

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()

    for row in records:
        tree.insert("", "end", values=row)

    conn.close()


def refresh_records():
    clear_entries()
    display_records()

root = tk.Tk()
root.title("Список сотрудников компании")

# Создаем и размещаем виджеты на форме
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(frame, text="ID сотрудника:").grid(row=0, column=0, padx=5, pady=5)
entry_id = ttk.Entry(frame)
entry_id.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="ФИО:").grid(row=1, column=0, padx=5, pady=5)
entry_full_name = ttk.Entry(frame)
entry_full_name.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Номер телефона:").grid(row=2, column=0, padx=5, pady=5)
entry_phone_number = ttk.Entry(frame)
entry_phone_number.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
entry_email = ttk.Entry(frame)
entry_email.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="Заработная плата:").grid(row=4, column=0, padx=5, pady=5)
entry_salary = ttk.Entry(frame)
entry_salary.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(frame, text="Добавить", command=add_employee).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
ttk.Button(frame, text="Изменить", command=update_employee).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
ttk.Button(frame, text="Удалить", command=delete_employee).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

search_frame = ttk.Frame(root)
search_frame.grid(row=1, column=0, padx=10, pady=10)

ttk.Label(search_frame, text="Поиск по ФИО:").grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(search_frame, text="Поиск", command=search_employee).grid(row=0, column=2, padx=5, pady=5)

tree = ttk.Treeview(root, columns=("ID", "ФИО", "Номер телефона", "Email", "Заработная плата"), show="headings")
tree.heading("ID", text="ID")
tree.heading("ФИО", text="ФИО")
tree.heading("Номер телефона", text="Номер телефона")
tree.heading("Email", text="Email")
tree.heading("Заработная плата", text="Заработная плата")
tree.grid(row=2, column=0, padx=10, pady=10)

display_records()

error_label = ttk.Label(root, text="", foreground="red")
error_label.grid(row=3, column=0, padx=10, pady=10)

refresh_button = ttk.Button(root, text="Обновить", command=refresh_records)
refresh_button.grid(row=4, column=0, padx=10, pady=10)



root.mainloop()
