import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

grid_size = (100, 100)

# Initialize the grid with zeros
grid = np.zeros(grid_size, dtype=int)

# Glider pattern
glider = np.array([[0, 0, 1],
                   [1, 0, 1],
                   [0, 1, 1]])

# Place the glider at the beginning
grid[50:53, 80:83] = glider

def update_grid(grid):
    new_grid = np.copy(grid)
    rows, cols = grid.shape

    for i in range(rows):
        for j in range(cols):
            # Periodic boundary
            live_neighbors = (
                grid[(i - 1) % rows, (j - 1) % cols] + grid[(i - 1) % rows, j] + grid[(i - 1) % rows, (j + 1) % cols] +
                grid[i, (j - 1) % cols] + grid[i, (j + 1) % cols] +
                grid[(i + 1) % rows, (j - 1) % cols] + grid[(i + 1) % rows, j] + grid[(i + 1) % rows, (j + 1) % cols]
            )

            # Apply the rules
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1

    return new_grid

# Create a custom colormap with teal and orange colors
colors = ['teal', 'orange']
cmap = ListedColormap(colors)

# Create a function to update the plot in each animation frame
def update(frameNum, img, grid):
    new_grid = update_grid(grid)
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

# Create the initial plot
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap=cmap)
ani = animation.FuncAnimation(fig, update, fargs=(img, grid), frames=10, interval=50, save_count=50)

plt.show()
