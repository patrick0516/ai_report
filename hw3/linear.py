import numpy as np

def objective(x, y, z):
    return 3*x + 2*y + 5*z

def is_feasible(x, y, z):
    return (x + y <= 10) and (2*x + z <= 9) and (y + 2*z <= 11) and (x >= 0) and (y >= 0) and (z >= 0)

def get_neighbors(x, y, z, step=0.1):
    neighbors = []
    for dx in [-step, 0, step]:
        for dy in [-step, 0, step]:
            for dz in [-step, 0, step]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                neighbors.append((x + dx, y + dy, z + dz))
    return neighbors

def hill_climbing(x, y, z, max_fail=10000, step=0.1):
    best_x, best_y, best_z = x, y, z
    best_value = objective(x, y, z)
    fail = 0
    while fail < max_fail:
        neighbors = get_neighbors(best_x, best_y, best_z, step)
        improved = False
        for nx, ny, nz in neighbors:
            if is_feasible(nx, ny, nz):
                new_value = objective(nx, ny, nz)
                if new_value > best_value:
                    best_x, best_y, best_z = nx, ny, nz
                    best_value = new_value
                    improved = True
                    break
        if not improved:
            fail += 1
        else:
            fail = 0
    return best_x, best_y, best_z, best_value

initial_x = np.random.uniform(0, 10)
initial_y = np.random.uniform(0, 10)
initial_z = np.random.uniform(0, 10)
while not is_feasible(initial_x, initial_y, initial_z):
    initial_x = np.random.uniform(0, 10)
    initial_y = np.random.uniform(0, 10)
    initial_z = np.random.uniform(0, 10)

best_x, best_y, best_z, best_value = hill_climbing(initial_x, initial_y, initial_z)

print('Best x:', best_x)
print('Best y:', best_y)
print('Best z:', best_z)
print('Best value:', best_value)
