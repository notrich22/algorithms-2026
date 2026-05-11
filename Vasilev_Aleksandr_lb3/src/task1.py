def show(s):
    return s if s else '""'


def min_edit_cost(a, b, replace_cost, insert_cost, delete_cost):
    n = len(a)
    m = len(b)

    print("=== ВХОДНЫЕ ДАННЫЕ ===")
    print("A =", show(a))
    print("B =", show(b))
    print("replace =", replace_cost)
    print("insert  =", insert_cost)
    print("delete  =", delete_cost)

    dp = [j * insert_cost for j in range(m + 1)]

    print("\n=== НАЧАЛЬНАЯ СТРОКА ===")
    print("dp =", dp)

    print("\n=== ЗАПОЛНЕНИЕ ===")

    for i in range(1, n + 1):
        new_dp = [0] * (m + 1)
        new_dp[0] = i * delete_cost

        print(f"\nОбрабатываем A[:{i}] = {show(a[:i])}")
        print(f"Первый элемент new_dp[0] = {i} * delete = {new_dp[0]}")

        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
                operation = "match"
            else:
                cost = replace_cost
                operation = "replace"

            delete_value = dp[j] + delete_cost
            insert_value = new_dp[j - 1] + insert_cost
            replace_value = dp[j - 1] + cost

            new_dp[j] = min(
                delete_value,
                insert_value,
                replace_value
            )

            print(
                f"A[:{i}] -> B[:{j}] | "
                f"'{a[i - 1]}' и '{b[j - 1]}': {operation}; "
                f"delete={delete_value}, "
                f"insert={insert_value}, "
                f"{operation}={replace_value}; "
                f"dp={new_dp[j]}"
            )

        dp = new_dp

        print("Готовая строка DP:")
        print("dp =", dp)

    print("Ответ:", dp[m])

    return dp[m]


replace_cost, insert_cost, delete_cost = map(int, input().split())
a = input()
b = input()

min_edit_cost(a, b, replace_cost, insert_cost, delete_cost)