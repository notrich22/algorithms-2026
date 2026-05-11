def show(s):
    return s if s else '""'


def build_dp(a, b, replace_cost, insert_cost, delete_cost):
    n = len(a)
    m = len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    print("=== ВХОДНЫЕ ДАННЫЕ ===")
    print("A =", show(a))
    print("B =", show(b))
    print("replace =", replace_cost)
    print("insert  =", insert_cost)
    print("delete  =", delete_cost)

    print("\n=== ТАБЛИЦА DP ===")
    print("dp[i][j] = минимальная стоимость превращения A[:i] в B[:j]")

    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + delete_cost

    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + insert_cost

    print("\nНачальная строка:")
    print("A[:0] =", show(""))
    print("dp[0] =", dp[0])

    for i in range(1, n + 1):
        print(f"\nОбрабатываем A[:{i}] = {show(a[:i])}")

        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
                op = "M"
            else:
                cost = replace_cost
                op = "R"

            delete_value = dp[i - 1][j] + delete_cost
            insert_value = dp[i][j - 1] + insert_cost
            change_value = dp[i - 1][j - 1] + cost

            dp[i][j] = min(delete_value, insert_value, change_value)

            print(
                f"dp[{i}][{j}] ({show(a[:i])} -> {show(b[:j])}): "
                f"D={delete_value}, I={insert_value}, {op}={change_value} => {dp[i][j]}"
            )

        print("Готовая строка:")
        print(f"dp[{i}] =", dp[i])

    return dp


def restore_operations(dp, a, b, replace_cost, insert_cost, delete_cost):
    i = len(a)
    j = len(b)
    operations = []

    print("\n=== ВОССТАНОВЛЕНИЕ ОПЕРАЦИЙ ===")
    while i > 0 or j > 0:
        print(f"\nПозиция: i={i}, j={j}, значение={dp[i][j]}")

        if j > 0 and dp[i][j] == dp[i][j - 1] + insert_cost:
            operations.append("I")
            print("Берём I: вставка символа из B")
            j -= 1

        elif i > 0 and j > 0:
            if a[i - 1] == b[j - 1]:
                cost = 0
                operation = "M"
            else:
                cost = replace_cost
                operation = "R"

            if dp[i][j] == dp[i - 1][j - 1] + cost:
                operations.append(operation)
                print(f"Берём {operation}: A[{i - 1}]='{a[i - 1]}', B[{j - 1}]='{b[j - 1]}'")
                i -= 1
                j -= 1
            else:
                operations.append("D")
                print(f"Берём D: удаление A[{i - 1}]='{a[i - 1]}'")
                i -= 1

        else:
            operations.append("D")
            print(f"Берём D: удаление A[{i - 1}]='{a[i - 1]}'")
            i -= 1

    operations.reverse()

    print("\nОперации:")
    print("".join(operations))

    return operations


replace_cost, insert_cost, delete_cost = map(int, input().split())
a = input()
b = input()

dp = build_dp(a, b, replace_cost, insert_cost, delete_cost)
operations = restore_operations(dp, a, b, replace_cost, insert_cost, delete_cost)

print("\n=== РЕЗУЛЬТАТ ===")
print("".join(operations))
print(a)
print(b)