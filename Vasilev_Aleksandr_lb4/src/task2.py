def prefix_function(pattern):
    n = len(pattern)
    pi = [0] * n

    print("Построение префикс-функции")
    print(f"Шаблон B: {pattern}")
    print(f"Начальное pi: {pi}")

    for i in range(1, n):
        j = pi[i - 1]

        print()
        print(f"i = {i}, B[{i}] = '{pattern[i]}', начальное j = {j}")

        while j > 0 and pattern[i] != pattern[j]:
            print(f"  несовпадение: B[{i}] = '{pattern[i]}' != B[{j}] = '{pattern[j]}'")
            j = pi[j - 1]
            print(f"  откат: j = {j}")

        if pattern[i] == pattern[j]:
            j += 1
            print(f"  совпадение, новое j = {j}")
        else:
            print("  совпадения нет, j = 0")

        pi[i] = j
        print(f"  pi[{i}] = {j}")

    print()
    print(f"Итоговая префикс-функция: {pi}")
    print("-" * 50)

    return pi


def find_cyclic_shift(a, b):
    n = len(a)

    print("Проверка циклического сдвига")
    print(f"A = {a}")
    print(f"B = {b}")
    print(f"len(A) = {len(a)}, len(B) = {len(b)}")
    print("-" * 50)

    if len(b) != n:
        print("Длины строк различаются")
        return -1

    if n == 0:
        print("Обе строки пустые")
        return 0

    pi = prefix_function(b)
    j = 0

    print("Поиск B в виртуальной строке A + A")
    print("Проход выполняется по A и затем по началу A")
    print("-" * 50)

    for i in range(n):
        c = a[i]

        print(f"pos = {i}, A[{i}] = '{c}', j = {j}")

        while j > 0 and c != b[j]:
            print(f"  несовпадение: '{c}' != B[{j}] = '{b[j]}'")
            j = pi[j - 1]
            print(f"  откат: j = {j}")

        if c == b[j]:
            j += 1
            print(f"  совпадение, j = {j}")
        else:
            print("  совпадения нет, j = 0")

        if j == n:
            start = i - n + 1
            print(f"  найдено полное вхождение, start = {start}")
            return start

    for i in range(n - 1):
        c = a[i]
        pos = n + i

        print(f"pos = {pos}, A[{i}] = '{c}', j = {j}")

        while j > 0 and c != b[j]:
            print(f"  несовпадение: '{c}' != B[{j}] = '{b[j]}'")
            j = pi[j - 1]
            print(f"  откат: j = {j}")

        if c == b[j]:
            j += 1
            print(f"  совпадение, j = {j}")
        else:
            print("  совпадения нет, j = 0")

        if j == n:
            start = i + 1
            print(f"  найдено полное вхождение, start = {start}")
            return start

    print("Полное вхождение не найдено")
    return -1


a = input()
b = input()

answer = find_cyclic_shift(a, b)

print()
print("Ответ:")
print(answer)