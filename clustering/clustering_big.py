import sys
from union_find import *

def process(input_path):
    input = open(input_path)
    lines = input.read().splitlines()
    first_line_def = lines[0].split()

    cnt_nodes = int(first_line_def[0])
    print("cnt_nodes = %d" % cnt_nodes)
    cnt_bits = int(first_line_def[1])
    print("cnt_bits = %d" % cnt_bits)
    if(len(first_line_def) > 2):
        expected_answer = int(first_line_def[2])    

    clusters = {}
    for index, line in enumerate(lines[1:]):    
        clusters[int(line.replace(' ', ''), 2)] = index
        #print(clusters)

    uf = UnionFind(clusters)

    print('hamming distances have been read')

    spacing = 2
    for node in clusters:    
        # вычислить соседа с помощью каждого из cnt_bits битов    
        first_bit_index = 0        
        while first_bit_index < cnt_bits:
            neighbour_one_bit_inverted = invert_bit_in_number(node, first_bit_index)         
                
            process_neighbour(clusters, neighbour_one_bit_inverted, uf, node)
            #neighbour_cnt += 1
            second_bit_index = first_bit_index + 1
            while second_bit_index < cnt_bits:
                if second_bit_index != first_bit_index:
                    neighbour_two_bits_inverted = invert_bit_in_number(neighbour_one_bit_inverted, second_bit_index)                    
      
                    #есть сосед (расстояние от эталона не больше spacing)
                    #проверить, есть ли в массиве сосед
                    process_neighbour(clusters, neighbour_two_bits_inverted, uf, node)
                    
                    #if test_case:
                    #    print("{0:b}".format(neighbour_two_bits_inverted))
                    
                    #neighbour_cnt += 1
                    second_bit_index+=1
            # будем переходить к следующему соседу в следующей итерации    
            first_bit_index+=1    

    cluster_parents = {}
    for el in uf:  
        if el.parent not in cluster_parents:
            cluster_parents[el.parent] = []
        cluster_parents[el.parent].append(el) 

    cluster_parents_cnt = len(cluster_parents)
    print('spacing = %d and cnt_clusters = %d' %  (spacing, cluster_parents_cnt))
    if(expected_answer is not None and cluster_parents_cnt != expected_answer):
        print('WRONG! WRONG! WRONG!');
    print('finish')

    if False:
        print('CHECK CORRECTNESS')    

        for point in clusters:
            print(point)
            point_parent = uf.find(point).parent
            print(point_parent)
            print('------')

        print('Done')

    print()

def invert_bit_in_number(number, bit_index):
    bit = (number & 2**bit_index) / 2**bit_index
    if bit == 1:            
        return (number - 2**bit_index)
    else:            
        return (number + 2**bit_index)

def process_neighbour(clusters, neighbour, uf, node):
    if neighbour in clusters:                    
        #если есть, то ищем в объединении
        cl_neighbour = uf.find(neighbour)
        cl_ethalon = uf.find(node)            
        #теперь возможны два случая
        # он в том же кластере, что и эталон, то оставляем всё как есть
        # он в другом кластере
        if cl_neighbour.parent != cl_ethalon.parent:
            # если эталон сам по себе, то эталон включаем в соседский кластер
            # если эталон уже в кластере, а сосед в другом, то включаем меньший кластер в больший
            # т.е. в любом случае включаем меньший кластерв больший, этим занимается реализация UnionFind
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

inputs = [
    'inputs/tc1_big.txt',
    'inputs/tc2_big.txt',
    'inputs/tc3_big.txt',
    'inputs/tc4_big.txt',
    'inputs/tc5_big.txt'
]

#input = open("inputs/clustering_big.txt")

for input_path in inputs:
    process(input_path)