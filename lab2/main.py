import time
import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


def boz_nelson_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = boz_nelson_sort(arr[:mid])
    right = boz_nelson_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def measure_time(sort_function, arr):
    start_time = time.perf_counter()
    sort_function(arr)
    end_time = time.perf_counter()
    return end_time - start_time


def generate_test_data(sizes):
    return [random.choices(range(1, 10000), k=size) for size in sizes]


def run_sort():
    input_data = entry.get()
    try:
        arr = list(map(int, input_data.split()))
        sorted_arr = boz_nelson_sort(arr)
        result_label.config(text=f"Відсортований масив: {sorted_arr}")
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний ввід даних")


def load_from_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            with open(filename, 'r') as file:
                arr = list(map(int, file.read().split()))
            sorted_arr = boz_nelson_sort(arr)
            result_label.config(text=f"Відсортований масив: {sorted_arr}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при зчитуванні файлу: {e}")


def plot_graph():
    sizes = [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 7000, 10000]
    test_data = generate_test_data(sizes)
    time_results = [measure_time(boz_nelson_sort, arr) for arr in test_data]
    theoretical_complexity = [size * np.log2(size) for size in sizes]

    plt.figure(figsize=(10, 5))
    plt.plot(sizes, time_results, marker='o', label='Час виконання')
    plt.plot(sizes, np.array(theoretical_complexity) / max(theoretical_complexity) * max(time_results), '--',
             label='Теоретична складність')
    plt.xlabel('Розмір масиву')
    plt.ylabel('Час (секунди)')
    plt.title('Порівняння часової складності та теоретичної складності')
    plt.legend()
    plt.grid()
    plt.show()


# Створення GUI
root = tk.Tk()
root.title("Сортування Боуза-Нельсона")
root.geometry("600x400")

tk.Label(root, text="Введіть масив чисел (через пробіл):").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

sort_button = tk.Button(root, text="Відсортувати", command=run_sort)
sort_button.pack(pady=5)

file_button = tk.Button(root, text="Завантажити з файлу", command=load_from_file)
file_button.pack(pady=5)

graph_button = tk.Button(root, text="Побудувати графік", command=plot_graph)
graph_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()