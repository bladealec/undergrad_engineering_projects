import tkinter as tk
from tkinter import messagebox

def add_task():
    task = task_entry.get()
    if task:
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    try:
        selected_task = task_list.curselection()[0]
        task_list.delete(selected_task)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def clear_tasks():
    task_list.delete(0, tk.END)

def create_todo_app():
    global task_entry, task_list
    
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("300x400")
    
    task_entry = tk.Entry(root, font=("Arial", 14), bd=5)
    task_entry.pack(pady=10)
    
    add_button = tk.Button(root, text="Add Task", font=("Arial", 12), command=add_task)
    add_button.pack(pady=5)
    
    task_list = tk.Listbox(root, font=("Arial", 12), width=30, height=10)
    task_list.pack(pady=10)
    
    remove_button = tk.Button(root, text="Remove Task", font=("Arial", 12), command=remove_task)
    remove_button.pack(pady=5)
    
    clear_button = tk.Button(root, text="Clear All", font=("Arial", 12), command=clear_tasks)
    clear_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_todo_app()
