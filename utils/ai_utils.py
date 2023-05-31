def linear_map(max, value):
    return round(min(1, value / max), 3)
    

print(linear_map(40, 13))
print(linear_map(31, 13))
print(linear_map(40, 53))
print(linear_map(4, 3))