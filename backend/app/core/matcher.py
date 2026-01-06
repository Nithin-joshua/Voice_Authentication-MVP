import numpy as np
from numpy.linalg import norm

def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (norm(vec1) * norm(vec2)))
