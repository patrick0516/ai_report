# 使用模擬退火演算法

import numpy as np
import matplotlib.pyplot as plt

# 生成隨機城市位址
def generate_cities(num_cities, seed=None):
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(num_cities, 2)

# 計算距離矩陣
def calculate_distance_matrix(cities):
    num_cities = cities.shape[0]
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])
    return distance_matrix

# 計算傅鏡的總距離
def calculate_total_distance(path, distance_matrix):
    total_distance = 0
    num_cities = len(path)
    for i in range(num_cities):
        total_distance += distance_matrix[path[i], path[(i + 1) % num_cities]]
    return total_distance

# 模擬退火演算法
def simulated_annealing(cities, initial_temp, cooling_rate, num_iterations):
    num_cities = cities.shape[0]  # 獲取城市的數量
    distance_matrix = calculate_distance_matrix(cities)  # 計算城市之間的距離矩陣
    current_path = np.arange(num_cities)  # 生成初始路徑，城市順序為0, 1, ..., num_cities-1
    np.random.shuffle(current_path)  # 隨機打亂初始路徑
    current_distance = calculate_total_distance(current_path, distance_matrix)  # 計算初始路徑的總距離
    best_path = current_path.copy()  # 初始化最佳路徑為當前路徑
    best_distance = current_distance  # 初始化最佳距離為當前路徑的距離
    temp = initial_temp  # 設置初始溫度

    for iteration in range(num_iterations):  # 選代指定次數
        new_path = current_path.copy()  # 創建當前路徑的副本
        i, j = np.random.randint(0, num_cities, size=2)  # 隨機選擇兩個城市的位置
        new_path[i], new_path[j] = new_path[j], new_path[i]  # 交換這兩個城市的位置，形成新路徑
        new_distance = calculate_total_distance(new_path, distance_matrix)  # 計算新路徑的總距離
        
        # 如果新路徑的距離更短，或者按一定概率接受新路徑
        if new_distance < current_distance or np.random.rand() < np.exp((current_distance - new_distance) / temp):
            current_path = new_path  # 接受新路徑
            current_distance = new_distance  # 更新當前路徑的距離
            if current_distance < best_distance:  # 如果新路徑是目前最短的
                best_path = current_path  # 更新最佳路徑
                best_distance = current_distance  # 更新最佳距離
                
        temp *= cooling_rate  # 按冷卻速率降低溫度
    
    return best_path, best_distance  # 返回最佳路徑和最佳距離


num_cities = 20
initial_temp = 100
cooling_rate = 0.995
num_iterations = 10000

cities = generate_cities(num_cities, seed=42)
best_path, best_distance = simulated_annealing(cities, initial_temp, cooling_rate, num_iterations)

print(f"Best path: {best_path}")
print(f"Best distance: {best_distance}")

def plot_path(cities, path):
    plt.figure(figsize=(10, 6))
    plt.plot(cities[path, 0], cities[path, 1], 'o-', markersize=10)
    plt.plot([cities[path[-1], 0], cities[path[0], 0]], [cities[path[-1], 1], cities[path[0], 1]], 'o-', markersize=10)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Traveling Salesman Problem Solution")
    plt.show()

plot_path(cities, best_path)
