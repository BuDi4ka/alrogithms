import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Обчислення коефіцієнтів Ньютона
def newton_coefficients(x, y):
    n = len(x)
    coef = np.copy(y).astype(float)

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    
    return coef

# Обчислення значення полінома Ньютона у точці x
def newton_interpolation(x_data, coefficients, x):
    n = len(coefficients)
    result = coefficients[-1]

    for i in range(n - 2, -1, -1):
        result = result * (x - x_data[i]) + coefficients[i]

    return result

# Основна функція для інтерполяції
def function_f(x):
    return 10 * np.log(2 * x) / (1 + x)

# Тестова функція (sin(x))
def function_test(x):
    return np.sin(x)

# Оцінка похибки
def calculate_error(x_vals, y_vals, degree, func):
    subset_x = x_vals[:degree+1]
    subset_y = y_vals[:degree+1]
    coef = newton_coefficients(subset_x, subset_y)

    x_dense = np.linspace(x_vals[0], x_vals[-1], 100)
    y_real = func(x_dense)
    y_interp = np.array([newton_interpolation(subset_x, coef, x) for x in x_dense])
    
    return x_dense, np.abs(y_real - y_interp)

# Головний клас
class NewtonInterpolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Інтерполяція Ньютона")
        self.root.geometry("500x450")

        # Кнопки
        ttk.Button(root, text="Інтерполяція заданої функції", command=self.plot_interpolation).place(x=130, y=30)
        ttk.Button(root, text="Тестова інтерполяція sin(x)", command=self.plot_test_interpolation).place(x=125, y=80)
        ttk.Button(root, text="Аналіз похибки", command=self.plot_error).place(x=180, y=130)
        ttk.Button(root, text="Показати таблицю похибок", command=self.show_error_table).place(x=130, y=180)

        # Параметри для основної функції
        self.a, self.b = 1, 5
        self.x_vals = np.linspace(self.a, self.b, 11)
        self.y_vals = function_f(self.x_vals)
        self.coefficients = newton_coefficients(self.x_vals, self.y_vals)

        # Параметри для тестової функції
        self.a_test, self.b_test = 0, np.pi
        self.x_test_vals = np.linspace(self.a_test, self.b_test, 11)
        self.y_test_vals = function_test(self.x_test_vals)
        self.test_coefficients = newton_coefficients(self.x_test_vals, self.y_test_vals)

    def plot_interpolation(self):
        x_dense = np.linspace(self.a, self.b, 100)
        y_real = function_f(x_dense)
        y_interp = [newton_interpolation(self.x_vals, self.coefficients, x) for x in x_dense]

        plt.figure(figsize=(8, 5))
        plt.plot(x_dense, y_real, 'g--', label="Оригінальна функція")
        plt.plot(x_dense, y_interp, 'b-', label="Інтерполяція Ньютона")
        plt.scatter(self.x_vals, self.y_vals, color='red', label="Вузли інтерполяції")
        plt.legend()
        plt.title("Інтерполяція функції")
        plt.show()

    def plot_test_interpolation(self):
        x_dense = np.linspace(self.a_test, self.b_test, 100)
        y_real = function_test(x_dense)
        y_interp = [newton_interpolation(self.x_test_vals, self.test_coefficients, x) for x in x_dense]

        plt.figure(figsize=(8, 5))
        plt.plot(x_dense, y_real, 'g--', label="Оригінальна sin(x)")
        plt.plot(x_dense, y_interp, 'b-', label="Інтерполяція Ньютона")
        plt.scatter(self.x_test_vals, self.y_test_vals, color='red', label="Вузли інтерполяції")
        plt.legend()
        plt.title("Інтерполяція sin(x)")
        plt.show()

    def plot_error(self):
        degrees = [2, 4, 6, 10]
        plt.figure(figsize=(8, 5))

        for d in degrees:
            x_err, err = calculate_error(self.x_vals, self.y_vals, d, function_f)
            plt.plot(x_err, err, label=f"Похибка для степеня {d}")

        plt.legend()
        plt.title("Оцінка похибки (задана функція)")
        plt.show()

    def show_error_table(self):
        # Вікно з таблицею похибок
        table_window = tk.Toplevel(self.root)
        table_window.title("Таблиця похибок")
        table_window.geometry("650x400")

        columns = ("№", "X", "Похибка (n=2)", "Похибка (n=4)", "Похибка (n=6)", "Похибка (n=10)")
        tree = ttk.Treeview(table_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Обчислення похибок
        for i, x in enumerate(np.linspace(self.a, self.b, 10)):
            errors = []
            for degree in [2, 4, 6, 10]:
                _, err = calculate_error(self.x_vals, self.y_vals, degree, function_f)
                errors.append(err[i])

            tree.insert("", tk.END, values=(i+1, f"{x:.3f}", f"{errors[0]:.5f}", f"{errors[1]:.5f}", f"{errors[2]:.5f}", f"{errors[3]:.5f}"))

        tree.pack(expand=True, fill="both")

# Запуск GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = NewtonInterpolationApp(root)
    root.mainloop()
