import tkinter as tk
import time
import random
import math
import matplotlib.pyplot as plt
import tkinter.filedialog as fd


def bose_nelson_sort(arr):
    ops = 0  # Лічильник операцій

    def merge(j, r, m):
        nonlocal ops
        if j + r < len(arr):
            ops += 1
            if m == 1:
                ops += 1
                if arr[j] > arr[j + r]:
                    arr[j], arr[j + r] = arr[j + r], arr[j]
                    ops += 1
            else:
                m = m // 2
                ops += 1
                merge(j, r, m)
                if j + r + m < len(arr):
                    merge(j + m, r, m)
                merge(j + m, r - m, m)

    m = 1
    while m < len(arr):
        j = 0
        while j + m < len(arr):
            merge(j, m, m)
            j += 2 * m
            ops += 1
        m *= 2
        ops += 1

    return ops


def run_experiment():
    arr_sizes = [1000 * i for i in range(1, 11)]
    times_measured = []
    ops_measured = []

    for size in arr_sizes:
        arr = [random.randint(0, 100000) for _ in range(size)]
        arr_copy = arr[:]
        start_time = time.perf_counter()
        ops = bose_nelson_sort(arr_copy)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        times_measured.append(elapsed)
        ops_measured.append(ops)
        print(f"Розмір: {size:5d} елементів, час: {elapsed:.6f} сек, операцій: {ops}")

    theory = [size * math.log(size) for size in arr_sizes]
    max_theory = max(theory)
    max_time = max(times_measured)
    max_ops = max(ops_measured)

    theory_time = [val / max_theory * max_time for val in theory]
    theory_ops = [val / max_theory * max_ops for val in theory]

    plt.figure("Час сортування")
    plt.plot(arr_sizes, times_measured, label="Експериментальний час", marker='o')
    plt.plot(arr_sizes, theory_time, label="Теоретична O(n log n) (масштабована)", marker='x')
    plt.xlabel("Розмір масиву")
    plt.ylabel("Час (сек)")
    plt.title("Залежність часу сортування від розміру масиву")
    plt.legend()
    plt.grid(True)

    plt.figure("Кількість операцій")
    plt.plot(arr_sizes, ops_measured, label="Експериментальна кількість операцій", marker='o')
    plt.plot(arr_sizes, theory_ops, label="Теоретична O(n log n) (масштабована)", marker='x')
    plt.xlabel("Розмір масиву")
    plt.ylabel("Кількість операцій")
    plt.title("Залежність кількості операцій від розміру масиву")
    plt.legend()
    plt.grid(True)

    plt.show()


def get_array_from_keyboard():
    try:
        user_input = entry_input.get()
        arr = list(map(int, user_input.split()))
        output_label.config(text=f"Введений масив: {arr}")
        sorted_arr = arr[:]
        bose_nelson_sort(sorted_arr)
        output_label.config(text=f"Відсортований масив: {sorted_arr}")
    except ValueError:
        output_label.config(text="Некоректний ввід! Введіть числа через пробіл.")


def get_array_from_file():
    file_path = fd.askopenfilename(filetypes=[("Текстові файли", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                arr = list(map(int, file.read().split()))
            output_label.config(text=f"Завантажений масив: {arr}")
            sorted_arr = arr[:]
            bose_nelson_sort(sorted_arr)
            output_label.config(text=f"Відсортований масив: {sorted_arr}")
        except ValueError:
            output_label.config(text="Файл містить некоректні дані!")


# GUI
root = tk.Tk()
root.title("Сортування Бозе-Нельсона")

tk.Label(root, text="Лабораторна робота: Сортування Бозе-Нельсона", font=("Arial", 14)).pack(pady=10)

tk.Label(root, text="Введіть масив чисел через пробіл:").pack()
entry_input = tk.Entry(root, width=50)
entry_input.pack()

tk.Button(root, text="Ввести масив вручну", command=get_array_from_keyboard).pack(pady=5)
tk.Button(root, text="Завантажити масив з файлу", command=get_array_from_file).pack(pady=5)
tk.Button(root, text="Запустити експеримент", command=run_experiment).pack(pady=10)

output_label = tk.Label(root, text="")
output_label.pack(pady=10)

root.mainloop()
