import subprocess
import time
import matplotlib.pyplot as plt

EXECUTABLE = "./square_solver"
N_VALUES = range(2, 21)
MEASUREMENTS = 5

x, y = [], []

for n in N_VALUES:
    times = []
    for _ in range(MEASUREMENTS):
        start = time.perf_counter()
        subprocess.run([EXECUTABLE], input=str(n), text=True, capture_output=True)
        times.append((time.perf_counter() - start) * 1000)
    
    avg_ms = sum(times) / MEASUREMENTS
    x.append(n)
    y.append(avg_ms)
    print(f"N={n}, avg={avg_ms:.4f} ms")

plt.figure(figsize=(8, 5))
plt.plot(x, y, marker="o")
plt.xlabel("Размер квадрата N")
plt.ylabel("Среднее время, мс")
plt.title("Зависимость времени выполнения от N")
plt.grid(True)
plt.savefig("time_vs_n.png")
plt.show()