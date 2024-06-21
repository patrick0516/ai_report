citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

l = len(citys)
path = [(i+1)%l for i in range(l)]
print("Initial path:", path)

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def pathLength(p):
    dist = 0
    plen = len(p)
    for i in range(plen):
        dist += distance(citys[p[i]], citys[p[(i+1)%plen]])
    return dist

print('Initial path length:', pathLength(path))

def neighbor(p):
    new_p = p.copy()
    i, j = np.random.randint(0, len(p), size=2)
    new_p[i], new_p[j] = new_p[j], new_p[i]
    return new_p

def hillClimbing(x, height, neighbor, max_fail=10000):
    fail = 0
    while True:
        nx = neighbor(x)
        if height(nx) > height(x):
            x = nx
            fail = 0
        else:
            fail += 1
            if fail > max_fail:
                return x

def height(path):
    return -pathLength(path) 

best_path = hillClimbing(path, height, neighbor)

print('Best path:', best_path)
print('Best path length:', pathLength(best_path))

import matplotlib.pyplot as plt

def plot_path(citys, path):
    plt.figure(figsize=(10, 6))
    for i in range(len(path)):
        start = citys[path[i]]
        end = citys[path[(i+1) % len(path)]]
        plt.plot([start[0], end[0]], [start[1], end[1]], 'bo-')
    plt.scatter([city[0] for city in citys], [city[1] for city in citys], color='red')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Traveling Salesman Problem Solution using Hill Climbing")
    plt.show()

plot_path(citys, best_path)
