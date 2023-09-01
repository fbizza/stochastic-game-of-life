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


grid_size = (500, 500)
initial_probability = 0.1
n_time_steps = 10000
grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
n_samples = 5
p_dc = 0.004
p_lc = 0.9935
p_lc_large = 0.9945
p_lc_small = 0.9925
log_distances = np.logspace(-3.4, -2, n_samples)

pl_list = []
pl_list_large = []
pl_list_small = []

for num in log_distances:
    p_l = num + p_lc
    p_l_large = num + p_lc_large
    p_l_small = num + p_lc_small
    pl_list.append(p_l)
    pl_list_large.append(p_l_large)
    pl_list_small.append(p_l_small)

phi_list = []
phi_list_large = []
phi_list_small = []

for i in tqdm(range(n_samples), desc='Running the 1/3 simulation loop'):
    densities = run_simulation(grid, p_dc, pl_list[i])
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    phi_list.append(phi)

for i in tqdm(range(n_samples), desc='Running the 2/3 simulation loop'):
    densities = run_simulation(grid, p_dc, pl_list_large[i])
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    phi_list_large.append(phi)

for i in tqdm(range(n_samples), desc='Running the 3/3 simulation loop'):
    densities = run_simulation(grid, p_dc, pl_list_small[i])
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    phi_list_small.append(phi)


plt.loglog(log_distances, phi_list, 'o', color='blue', label='p$_{lc}$ = 0.9935')
plt.loglog(log_distances, phi_list_large, 'o', color='red', label='p$_{lc}$ = 0.9945')
plt.loglog(log_distances, phi_list_small, 'o', color='yellow', label='p$_{lc}$ = 0.9925')
plt.title('Double-logarithmic plot of the life density \u03A6')
plt.xlabel('p$_l$ - p$_{lc}$')
plt.ylabel('\u03A6')
plt.xlim(0.0001, 0.01)
plt.ylim(0.01, 0.1)
plt.legend()
plt.savefig('grafico.png')
plt.show()

slope, _, _, _, _ = linregress(np.log(log_distances), np.log(phi_list))

print(f"\nSlope: {slope}")
