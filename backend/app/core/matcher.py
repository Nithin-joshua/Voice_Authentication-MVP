import numpy as np
from numpy.linalg import norm

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def variance_distance(test, mean, std):
    std_safe = np.where(std == 0, 1e-6, std)
    z = np.abs(test - mean) / std_safe
    return np.mean(z)
