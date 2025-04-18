import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gauss_seidel(A, b, eps=1e-5, max_iterations=1000):
    n = len(A)
    x = np.zeros(n)
    errors = []

    for iteration in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            if A[i][i] == 0:
                raise ValueError(f"Нульовий елемент на діагоналі в рядку {i + 1}")
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        error = np.linalg.norm(x_new - x, ord=np.inf)
        errors.append(error)

        if error < eps:
            return [round(val, 6) for val in x_new], iteration + 1, errors

        x = x_new

    raise Exception("Метод не збігся — перевищено максимальну кількість ітерацій.")

def plot_convergence(errors):
    fig = plt.Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(errors, marker='o', color='blue')
    ax.set_title("Збіжність методу")
    ax.set_xlabel("Ітерація")
    ax.set_ylabel("Похибка")
    ax.grid(True)
    return fig

def solve():
    try:
        A = []
        for i in range(3):
            row = []
            for j in range(3):
                val = float(entries[i][j].get())
                row.append(val)
            A.append(row)

        b = [float(free_entries[i].get()) for i in range(3)]

        result, iterations, errors = gauss_seidel(A, b)

        for i, val in enumerate(result):
            result_labels[i].config(text=f"x{i+1} = {val}")

        iter_label.config(text=f"Кількість ітерацій: {iterations}")

        for widget in plot_frame.winfo_children():
            widget.destroy()

        fig = plot_convergence(errors)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Помилка", str(e))


# ---------- Інтерфейс ----------
root = tk.Tk()
root.title("Метод Гауса-Зейделя — Варіант 4")
root.geometry("700x650")
root.configure(bg="#f5f5f5", padx=20, pady=20)

input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Матриця коефіцієнтів A і вектор B:", font=("Arial", 12, "bold"), bg="#f5f5f5").grid(row=0, column=0, columnspan=4, pady=(0, 10))

entries = []
free_entries = []
default_A = [
    [1, 1, 1],
    [2, 3, 1],
    [1, -1, -1]
]
default_b = [4, 9, -2]

for i in range(3):
    row_entries = []
    for j in range(3):
        entry = tk.Entry(input_frame, width=6, font=("Courier", 11), justify="center")
        entry.grid(row=i+1, column=j, padx=4, pady=2)
        entry.insert(0, str(default_A[i][j]))
        row_entries.append(entry)
    entries.append(row_entries)

    b_entry = tk.Entry(input_frame, width=6, font=("Courier", 11), justify="center")
    b_entry.grid(row=i+1, column=3, padx=10)
    b_entry.insert(0, str(default_b[i]))
    free_entries.append(b_entry)

for j, text in enumerate(["a₁", "a₂", "a₃", "b"]):
    tk.Label(input_frame, text=text, font=("Arial", 10, "bold"), bg="#f5f5f5").grid(row=0, column=j)

tk.Button(root, text="Розв’язати", command=solve, font=("Arial", 12, "bold"), bg="#90ee90", width=20).pack(pady=15)

result_frame = tk.Frame(root, bg="#f5f5f5")
result_frame.pack(pady=5)

result_labels = []
for i in range(3):
    lbl = tk.Label(result_frame, text=f"x{i+1} =", font=("Arial", 11), bg="#f5f5f5")
    lbl.pack()
    result_labels.append(lbl)

iter_label = tk.Label(result_frame, text="", font=("Arial", 11, "italic"), bg="#f5f5f5", pady=5)
iter_label.pack()

plot_frame = tk.Frame(root, bg="#f5f5f5")
plot_frame.pack(pady=10)

root.mainloop()
