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