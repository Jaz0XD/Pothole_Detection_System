def calculate_area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area

def calculate_perimeter(points):
    perimeter = 0.0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        perimeter += ((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2) ** 0.5
    return perimeter

def calculate_volume(points, depth):
    area = calculate_area(points)
    volume = area * depth
    return volume

def calculate_dimensions(points, depth):
    area = calculate_area(points)
    perimeter = calculate_perimeter(points)
    volume = calculate_volume(points, depth)
    return {
        'area': area,
        'perimeter': perimeter,
        'volume': volume
    }