def show(s):
    return s if s else '""'


def distances(a, b, title):
    n = len(a)
    m = len(b)

    dp = list(range(m + 1))
    result = [dp[m]]

    print(f"\n=== {title} ===")
    print(f"i=0 | A[:0]={show('')} | dp={dp} | dist={dp[m]}")

    for i in range(1, n + 1):
        new_dp = [0] * (m + 1)
        new_dp[0] = i

        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1

            new_dp[j] = min(
                dp[j] + 1,
                new_dp[j - 1] + 1,
                dp[j - 1] + cost
            )

        result.append(new_dp[m])
        dp = new_dp

        print(f"i={i} | A[:{i}]={show(a[:i])} | dp={dp} | dist={new_dp[m]}")

    return result


a = input()
b = input()

print("=== ВХОДНЫЕ ДАННЫЕ ===")
print("A =", show(a))
print("B =", show(b))

prefixes = distances(a, b, "ТАБЛИЦА DP ПРЕФИКСОВ")

reversed_suffixes = distances(a[::-1], b[::-1], "ТАБЛИЦА DP СУФФИКСОВ")

suffixes = [0] * (len(a) + 1)
for i in range(len(a) + 1):
    suffixes[i] = reversed_suffixes[len(a) - i]

best_prefix = min(prefixes)
best_suffix = min(suffixes)

print("\n=== ДИСТАНЦИИ ПРЕФИКСОВ ===")
for i in range(len(a) + 1):
    print(f"A[:{i}]={show(a[:i])} | dist={prefixes[i]}")

print("\n=== ЛУЧШИЕ ПРЕФИКСЫ ===")
print(best_prefix)
for i in range(len(a) + 1):
    if prefixes[i] == best_prefix:
        print(show(a[:i]))

print("\n=== ДИСТАНЦИИ СУФФИКСОВ ===")
for i in range(len(a) + 1):
    print(f"A[{i}:]={show(a[i:])} | dist={suffixes[i]}")

print("\n=== ЛУЧШИЕ СУФФИКСЫ ===")
print(best_suffix)
for i in range(len(a) + 1):
    if suffixes[i] == best_suffix:
        print(show(a[i:]))