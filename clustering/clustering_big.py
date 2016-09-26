from union_find import *

def put_neighbours_to_same_cluster(clusters, node, shortest_distance):

    pass

input = open('inputs/tc1_big.txt')
lines = input.read().splitlines()
first_line_def = lines[0].split()

cnt_nodes = int(first_line_def[0])
print("cnt_nodes = %d" % cnt_nodes)

cnt_bits = int(first_line_def[1])
print("cnt_bits = %d" % cnt_bits)

clusters = dict.fromkeys([int(line.replace(' ', ''), 2) for line in lines[1:]])
uf = UnionFind(clusters)

print('hamming distances have been read')

shortest_distance = 2
for node in clusters:
    # вычислить соседа с помощью каждого из cnt_bits битов    
    bit_index = 0    
    while bit_index < cnt_bits:
        i_position_bit = (node & 2**bit_index) / 2**bit_index
        neighbour = None
        if i_position_bit == 1:            
            neighbour = (node + 2**bit_index)
        else:            
            neighbour = (node + 2**bit_index)
        #есть сосед (расстояние от эталона не больше shortest_distance)
        #проверить, есть ли в массиве сосед
        if neighbour in clusters:
            #если есть, то ищем в объединении
            сl_neighbour = uf.find(neighbour)
            cl_ethalon = uf.find(node)            
            #теперь возможны два случая
            # он в том же кластере, что и эталон, то оставляем всё как есть
            # он в другом кластере
            if сl_neighbour != cl_ethalon:
                # если эталон сам по себе, то эталон включаем в соседский кластер
                # если эталон уже в кластере, а сосед в другом, то включаем меньший кластер в больший
                # т.е. в любом случае включаем меньший кластерв больший, этим занимается реализация UnionFind
                uf.union(cl_neighbour, cl_ethalon)
        # будем переходить к следующему соседу в следующей итерации    
        bit_index+=1

cnt_clusters = len(clusters)
print('shortest_distance = %d and cnt_clusters = %d' %  (shortest_distance, cnt_clusters))
print('finish')

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