import math
import tkinter as tk
from tkinter import messagebox, filedialog


def linear_algorithm(a, b, c, d):
    if d == 0:
        raise ValueError("d не може бути нулем")
    return (a / d) ** 2 + (b / d) ** 3 + (c / 2) ** 4


def branching_algorithm(f, d, l, k, w):
    if f == 0:
        return math.log10(l * k) + d * math.sin(w * k)
    else:
        return math.cos(w * k) + math.log10(l * k)


def cyclic_algorithm(b):
    results = []
    for a in range(-4, 19, 1):
        f = math.sqrt(a ** 2 + b ** 2) - (a + b) ** 2
        results.append(f"a = {a}, f = {f}")
    return "\n".join(results)


def load_from_file(entry_fields):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, entry in enumerate(entry_fields):
                entry.delete(0, tk.END)
                entry.insert(0, lines[i].strip())


def run_algorithm(choice, entries, output_text):
    try:
        values = [float(entry.get()) for entry in entries]
        if choice == "Лінійний алгоритм":
            if values[3] == 0:
                raise ValueError("d не може бути нулем")
            result = linear_algorithm(*values)
        elif choice == "Розгалужений алгоритм":
            if values[2] == 0:
                raise ValueError("l не може бути нулем")
            result = branching_algorithm(int(values[0]), *values[1:])
        elif choice == "Циклічний алгоритм":
            result = cyclic_algorithm(values[0])
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Результат:\n{result}")
    except ValueError as e:
        messagebox.showerror("Помилка", str(e))


def update_fields(choice, entry_fields, labels_frame):
    for widget in labels_frame.winfo_children():
        widget.destroy()
    entry_fields.clear()

    if choice == "Лінійний алгоритм":
        fields = ["a", "b", "c", "d"]
    elif choice == "Розгалужений алгоритм":
        fields = ["f", "d", "l", "k", "w"]
    elif choice == "Циклічний алгоритм":
        fields = ["b"]

    for label in fields:
        frame = tk.Frame(labels_frame)
        frame.pack()
        tk.Label(frame, text=label).pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.RIGHT)
        entry_fields.append(entry)


def create_gui():
    root = tk.Tk()
    root.title("Алгоритмічні обчислення")

    tk.Label(root, text="Виберіть алгоритм:").pack()
    choice_var = tk.StringVar(value="Лінійний алгоритм")
    choices = ["Лінійний алгоритм", "Розгалужений алгоритм", "Циклічний алгоритм"]
    choice_menu = tk.OptionMenu(root, choice_var, *choices)
    choice_menu.pack()

    entry_fields = []
    labels_frame = tk.Frame(root)
    labels_frame.pack()

    update_fields(choice_var.get(), entry_fields, labels_frame)
    choice_var.trace("w", lambda *args: update_fields(choice_var.get(), entry_fields, labels_frame))

    output_text = tk.Text(root, height=10, width=50)
    output_text.pack()

    tk.Button(root, text="Запустити", command=lambda: run_algorithm(choice_var.get(), entry_fields, output_text)).pack()
    tk.Button(root, text="Завантажити з файлу", command=lambda: load_from_file(entry_fields)).pack()
    tk.Button(root, text="Вихід", command=root.quit).pack()

    root.mainloop()


if __name__ == "__main__":
    create_gui()