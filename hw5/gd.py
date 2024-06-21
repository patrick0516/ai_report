import numpy as np
from numpy.linalg import norm
from engine import Value

def gradient_descent(f, p0, learning_rate=0.01, max_iterations=100000, tolerance=1e-5):
    p = p0.copy()
    for _ in range(max_iterations):
        fp = f(p)
        fp.backward()
        gradients = [param.grad for param in p]
        grad_norm = norm(gradients)
        
        if grad_norm < tolerance:
            break
        
        step = np.multiply(gradients, -learning_rate)
        p += step

    return p

def f(p):
    x, y, z = p
    return (x - 1) ** 2 + (y - 2) ** 2 + (z - 3) ** 2

if __name__ == "__main__":
    initial_params = [Value(0), Value(0), Value(0)]
    optimized_params = gradient_descent(f, initial_params)
    print(f(optimized_params))
