import time
import matplotlib.pyplot as plt
import numpy as np

from src.State import State

state = State(2)
state.h_walls.add((4,4))
state.h_walls.add((3,3))
state.h_walls.add((5,5))
state.h_walls.add((6,6))
state.h_walls.add((6,2))

execution_times = []

for _ in range(500):
    start = time.perf_counter_ns()
    state.neighbors()
    end = time.perf_counter_ns()
    execution_times.append((end - start)/10000)

print(f"Average Time: {np.mean(execution_times)}\n"
      f"Maximum Time: {max(execution_times)}\n"
      f"Minimum Time: {min(execution_times)}\n")

plt.boxplot(execution_times)
plt.title('Execution Time Box Plot')
plt.ylabel('Time (ns)')
plt.show()