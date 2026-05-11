def show(s):
    return s if s else '""'


def levenshtein(a, b):
    n = len(a)
    m = len(b)

    print("=== ВХОДНЫЕ ДАННЫЕ ===")
    print("A =", show(a))
    print("B =", show(b))

    dp = list(range(m + 1))

    print("\n=== НАЧАЛЬНОЕ СОСТОЯНИЕ ===")
    print("A[:0] =", show(""))
    print("dp =", dp)

    print("\n=== ЗАПОЛНЕНИЕ ===")

    for i in range(1, n + 1):
        new_dp = [0] * (m + 1)
        new_dp[0] = i

        print(f"\nОбрабатываем A[:{i}] = {show(a[:i])}")
        print(f"new_dp[0] = {i}")

        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
                operation = "match"
            else:
                cost = 1
                operation = "replace"

            delete_value = dp[j] + 1
            insert_value = new_dp[j - 1] + 1
            replace_value = dp[j - 1] + cost

            new_dp[j] = min(
                delete_value,
                insert_value,
                replace_value
            )

            print(
                f"dp[{i}][{j}] для {show(a[:i])} -> {show(b[:j])}: "
                f"delete={delete_value}, "
                f"insert={insert_value}, "
                f"{operation}={replace_value} => {new_dp[j]}"
            )

        dp = new_dp

        print("Готовая строка DP: dp =", dp)

    print("Расстояние Левенштейна:", dp[m])

    return dp[m]


a = input()
b = input()

levenshtein(a, b)