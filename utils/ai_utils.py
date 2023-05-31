def linear_map(min_v, max_v, value, min_map = 0, max_map = 1):
    map_v = (value - min_v) / (max_v - min_v) * (max_map - min_map) + min_map
    return 1 if map_v > 1 else 0 if map_v < 0 else map_v