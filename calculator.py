import tkinter as tk
from tkinter import messagebox

def on_click(button_text):
    if button_text == "C":
        entry_var.set("")
    elif button_text == ("="):
        try:
            result = eval(entry_var.get())
            entry_var.set(result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
    else:
        entry_var.set(entry_var.get() + button_text)

def create_calculator():
    global entry_var
    root = tk.Tk()
    root.title("Calculator")
    root.geometry("300x400")
    entry_var = tk.StringVar()
    
    entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 20), bd=10, relief=tk.GROOVE, justify="right")
    entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8)
    
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('C', '0', '=', '+')
    ]
    
    for i, row in enumerate(buttons):
        for j, button_text in enumerate(row):
            button = tk.Button(root, text=button_text, font=("Arial", 18), padx=20, pady=20, 
                               command=lambda text=button_text: on_click(text))
            button.grid(row=i + 1, column=j, sticky="nsew")
    
    root.mainloop()

if __name__ == "__main__":
    create_calculator()
