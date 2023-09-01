import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

grid_size = (500, 500)
initial_probability = 0.1
n_time_steps = 10000


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

def plot_heatmap(matrix, x_labels, y_labels):
    x_labels_formatted = [f'{x:.4f}' for x in x_labels]
    y_labels_formatted = [f'{y:.4f}' for y in y_labels]
    plt.imshow(matrix, cmap='viridis', interpolation="bilinear")
    plt.colorbar()
    plt.title('Phase Diagram')
    plt.xlabel('P$_d$')
    plt.ylabel('P$_l$')
    plt.xticks(np.arange(len(x_labels_formatted)), x_labels_formatted, rotation=45, ha='right')
    plt.yticks(np.arange(len(y_labels_formatted)), y_labels_formatted)
    plt.show()

def create_matrix(num_rows, num_cols, list1, list2):
    matrix = [[(i, j) for j in range(num_cols)] for i in range(num_rows)]

    x, y = np.meshgrid(list1, list2)

    # Update the entries in the matrix with the corresponding meshgrid values
    for i in range(num_rows):
        for j in range(num_cols):
            matrix[i][j] = (x[i, j], y[i, j])

    return matrix


num_rows = 10
num_cols = 10
list1 = np.linspace(0.0, 0.01, num=num_rows)
list2 = np.linspace(1.0, 0.99, num=num_cols)

matrix = create_matrix(num_rows, num_cols, list1, list2)
densities_matrix = np.zeros((num_rows, num_cols))
grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])

for i in tqdm(range(num_rows)):
    for j in range(num_cols):
        probability_tuple = matrix[i][j]
        pd = probability_tuple[0]
        pl = probability_tuple[1]
        densities = run_simulation(grid, pd, pl)
        last_1000 = densities[-1000:]
        phi = np.mean(last_1000)
        densities_matrix[i][j] = phi

for row in densities_matrix:
    row_str = " ".join(f"{num:2.1f}" for num in row)
    print(row_str)

plot_heatmap(densities_matrix, list1, list2)

