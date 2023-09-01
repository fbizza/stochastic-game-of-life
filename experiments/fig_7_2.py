import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
from tqdm import tqdm


def update_grid(grid, p_d, p_l):
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    living_cells = 0

    for i in range(rows):
        for j in range(cols):
            # Periodic boundary
            live_neighbors = (
                grid[(i - 1) % rows, (j - 1) % cols] + grid[(i - 1) % rows, j] + grid[(i - 1) % rows, (j + 1) % cols] +
                grid[i, (j - 1) % cols] + grid[i, (j + 1) % cols] +
                grid[(i + 1) % rows, (j - 1) % cols] + grid[(i + 1) % rows, j] + grid[(i + 1) % rows, (j + 1) % cols]
            )

            # Update living cells
            if grid[i, j] == 1:
                living_cells += 1
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0
                elif live_neighbors == 2 and np.random.random() >= p_l:
                    new_grid[i, j] = 0

            # Update dead cells
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1
                elif live_neighbors == 2 and np.random.random() <= p_d:
                    new_grid[i, j] = 1

    density = living_cells/(grid_size[0]*grid_size[1])
    return new_grid, density


def run_simulation(grid, p_d, p_l, i, n):
    densities = []
    for _ in tqdm(range(n_time_steps), desc=f"Running {i+1} of {n} simulations {grid_size}", position=0):
        new_grid, density = update_grid(grid, p_d, p_l)
        grid = new_grid
        densities.append(density)
    return densities

grid_size = (500, 500)
initial_probability = 0.1
n_time_steps = 10000
n_samples = 16
pd_list = np.linspace(0.0, 0.01, num=n_samples)


phi_list = []

for i in range(n_samples):
    grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
    densities = run_simulation(grid, pd_list[i], 1.0, i, n_samples)
    last_1000 = densities[-2000:]
    rounded_last_1000 = np.round(last_1000, 3)
    mode_result = stats.mode(rounded_last_1000)
    mode_value = mode_result.mode[0]
    print(f"\nMode density (pd = {round(pd_list[i], 4)}): {mode_value}")
    phi_list.append(mode_value)


plt.plot(pd_list, phi_list)
plt.title('Life density \u03A6 along edge (p$_d$, p$_l$ = 1)')
plt.xlabel('p$_d$')
plt.ylabel('\u03A6')
plt.ylim(0, 0.1)
plt.show()
