def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m

    print("Построение префикс-функции:")
    print("P =", pattern)

    for i in range(1, m):
        j = pi[i - 1]

        print()
        print(f"i = {i}, символ P[{i}] = {pattern[i]}")
        print(f"Начальное j = {j}")

        while j > 0 and pattern[i] != pattern[j]:
            print(f"Несовпадение: {pattern[i]} != {pattern[j]}, откат j")
            j = pi[j - 1]
            print(f"Новое j = {j}")

        if pattern[i] == pattern[j]:
            j += 1
            print(f"Совпадение найдено, j = {j}")
        else:
            print("Совпадения нет, j = 0")

        pi[i] = j
        print(f"pi[{i}] = {j}")

    print()
    print("Итоговая префикс-функция:", pi)
    print("-" * 40)

    return pi


def kmp_search(pattern, text):
    m = len(pattern)

    if m == 0:
        return []

    pi = prefix_function(pattern)

    result = []
    j = 0

    print("Поиск шаблона в тексте:")
    print("T =", text)
    print("P =", pattern)
    print("-" * 40)

    for i in range(len(text)):
        print()
        print(f"i = {i}, символ T[{i}] = {text[i]}, текущее j = {j}")

        while j > 0 and text[i] != pattern[j]:
            print(f"Несовпадение: {text[i]} != {pattern[j]}, откат j")
            j = pi[j - 1]
            print(f"Новое j = {j}")

        if text[i] == pattern[j]:
            j += 1
            print(f"Совпадение, j = {j}")
        else:
            print("Совпадения нет, j = 0")

        if j == m:
            start = i - m + 1
            result.append(start)

            print(f"Найдено вхождение с позиции {start}")

            j = pi[j - 1]
            print(f"После нахождения откат j = {j}")

    print()
    print("Поиск завершён")
    print("Найденные позиции:", result if result else "нет")
    print("-" * 40)

    return result


P = input()
T = input()

answer = kmp_search(P, T)

print()
print("Ответ:")

if len(answer) == 0:
    print(-1)
else:
    print(",".join(map(str, answer)))