import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

grid_size = (500, 500)
initial_probability = 0.1  # Probability for an initial cell to be alive
p_d = 0.02  # Probability for a dead cell to come to life with 2 living neighbors
p_l = 0.985  # Probability for a living cell to stay alive with 2 living neighbors
n_time_steps = 10


def update_grid(grid):
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


def run_simulation(grid):
    for _ in tqdm(range(n_time_steps)):
        new_grid, density = update_grid(grid)
        grid = new_grid
        densities.append(density)


def plot_density_distribution(densities):
    plt.hist(densities, bins=100, color='teal')
    plt.xlabel('Density of Life (\u03A6)')
    plt.ylabel('D(\u03A6)')
    plt.title('Density Distribution')
    plt.show()


def plot_density(densities):
    plt.figure()
    plt.plot(densities, color='teal')
    plt.xlabel('t')
    plt.ylabel('Density of Life (\u03A6) ')
    plt.title(f'Density evolution over {n_time_steps} time steps')
    plt.show()

grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])

densities = []
run_simulation(grid)

plot_density(densities)
plot_density_distribution(densities)
