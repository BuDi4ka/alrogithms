import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Функція для розв'язання системи рівнянь методом Гауса-Зейделя
def gauss_seidel(A, b, epsilon, max_iter):
    n = len(A)
    x = [0.0] * n  # Початкові значення розв'язків
    iterations = 0
    convergence = []  # Список для збереження значень для графіку збіжності
    
    for k in range(max_iter):
        x_new = x[:]
        for i in range(n):
            sum1 = sum(A[i][j] * x_new[j] for j in range(i))  # Від суми лівої частини
            sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))  # Від суми правої частини
            x_new[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        # Оцінка збіжності (зберігаємо різницю для побудови графіка)
        diff = max(abs(x_new[i] - x[i]) for i in range(n))
        convergence.append(diff)

        # Перевірка на точність
        if diff < epsilon:
            return x_new, k + 1, convergence  # Повертаємо розв'язок, кількість ітерацій і графік
        x = x_new
        iterations += 1

    return x, max_iter, convergence  # Якщо кількість ітерацій досягла max_iter

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
        result, iterations, convergence = gauss_seidel(A, b, epsilon, max_iter)
        
        # Виведення результату
        result_label.config(text=f"Розв'язок: x1 = {result[0]}, x2 = {result[1]}, x3 = {result[2]}")
        iterations_label.config(text=f"Кількість ітерацій: {iterations}")
        
        # Побудова графіка збіжності
        plt.figure()
        plt.plot(range(1, iterations + 1), convergence, marker='o')
        plt.title('Графік збіжності методу Гауса-Зейделя')
        plt.xlabel('Ітерація')
        plt.ylabel('Максимальна різниця між наближеннями')
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

# Створення вікна
root = tk.Tk()
root.title("Метод Гауса-Зейделя")

# Параметри GUI
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Ввід матриці коефіцієнтів (за замовчуванням згідно з вашим варіантом)
tk.Label(frame, text="Введіть матрицю коефіцієнтів (3x3):").grid(row=0, columnspan=2)
matrix_entries = []
default_matrix = ["1 1 1", "2 3 1", "1 -1 -1"]  # Дефолтні дані згідно з варіантом
for i in range(3):
    tk.Label(frame, text=f"Рядок {i+1}:").grid(row=i+1, column=0)
    entry = tk.Entry(frame, width=20)
    entry.grid(row=i+1, column=1)
    entry.insert(0, default_matrix[i])  # Встановлюємо дефолтне значення
    matrix_entries.append(entry)

# Ввід вектора вільних членів (за замовчуванням)
tk.Label(frame, text="Введіть вектор вільних членів:").grid(row=4, columnspan=2)
b_entries = []
default_b = ["4", "9", "-2"]  # Дефолтні значення для вектора вільних членів
for i in range(3):
    tk.Label(frame, text=f"b{i+1}:").grid(row=i+5, column=0)
    entry = tk.Entry(frame, width=20)
    entry.grid(row=i+5, column=1)
    entry.insert(0, default_b[i])  # Встановлюємо дефолтне значення
    b_entries.append(entry)

# Ввід параметрів похибки та кількості ітерацій
tk.Label(frame, text="Параметри:").grid(row=8, columnspan=2)

tk.Label(frame, text="Похибка (ε):").grid(row=9, column=0)
epsilon_entry = tk.Entry(frame, width=20)
epsilon_entry.grid(row=9, column=1)
epsilon_entry.insert(0, "0.0001")  # Дефолтне значення для похибки

tk.Label(frame, text="Макс. ітерацій:").grid(row=10, column=0)
iterations_entry = tk.Entry(frame, width=20)
iterations_entry.grid(row=10, column=1)
iterations_entry.insert(0, "100")  # Дефолтне значення для кількості ітерацій

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
