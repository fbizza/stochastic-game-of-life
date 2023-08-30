import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

grid_size = (200, 200)
initial_probability = 0.1  # Probability for an initial cell to be alive
p_d = 0.005  # Probability for a dead cell to come to life with 2 living neighbors
p_l = 0.9925  # Probability for a living cell to stay alive with 2 living neighbors
n_time_steps = 10000
densities = []

# Initialize the grid
grid = np.random.choice([0, 1], grid_size, p=[1 - initial_probability, initial_probability])

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

# Create a function to update the plot in each animation frame
def update(frameNum, img, grid):
    if frameNum <= n_time_steps:  # Stop the animation after 10000 frames
        new_grid, density = update_grid(grid)
        img.set_data(new_grid)
        grid[:] = new_grid[:]
        print(f"Current density: {density}")
        densities.append(density)
    else:
        ani.event_source.stop()  # Stop the animation
    return img

colors = ['teal', 'orange']
cmap = ListedColormap(colors)

fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap=cmap)
ani = animation.FuncAnimation(fig, update, fargs=(img, grid), interval=0.1)

plt.show()

plt.figure()
plt.plot(densities, color='teal')
plt.xlabel('t')
plt.ylabel('Density of Life (\u03A6) ')
plt.title(f'Density evolution over {len(densities)} time steps')
plt.show()