def clip(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    return x