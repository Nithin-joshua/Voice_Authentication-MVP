AUTH_THRESHOLD = 0.85

def is_authenticated(score):
    return score >= AUTH_THRESHOLD
