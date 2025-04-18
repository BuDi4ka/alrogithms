import tkinter as tk
from tkinter import messagebox

# Функція для розв'язання системи рівнянь методом Гауса-Зейделя
def gauss_seidel(A, b, epsilon, max_iter):
    n = len(A)
    x = [0.0] * n  # Початкові значення розв'язків
    for k in range(max_iter):
        x_new = x[:]
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # Від суми лівої частини
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # Від суми правої частини
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        # Перевірка на точність
        if all(abs(x_new[i] - x[i]) < epsilon for i in range(n)):
            return x_new, k + 1  # Повертаємо розв'язок і кількість ітерацій
        x = x_new
    return x, max_iter  # Якщо кількість ітерацій досягла max_iter

# Функція для обробки введених значень
def solve_system():
    try:
        # Зчитуємо введені значення
        epsilon = float(epsilon_entry.get())
        max_iter = int(iterations_entry.get())
        A = []
        b = []
        
        # Вводимо матрицю коефіцієнтів
        for i in range(3):
            row = list(map(float, matrix_entries[i].get().split()))
            A.append(row)
        
        # Вводимо вектор вільних членів
        for i in range(3):
            b.append(float(b_entries[i].get()))
        
        # Перевірка на правильність введених значень
        if len(A) != 3 or len(A[0]) != 3 or len(b) != 3:
            raise ValueError("Матриця має бути 3x3 і вектор вільних членів має бути довжини 3.")

        # Викликаємо метод Гауса-Зейделя
        result, iterations = gauss_seidel(A, b, epsilon, max_iter)
        
        # Виведення результату
        result_label.config(text=f"Розв'язок: x1 = {result[0]}, x2 = {result[1]}, x3 = {result[2]}")
        iterations_label.config(text=f"Кількість ітерацій: {iterations}")
    
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

# Створення вікна
root = tk.Tk()
root.title("Метод Гауса-Зейделя")

# Параметри GUI
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Ввід матриці коефіцієнтів
tk.Label(frame, text="Введіть матрицю коефіцієнтів (3x3):").grid(row=0, columnspan=2)
matrix_entries = []
for i in range(3):
    tk.Label(frame, text=f"Рядок {i+1}:").grid(row=i+1, column=0)
    entry = tk.Entry(frame, width=20)
    entry.grid(row=i+1, column=1)
    matrix_entries.append(entry)

# Ввід вектора вільних членів
tk.Label(frame, text="Введіть вектор вільних членів:").grid(row=4, columnspan=2)
b_entries = []
for i in range(3):
    tk.Label(frame, text=f"b{i+1}:").grid(row=i+5, column=0)
    entry = tk.Entry(frame, width=20)
    entry.grid(row=i+5, column=1)
    b_entries.append(entry)

# Ввід параметрів похибки та кількості ітерацій
tk.Label(frame, text="Параметри:").grid(row=8, columnspan=2)

tk.Label(frame, text="Похибка (ε):").grid(row=9, column=0)
epsilon_entry = tk.Entry(frame, width=20)
epsilon_entry.grid(row=9, column=1)

tk.Label(frame, text="Макс. ітерацій:").grid(row=10, column=0)
iterations_entry = tk.Entry(frame, width=20)
iterations_entry.grid(row=10, column=1)

# Кнопка для запуску розв'язку
solve_button = tk.Button(frame, text="Розв'язати", command=solve_system)
solve_button.grid(row=11, columnspan=2)

# Місце для результатів
result_label = tk.Label(frame, text="Розв'язок:")
result_label.grid(row=12, columnspan=2)

iterations_label = tk.Label(frame, text="Кількість ітерацій:")
iterations_label.grid(row=13, columnspan=2)

# Запуск GUI
root.mainloop()
