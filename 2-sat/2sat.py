import sys
import cProfile
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import random
import math


def adjust_clause_var(i):
    if i == 0:
        raise ValueError
    if i < 0:
        return -(i + 1)
    return i - 1


def get_flip_var_pos(unsat_clause_positions, unsat_clauses_len, clauses):
    r1 = random.randint(0, unsat_clauses_len-1)
    r2 = random.randint(0, 1)
    return abs(adjust_clause_var(clauses[unsat_clause_positions[r1]][r2]))    


def check_clauses(clauses, clauses_cnt, assignment):
    try:
        unsat_clause_positions = []
        unsat_clause_positions_cnt = 0

        for c_index in range(clauses_cnt):
            c = clauses[c_index]

            has_var1_not_operator = False
            has_var2_not_operator = False
            var1_pos = c[0]    
            var2_pos = c[1]    

            if var1_pos == 0 or var2_pos == 0:
                raise ValueError

            if var1_pos < 0:
                has_var1_not_operator = True                
            var1_pos = abs(adjust_clause_var(var1_pos))
            if var2_pos < 0:
                has_var2_not_operator = True                
            var2_pos = abs(adjust_clause_var(var2_pos))

            val1 = not assignment[var1_pos] if has_var1_not_operator else assignment[var1_pos]
            val2 = not assignment[var2_pos] if has_var2_not_operator else assignment[var2_pos]
            if not val1 and not val2:
                unsat_clause_positions.append(c_index)
                unsat_clause_positions_cnt += 1
                if unsat_clause_positions_cnt == 10: # NOTE let's only collect limited number of unsatisfying clauses 
                    break; 

        return unsat_clause_positions
    except:        
        print(var2_pos)
        print(has_var2_not_operator)
        raise

    return True

def papadimitrous_algorithm(var_count, clauses):
    succeeded = False
    iter_count = round(math.log(var_count, 2))    
    local_search_iter_count = 2*(var_count**2)
    clauses_cnt = len(clauses)

    print("iter_count: {}".format(iter_count))
    print("local_search_iter_count: {}".format(local_search_iter_count))

    for attempt in range(iter_count):
        #print(attempt)
        if succeeded:        
            break;
        # initialize array of variables values, assign them with some inital values, uniformly at random
        assignment = [bool(random.getrandbits(1)) for i in range(var_count)]    
        for local_search_index in range(local_search_iter_count):    
            #if local_search_index % 100 == 0:
            #    print(local_search_index)
            if local_search_index == 100:
                sys.exit()
            # check if initial assignment is satisfying
            #print("1")
            graphviz = GraphvizOutput()
            graphviz.output_file = './2sat.png'
            with PyCallGraph(output=GraphvizOutput()):
                unsat_clause_positions = check_clauses(clauses, clauses_cnt, assignment)
                #print("2")
                unsat_clauses_len = len(unsat_clause_positions)
                #print("3")
                if(not unsat_clauses_len):
                    succeeded = True
                    #print(assignment)
                    break;
                #print("4")   
                flip_var_pos = get_flip_var_pos(unsat_clause_positions, unsat_clauses_len, clauses)
                #print("5")
                assignment[flip_var_pos] = not assignment[flip_var_pos]        


    print("succeeded: {}".format(succeeded))


def main():
    f = open('./inputs/2sat1.txt')
    lines = f.read().splitlines()
    var_count = int(lines[0])

    # read clauses from the input
    clauses = []
    for i in lines[1:]:
        clauses.append(tuple( map(int, i.split()) ))    

    papadimitrous_algorithm(var_count, clauses)    

if __name__ == '__main__':    
    main()