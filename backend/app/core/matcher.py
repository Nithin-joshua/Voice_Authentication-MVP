import numpy as np
from numpy.linalg import norm

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def variance_distance(test, mean, std):
    std_safe = np.where(std == 0, 1e-6, std)
    z = np.abs(test - mean) / std_safe
    return np.mean(z)

def temporal_consistency(mfcc_segments):
    """
    Measures frame-to-frame variation across segments.
    Lower value = more stable (AI-like)
    Higher value = natural human variation
    """
    distances = []

    for i in range(len(mfcc_segments) - 1):
        a = mfcc_segments[i]
        b = mfcc_segments[i + 1]

        # Normalize length
        min_len = min(len(a), len(b))
        a = a[:min_len]
        b = b[:min_len]

        dist = np.linalg.norm(a - b)
        distances.append(dist)

    return np.mean(distances)
