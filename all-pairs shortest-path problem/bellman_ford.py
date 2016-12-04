import math
inf = float('inf')

def bellman_ford(graph, i, j):
    shortest_path 
    
    j_neighbours = []
    for index in range():
        

    optimal_solution = inf
    for w in j_neighbours:
        sub_optimal_solution = min(
            A[i][j],
            A[i][w] + graph[w][j]
        )
        optimal_solution = min(optimal_solution, sub_optimal_solution)

    A[i][j] = optimal_solution

    return shortest_path

