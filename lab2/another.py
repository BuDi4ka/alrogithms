def bose_nelson_sort(arr):
    ops = 0  # Лічильник операцій
    m = 1

    while m < len(arr):
        j = 0
        while j + m < len(arr):
            r, sub_m = m, m
            stack = [(j, r, sub_m)]

            while stack:
                j, r, sub_m = stack.pop()
                if j + r < len(arr):
                    ops += 1
                    if sub_m == 1:
                        ops += 1
                        if arr[j] > arr[j + r]:
                            arr[j], arr[j + r] = arr[j + r], arr[j]
                            ops += 1
                    else:
                        sub_m //= 2
                        ops += 1
                        stack.append((j + sub_m, r - sub_m, sub_m))
                        if j + r + sub_m < len(arr):
                            stack.append((j + sub_m, r, sub_m))
                        stack.append((j, r, sub_m))

            j += 2 * m
            ops += 1

        m *= 2
        ops += 1

    return ops