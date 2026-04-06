import random
import os

def generate_matrix(n, is_symmetric, filename="matrix.txt"):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = graph[j][i] if (is_symmetric and i > j) else random.randint(10, 99)
                
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for row in graph:
            f.write(" ".join(map(str, row)) + "\n")
            
    return graph

def read_matrix(filename="matrix.txt"):
    if not os.path.exists(filename):
        return 0, []
    with open(filename, 'r') as f:
        data = f.read().split()
    if not data: return 0, []
    n = int(data[0])
    graph = [[int(data[i * n + j + 1]) for j in range(n)] for i in range(n)]
    return n, graph

def format_mask(mask, n):
    return "{" + ",".join(str(i) for i in range(n) if mask & (1 << i)) + "}"

def solve_dp(n, graph):
    print("ТОЧНЫЙ МЕТОД (ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ)")
    INF = float('inf')
    num_states = 1 << n
    dp = [[INF] * n for _ in range(num_states)]
    parent = [[-1] * n for _ in range(num_states)]
    
    dp[1][0] = 0
    print("[ДП] Старт из вершины 0. Базовое состояние инициализировано.")
    
    for mask in range(1, num_states):
        if not (mask & 1): continue
            
        for u in range(n):
            if not (mask & (1 << u)) or dp[mask][u] == INF: continue
                
            for v in range(n):
                if not (mask & (1 << v)) and graph[u][v] > 0:
                    next_mask = mask | (1 << v)
                    new_cost = dp[mask][u] + graph[u][v]
                    
                    if new_cost < dp[next_mask][v]:
                        dp[next_mask][v] = new_cost
                        parent[next_mask][v] = u
                        print(f"  Обновлен путь в {v} через {format_mask(next_mask, n)}. Новая стоимость: {new_cost}")
                            
    print("[ДП] Таблица состояний заполнена. Поиск оптимального замыкания в 0...")
    min_cost, last_node, full_mask = INF, -1, num_states - 1
    
    for i in range(1, n):
        if dp[full_mask][i] != INF and graph[i][0] > 0:
            cost = dp[full_mask][i] + graph[i][0]
            if cost < min_cost:
                min_cost = cost
                last_node = i
                
    if min_cost == INF: 
        return None, float('inf')
        
    print("[ДП] Восстановление оптимального маршрута с конца:")
    path, curr, curr_mask = [], last_node, full_mask
    while curr != -1:
        path.append(curr)
        print(f"  Добавлена вершина {curr}")
        curr, curr_mask = parent[curr_mask][curr], curr_mask ^ (1 << curr)
        
    final_path = path[::-1] + [0]
    print("  Замыкание в стартовую вершину 0.")
    return final_path, min_cost

def solve_approx(n, graph):
    print("\nПРИБЛИЖЕННЫЙ МЕТОД (ЖАДНЫЙ + АЛШ-2)")
    
    print("[АЛШ-2] Этап 1: Жадное построение начального маршрута")
    unvisited = set(range(1, n))
    path, curr = [0], 0
    print(f"  Старт в 0.")
    
    while unvisited:
        nxt, min_dist = -1, float('inf')
        for v in unvisited:
            if 0 < graph[curr][v] < min_dist:
                min_dist, nxt = graph[curr][v], v
                    
        if nxt == -1: return None, float('inf')
            
        print(f"  Шаг в ближайшую вершину {nxt} (вес: {min_dist})")
        path.append(nxt)
        unvisited.remove(nxt)
        curr = nxt
        
    if graph[curr][0] == 0: return None, float('inf')
    path.append(0)
    print(f"[АЛШ-2] Базовый маршрут построен: {' -> '.join(map(str, path))}")
    
    print("\n[АЛШ-2] Этап 2: Локальная оптимизация (поиск и устранение пересечений)")
    improved = True
    iteration = 1
    
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1: continue 
                
                u1, v1 = path[i-1], path[i]
                u2, v2 = path[j], path[j+1]
                
                if graph[u1][u2] > 0 and graph[v1][v2] > 0 and graph[u1][v1] > 0 and graph[u2][v2] > 0:
                    current_dist = graph[u1][v1] + graph[u2][v2]
                    new_dist = graph[u1][u2] + graph[v1][v2]
                    
                    if new_dist < current_dist:
                        print(f"  [Итерация {iteration}] Найдено улучшение. Выгода: {current_dist - new_dist}")
                        print(f"    Заменяем связи ({u1}-{v1}) и ({u2}-{v2}) на ({u1}-{u2}) и ({v1}-{v2})")
                        path[i:j+1] = reversed(path[i:j+1])
                        print(f"    Новый маршрут: {' -> '.join(map(str, path))}")
                        improved = True
                        iteration += 1
                        
    if iteration == 1:
        print("  Улучшений не найдено, базовый маршрут локально оптимален.")
    else:
        print("  Оптимизация завершена.")
                        
    total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path) - 1))
    return path, total_cost

def main():
    FILENAME = "matrix.txt"
    n, graph = read_matrix(FILENAME)
    
    if n == 0:
        try:
            n = int(input("Файл не найден. Введите количество городов для генерации N: "))
            graph = generate_matrix(n, is_symmetric=True, filename=FILENAME)
        except ValueError:
            print("Ошибка ввода.")
            return

    exact_path, exact_cost = solve_dp(n, graph)
    approx_path, approx_cost = solve_approx(n, graph)
    
    print(" РЕЗУЛЬТАТЫ")
    
    print("1. Точный метод (ДП):")
    if exact_cost == float('inf'):
        print("  no path")
    else:
        print(f"  Стоимость: {exact_cost}")
        print(f"  Маршрут:   {' -> '.join(map(str, exact_path))}")

    print("\n2. Приближенный метод (АЛШ-2):")
    if approx_cost == float('inf'):
        print("  no path")
    else:
        print(f"  Стоимость: {approx_cost}")
        print(f"  Маршрут:   {' -> '.join(map(str, approx_path))}")

if __name__ == '__main__':
    main()