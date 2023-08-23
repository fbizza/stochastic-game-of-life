import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm
from matplotlib.colors import ListedColormap

grid_size = (100, 100)
initial_probability = 0.1  # Probability for an initial cell to be alive
n_time_steps = 12


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


def plot(pl_list, phi_list):
    plt.plot(pl_list, phi_list, marker='o', linestyle='-')
    plt.title('Phase Transition')
    plt.xlabel('P$_l$')
    plt.ylabel('Density of Life')
    plt.show()

# Initialize the grid
grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])
pl_list = np.linspace(0.9950, 0.9986, num=18)
# pl_list = [0.9950, 0.9968, 0.9986]

phi_list = []

for pl in tqdm(pl_list):
    densities = run_simulation(grid, 0, pl)
    last_1000 = densities[-1000:]
    phi = np.mean(last_1000)
    phi_list.append(phi)

plot(pl_list, phi_list)