import sys
from union_find import *

def collect_neighbours(cnt_bits, node):
    neighbours = []
    # вычислить соседа с помощью каждого из cnt_bits битов    
    first_bit_index = 0        
    while first_bit_index < cnt_bits:
        neighbour_one_bit_inverted = invert_bit_in_number(node, first_bit_index)                     
        neighbours.append(neighbour_one_bit_inverted)
        
        second_bit_index = first_bit_index + 1
        while second_bit_index < cnt_bits:
            if second_bit_index != first_bit_index:
                neighbour_two_bits_inverted = invert_bit_in_number(neighbour_one_bit_inverted, second_bit_index)                    
                neighbours.append(neighbour_two_bits_inverted)            
                second_bit_index+=1
        first_bit_index+=1 
    return neighbours

def process(input_path):
    input = open(input_path)
    lines = input.read().splitlines()
    first_line_def = lines[0].split()

    cnt_nodes = int(first_line_def[0])
    print("cnt_nodes = %d" % cnt_nodes)
    cnt_bits = int(first_line_def[1])
    print("cnt_bits = %d" % cnt_bits)
    expected_answer = None
    if(len(first_line_def) > 2):
        expected_answer = int(first_line_def[2])    

    clusters = {}
    for index, line in enumerate(lines[1:]):    
        clusters[int(line.replace(' ', ''), 2)] = index        

    uf = UnionFind(clusters)

    print('hamming distances have been read')

    spacing = 2
    for node in clusters:            
        neighbours = collect_neighbours(cnt_bits, node)        
        for neighbour in neighbours:                        
            process_neighbour(clusters, neighbour, uf, node)

    cluster_parents = {}
    for el in uf:    
        if el.parent not in cluster_parents:            
            cluster_parents[el.parent] = [None, []]
        cluster_parents[el.parent][1].append(el), 

    cluster_parents_cnt = len(cluster_parents)
    print('spacing = %d and cnt_clusters = %d' %  (spacing, cluster_parents_cnt))
    if(expected_answer is not None and cluster_parents_cnt != expected_answer):
        print('WRONG! WRONG! WRONG!');

    print(uf.size)
    print('finish')

    if False:
        print('CHECK CORRECTNESS')            
        for point in clusters:            
            p = uf.find(point)          
            if p is None:
                print('EXCEPTION')
                continue
            
            point_parent = p.parent  
            neighbours = collect_neighbours(cnt_bits, point)

            for n in neighbours:
                neighbour_element = uf.find(n)                
                if neighbour_element is None:
                    continue
                neighbour_parent = neighbour_element.parent
                if point_parent != neighbour_parent:
                    print('WRONG')       
        
        for i in cluster_parents:
            if(len(cluster_parents[i]) != uf.find(i).size):
                print('WRONG SIZE')
                print(uf.find(i).size)
                for e in cluster_parents[i]:
                    print(e)                
                sys.exit()

        for index, key in enumerate(cluster_parents):            
            cluster_parents[key][0] = index

        for key in cluster_parents:
            cp_neighbours = collect_neighbours(cnt_bits, key)
            for cp_n in cp_neighbours:
                if (cp_n in cluster_parents) and (cluster_parents[cp_n][0] != cluster_parents[key][0]):
                    print('EXCEPTION')                

        print('Done')

    print()

def invert_bit_in_number(number, bit_index):
    bit = (number & 2**bit_index) / 2**bit_index
    if bit == 1:            
        return (number - 2**bit_index)
    else:            
        return (number + 2**bit_index)

def process_neighbour(clusters, neighbour, uf, node):                     
    cl_neighbour = uf.find(neighbour)
    cl_ethalon = uf.find(node)

    if cl_neighbour is None or cl_ethalon is None:
        return

    if cl_neighbour.parent != cl_ethalon.parent:
        uf.union(cl_neighbour.parent, cl_ethalon.parent)

def is_spacing_exceeded(cnt_bits, x, y, max_distance):
    mask = 1
    differenceCount = 0
    i = 0
    while i < cnt_bits:    
         a = x & mask
         b = y & mask
         
         if a != b:             
             differenceCount += 1

         mask = mask << 1
         i += 1 
    
    return differenceCount > max_distance


print(sys.version)
'''
inputs = [
    'inputs/tc1_big.txt',
    'inputs/tc2_big.txt',
    'inputs/tc3_big.txt',
    'inputs/tc4_big.txt',
    'inputs/tc5_big.txt'
]
'''
inputs = [
    "inputs/clustering_big.txt"
]

for input_path in inputs:
    process(input_path)