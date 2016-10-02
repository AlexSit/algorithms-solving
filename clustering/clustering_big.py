import sys

from union_find import *

def invert_bit_in_number(number, bit_index):
    bit = (node & 2**bit_index) / 2**bit_index
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

#input = open('inputs/my1_big.txt') #4
#input = open('inputs/my2_big.txt') #2
#input = open('inputs/my3_big.txt') #1
#input = open('inputs/my4_big.txt') #8
#input = open('inputs/tc1_big.txt') #7
#input = open('inputs/tc2_big.txt') #1
input = open('inputs/tc3_big.txt') #4
#input = open('inputs/tc4_big.txt') #1
#input = open('inputs/tc5_big.txt') #6
#input = open("inputs/clustering_big.txt")
lines = input.read().splitlines()
first_line_def = lines[0].split()

cnt_nodes = int(first_line_def[0])
print("cnt_nodes = %d" % cnt_nodes)

cnt_bits = int(first_line_def[1])
print("cnt_bits = %d" % cnt_bits)

clusters = {}
for index, line in enumerate(lines[1:]):    
    clusters[int(line.replace(' ', ''), 2)] = index
    #print(clusters)

uf = UnionFind(clusters)

print('hamming distances have been read')

spacing = 2
for node in clusters:
    #print(bin(node)[2:])
    # вычислить соседа с помощью каждого из cnt_bits битов    
    first_bit_index = 0        
    while first_bit_index < cnt_bits:
        neighbour_one_bit_inverted = invert_bit_in_number(node, first_bit_index) 

        #print('FIRST BIT INDEX %d' % first_bit_index)
        #print("neighbour: %s" % bin(neighbour_one_bit_inverted)[2:])                  
        process_neighbour(clusters, neighbour_one_bit_inverted, uf, node)

        second_bit_index = first_bit_index + 1
        while second_bit_index < cnt_bits:
            if second_bit_index != first_bit_index:
                neighbour_two_bits_inverted = invert_bit_in_number(neighbour_one_bit_inverted, second_bit_index)            
        
                #есть сосед (расстояние от эталона не больше spacing)
                #проверить, есть ли в массиве сосед
                #print("neighbour: %s" % bin(neighbour_two_bits_inverted)[2:])                  
        
                process_neighbour(clusters, neighbour_two_bits_inverted, uf, node)
                second_bit_index+=1
        # будем переходить к следующему соседу в следующей итерации    
        first_bit_index+=1

#define cluster count
cluster_parents = {}
for el in uf:  
    if el.parent not in cluster_parents:
        cluster_parents[el.parent] = []
    cluster_parents[el.parent].append(el)    

print('spacing = %d and cnt_clusters = %d' %  (spacing, len(cluster_parents)))
print('finish')

if True:
    print('CHECK CORRECTNESS')    
    found_distance_exceeded = False

    uf_list = list(uf.elements.values())
    cnt = len(uf_list)
    el1_index = 0
    while el1_index < cnt - 1:
        el1 = uf_list[el1_index]
        el2_index = el1_index + 1
        while el2_index < cnt:
            el2 = uf_list[el2_index]
            if el1.parent != el2.parent and (not is_spacing_exceeded(cnt_bits, el1.number, el2.number, spacing)):
                print('NUMBERS WITH DISTANCE <= 2 IN DIFFERENT CLUSTERS')

            el2_index += 1
        el1_index += 1

    print('Done')
'''
1) Можно проверять, есть ли в массиве сосед с помощью хэш-таблицы
2) И если есть, то ищем в объединении
3) Если нашли, то два случая:
    - он в том же кластере, что и эталон, то оставляем всё как есть
    - он в другом кластере
        - если эталон сам по себе, то эталон включаем в соседский кластер
        - если эталон уже в кластере, а сосед в другом, то включаем меньший кластер в больший
4) как вычислить соседей: то есть как вычислить все варианты отличающихся на одну или две любые позиции
1 0 1 0 - 10

1 0 1 1 - 11
0 0 1 0 - 2
1 1 1 0 - 14
1 0 0 0 - 8

+

 
можно сделать xor и тогда там, где будет разница мы получим 1 в разряде.
Если будет одна 1 в разряде, то это число степень двойка, 
если две 1 в разряде, то. это степень двойки + другая степень двойки

стоп, но ксор делают с чем-то!

+ 

на ум приходит, пройтись по каждому из битов и поменять его на противоположный,
а что за операция, когда мы меняем бит в i-й позиции?
!вычитание или прибавка!
Как определить, вычитание или прибавка?

N
i = 1
while i <= 24:
    i-th_bit = (N & 2^i) / 2^i
    if i-th_bit == 1:
        N -= 2^i
    else:
        N += 2^i
    i+=1
'''