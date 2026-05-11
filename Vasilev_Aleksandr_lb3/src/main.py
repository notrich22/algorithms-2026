def show(s):
    return s if s else '""'


def prefix_distances(a, b):
    n = len(a)
    m = len(b)

    dp = list(range(m + 1))
    distances = [dp[m]]

    print("\n=== ТАБЛИЦА DP ПРЕФИКСОВ ===")
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

        distances.append(new_dp[m])
        dp = new_dp

        print(f"i={i} | A[:{i}]={show(a[:i])} | dp={dp} | dist={new_dp[m]}")

    return distances


def suffix_distances(a, b):
    n = len(a)
    m = len(b)

    next_dp = [m - j for j in range(m + 1)]
    distances = [0] * (n + 1)
    distances[n] = next_dp[0]

    print("\n=== ТАБЛИЦА DP СУФФИКСОВ ===")
    print(f"i={n} | A[{n}:]={show('')} | dp={next_dp} | dist={next_dp[0]}")

    for i in range(n - 1, -1, -1):
        current_dp = [0] * (m + 1)
        current_dp[m] = n - i

        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                cost = 0
            else:
                cost = 1

            current_dp[j] = min(
                next_dp[j] + 1,
                current_dp[j + 1] + 1,
                next_dp[j + 1] + cost
            )

        distances[i] = current_dp[0]
        next_dp = current_dp

        print(f"i={i} | A[{i}:]={show(a[i:])} | dp={current_dp} | dist={current_dp[0]}")

    return distances


a = input()
b = input()

print("=== ВХОДНЫЕ ДАННЫЕ ===")
print("A =", show(a))
print("B =", show(b))

prefixes = prefix_distances(a, b)
suffixes = suffix_distances(a, b)

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