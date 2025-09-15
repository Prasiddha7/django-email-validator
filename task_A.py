
import itertools

distances = {
    ('A', 'B'): 10, ('A', 'C'): 15, ('A', 'D'): 20, ('A', 'E'): 25, ('A', 'F'): 30,
    ('B', 'A'): 10, ('B', 'C'): 35, ('B', 'D'): 25, ('B', 'E'): 17, ('B', 'F'): 28,
    ('C', 'A'): 15, ('C', 'B'): 35, ('C', 'D'): 30, ('C', 'E'): 28, ('C', 'F'): 40,
    ('D', 'A'): 20, ('D', 'B'): 25, ('D', 'C'): 30, ('D', 'E'): 22, ('D', 'F'): 16,
    ('E', 'A'): 25, ('E', 'B'): 17, ('E', 'C'): 28, ('E', 'D'): 22, ('E', 'F'): 35,
    ('F', 'A'): 30, ('F', 'B'): 28, ('F', 'C'): 40, ('F', 'D'): 16, ('F', 'E'): 35,
}

cities = ['B', 'C', 'D', 'E', 'F'] 

def route_distance(route):
    """Calculate total distance of a route starting and ending at A."""
    total = 0
    current = 'A'
    for city in route:
        total += distances[(current, city)]
        current = city
    total += distances[(current, 'A')]  
    return total

# Generate possible routes
min_distance = float('inf')
best_route = None

for perm in itertools.permutations(cities):
    dist = route_distance(perm)
    if dist < min_distance:
        min_distance = dist
        best_route = perm

print("Shortest Route: A -> " + " -> ".join(best_route) + " -> A")
print("Total Distance:", min_distance, "km")

# The Shortest route and its distance is A -> B -> F -> D -> E -> C -> A and sum is 119 km  