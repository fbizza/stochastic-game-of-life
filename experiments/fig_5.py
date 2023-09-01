import matplotlib.pyplot as plt
import numpy as np
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


def run_simulation(grid, p_d, p_l):
    densities = []
    for _ in tqdm(range(n_time_steps), desc=f"Running {grid_size} simulation"):
        new_grid, density = update_grid(grid, p_d, p_l)
        grid = new_grid
        densities.append(density)
    return densities


initial_probability = 0.1
n_time_steps = 10000
n_samples = 5
p_d = 0.005
p_l_critical = 0.9925
p_l = 0.9935
log_grid_sizes = np.logspace(1, 3, n_samples)


phi_list_critical = []
phi_list = []

for i in range(n_samples):
    grid_size = (int(log_grid_sizes[i]), int(log_grid_sizes[i]))
    grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
    densities = run_simulation(grid, p_d, p_l_critical)
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    print(f"\nMean density: {round(phi, 3)}")
    phi_list_critical.append(phi)

for i in range(n_samples):
    grid_size = (int(log_grid_sizes[i]), int(log_grid_sizes[i]))
    grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
    densities = run_simulation(grid, p_d, p_l)
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    print(f"\nMean density: {round(phi, 3)}")
    phi_list.append(phi)


plt.loglog(log_grid_sizes, phi_list_critical, 'o')
plt.loglog(log_grid_sizes, phi_list, 'o')
plt.title('Double-logarithmic plot of the life density \u03A6 vs system size L')
plt.xlabel('L')
plt.ylabel('\u03A6')
plt.xlim(5, 1750)
plt.ylim(0.0065, 0.15)
x_ticks = [10, 100, 1000]
y_ticks = [0.01, 0.1]
plt.xticks(x_ticks)
plt.yticks(y_ticks)
plt.show()

