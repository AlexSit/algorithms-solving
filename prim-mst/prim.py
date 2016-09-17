import sys
import random

def choose_cheapest_new_edge(X, V, sorted_edges):
    min_cost_edge = None
    #print("INSIDE")
    #print('edges left to choose')
    #print(sorted_edges)
    for se in sorted_edges:            
        if((se[0] in X and se[1] in V) or (se[1] in X and se[0] in V)):            
            if(min_cost_edge is None):
                min_cost_edge = se
                #print('X') 
                #print(X)
                #print('V') 
                #print(V)
                #print('choose first')
                #print(min_cost_edge)
            elif(se[2] < min_cost_edge[2]):
                #print(se)
                min_cost_edge = se[2]
                #print(min_cost_edge)
    return min_cost_edge


print(sys.version)
print('Prim\'s Minimum Spanning Tree Algorithm')

fileInput = open("./inputs/edges.txt")
#fileInput = open("./inputs/tc1.txt")
#fileInput = open("./inputs/tc2.txt")
#fileInput = open("./inputs/tc3.txt")
#fileInput = open("./inputs/tc4.txt")

text = fileInput.read()
lines = text.splitlines()

(nodes_count, edges_count) = lines[0].split()
nodes_count = int(nodes_count)
edges_count = int(edges_count)

print('number of nodes: %d'  % nodes_count)
print('number of edges: %d'  % edges_count)

edges = []
for l in lines[1:]:
    edge_definition = l.split()    
    edges.append((int(edge_definition[0]), int(edge_definition[1]), int(edge_definition[2])))
sorted_edges = sorted(edges, key=lambda edge: edge[2])
#print(sorted_edges)

X = []
V = list(range(1, nodes_count + 1))

T = []
rnd_e = random.randint(0, len(sorted_edges)-1)
s = sorted_edges[rnd_e][0]
X.append(s)
#print(s)
V.remove(s)
X_cnt = 1

while (X_cnt != nodes_count):
    e = choose_cheapest_new_edge(X, V, sorted_edges)
    if(e is None):
        raise ValueError('Edge hasn\'t been chosen')
    T.append(e)
    sorted_edges.remove(e)
    if(e[0] not in X):
        X.append(e[0])
        V.remove(e[0])
    if(e[1] not in X):
        X.append(e[1])
        V.remove(e[1])
    X_cnt+=1
    #print("X_cnt = %d" % X_cnt)
    #print("nodes_count = %d" % nodes_count)        
    #print(X)

mst_cnt = sum(e[2] for e in T)
#print(len(T))
print(mst_cnt)