
def space_to_center(obj: tuple[int, int], container: tuple[int,int]):
    return ((container[0] - obj[0]) // 2, (container[1] - obj[1]) // 2)

def clamp(value, min_value, max_value): 
    return max(min_value, min(value, max_value))

def between(value, min, max, inclusive = True):
    if inclusive:
        return value >= min and value <= max
    return value > min and value < max

def value_or_one(value):
    return value if value != 0 else 1