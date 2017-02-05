import sys
import cProfile
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import random
import math
import datetime

global clauses
global assignment
global iterations_number
global var_in_clauses
global clauses_eval
global unsat_cnt

def get_var_to_flip(unsat_cnt, unsat_clause_positions):
    global clauses

    r1 = random.randint(0, unsat_cnt-1)
    r2 = random.randint(0, 1)
    return abs(clauses[unsat_clause_positions[r1]][r2])


def eval_clause(c_index):
    global clauses

    c = clauses[c_index]

    has_var1_not_operator = False
    has_var2_not_operator = False
    var1 = c[0]    
    var2 = c[1]    

    if var1 == 0 or var2 == 0:
        raise ValueError

    if var1 < 0:
        has_var1_not_operator = True                    
    if var2 < 0:
        has_var2_not_operator = True                    
    var1 = abs(var1)
    var2 = abs(var2)

    val1 = not assignment[var1] if has_var1_not_operator else assignment[var1]
    val2 = not assignment[var2] if has_var2_not_operator else assignment[var2]
    return val1 or val2

def check_clauses_from_scratch(clauses_cnt):
    global clauses
    global assignment
    global iterations_number
    global clauses_eval

    clauses_eval = []
    iterations_number += 1
    try:
        unsat_clause_positions = []
        for c_index in range(clauses_cnt):
            isSat = eval_clause(c_index)            
            clauses_eval.append(isSat)            
            if not isSat:
                unsat_clause_positions.append(c_index)

        return unsat_clause_positions
    except:        
        raise

    return True


def save_sign_info(vars_sign_info, k):        
    if abs(k) not in vars_sign_info:
        vars_sign_info[abs(k)] = 0    
    vars_sign_info[abs(k)] |= int((1+k/abs(k)) / 2 + 1)


def papadimitrous_algorithm(var_count):
    global clauses
    global assignment
    global iterations_number
    global clause_index
    global clauses_eval
    global unsat_cnt

    if not var_count:
        print("succeeded: True (var_count == 0)")
        return

    clauses_eval = []
    succeeded = False
    iter_count = round(math.log(var_count, 2))    
    local_search_iter_count = 2*(var_count**2)   
    clauses_cnt = len(clauses)   

    print("iter_count: {}".format(iter_count))
    print("local_search_iter_count: {}".format(local_search_iter_count))

    for attempt in range(iter_count):
        print("attempt: {}".format(attempt))
        print(datetime.datetime.now())

        if succeeded:        
            break;

        # initialize array of variables values, assign them with some inital values, uniformly at random
        assignment = {i: bool(random.getrandbits(1)) for i in assignment}            
        # check if initial assignment is satisfying                       
        unsat_clause_positions = check_clauses_from_scratch(clauses_cnt) 
        unsat_cnt = len(unsat_clause_positions)                
        for local_search_index in range(local_search_iter_count):
            if local_search_index % 10000 == 0:
                print("local_search_index: {}".format(local_search_index))
                print(datetime.datetime.now())
            if not unsat_cnt:
                succeeded = True                    
                break;                
            #graphviz = GraphvizOutput()
            #graphviz.output_file = './output.png'
            #with PyCallGraph(output=GraphvizOutput()):    
            flipped_var = get_var_to_flip(unsat_cnt, unsat_clause_positions) 
            assignment[flipped_var] = not assignment[flipped_var]            
            for clause_to_check_pos in var_in_clauses[flipped_var]:
                isSat_old = clauses_eval[clause_to_check_pos]
                isSat = eval_clause(clause_to_check_pos)
                clauses_eval[clause_to_check_pos] = isSat  
                if isSat:
                    if clause_to_check_pos in unsat_clause_positions: unsat_clause_positions.remove(clause_to_check_pos)
                else:        
                    unsat_clause_positions.append(clause_to_check_pos)                            
                unsat_cnt += (isSat_old - isSat)                    
   
    print("succeeded: {}".format(succeeded))
    print("iterations_number: {}".format(iterations_number))

def reduce_clauses(input_clauses):    
    global assignment    
    global var_in_clauses

    # read clauses from the input and remember whether variable occurs only positive or only negative but not both signs
    vars_sign_info = {}
    clauses = []
    result_clauses = []
    var_in_clauses = {}

    for c in input_clauses:        
        for v in c:
            save_sign_info(vars_sign_info, v)
        clauses.append(c)    
        
    clause_index = 0
    for c in clauses:              
        remove = False        
        for v in c:
            v = abs(v)
            # if in couple at least one variable has only one sign then remove a couple
            if vars_sign_info.get(v, -1) != 3: # variable has both signs; 1 +; 2 -; 0 - no info           
                remove = True
        if not remove:
            for t in c:
                if abs(t) not in assignment:
                    assignment[abs(t)] = True # write down this variable and it won't be used ever later                                        
                if abs(t) not in var_in_clauses: var_in_clauses[abs(t)] = [] # remember in which clauses variable exists
                var_in_clauses[abs(t)].append(clause_index)
            result_clauses.append(c)
            clause_index += 1

    return result_clauses

def main():
    global clauses
    global assignment
    global iterations_number
    global var_in_clauses

    iterations_number = 0
    clauses = []    
    assignment = {}
    var_in_clauses = {}

    '''
    2sat1.txt = 1
    2sat2.txt = 0
    2sat3.txt = 1
    2sat4.txt = 1
    2sat5.txt = 0
    2sat6.txt = 0
    '''

    f = open('./inputs/2sat5.txt')
    lines = f.read().splitlines()
    raw_clauses = []   
    for i in lines[1:]: raw_clauses.append( tuple( map(int, i.split()) ) )
    print('reduce')

    num_reduction = len(raw_clauses)
    print("num_reduction: {}".format(num_reduction))
    for i in range(num_reduction):
        if not i % 10000: print(i)
        clauses = reduce_clauses(raw_clauses)
        raw_clauses = clauses
        
    print('start')        
    var_count = len(clauses)
    print('var_count after reduction:')    
    print(var_count)    
    papadimitrous_algorithm(var_count)

if __name__ == '__main__':    
    main()