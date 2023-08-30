import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.stats import linregress


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


def run_simulation(grid, p_d, p_l):
    densities = []
    for _ in range(n_time_steps):
        new_grid, density = update_grid(grid, p_d, p_l)
        grid = new_grid
        densities.append(density)
    return densities


grid_size = (50, 50)
initial_probability = 0.1
n_time_steps = 10000
grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
n_samples = 12
p_d = 0.111
p_c = 0.782
pl_list = []
log_distances = np.logspace(-4, -1, n_samples)

for num in log_distances:
    p_l = num + p_c
    pl_list.append(p_l)

phi_list = []

for i in tqdm(range(n_samples)):
    densities = run_simulation(grid, p_d, pl_list[i])
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    phi_list.append(phi)


plt.loglog(log_distances, phi_list, 'o')
plt.title('Double-logarithmic plot of the life density \u03A6')
plt.xlabel('p - p$_c$')
plt.ylabel('\u03A6')
plt.xlim(0.0001, 0.1)
plt.ylim(0.01, 1)
plt.show()

# Perform linear regression to get line slope
slope, _, _, _, _ = linregress(np.log(log_distances), np.log(phi_list))

print(f"Slope: {slope}")

