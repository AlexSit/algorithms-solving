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

def get_var_to_flip(unsat_clause_positions):
    global clauses

    r1 = random.choice(list(unsat_clause_positions.keys()))
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
        unsat_clause_positions = {}
        unsat_clause_positions_cnt = 0        
        for c_index in range(clauses_cnt):
            isSat = eval_clause(c_index)            
            clauses_eval.append(isSat)            
            if not isSat:
                unsat_clause_positions[c_index] = True
                unsat_clause_positions_cnt += 1
                #if unsat_clause_positions_cnt == 10: # NOTE let's only collect limited number of unsatisfying clauses 
                #    break; 

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

    clauses_eval = []
    succeeded = False
    iter_count = round(math.log(var_count, 2))    
    local_search_iter_count = 2*(var_count**2)    # 2*(var_count**2)   
    clauses_cnt = len(clauses)   

    print("iter_count: {}".format(iter_count))
    print("local_search_iter_count: {}".format(local_search_iter_count))

    #graphviz = GraphvizOutput()
    #graphviz.output_file = './output.png'
    #with PyCallGraph(output=GraphvizOutput()):    
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
            flipped_var = get_var_to_flip(unsat_clause_positions)                
            assignment[flipped_var] = not assignment[flipped_var]
            for clause_to_check_pos in var_in_clauses[flipped_var]:
                isSat_old = clauses_eval[clause_to_check_pos]
                isSat = eval_clause(clause_to_check_pos)
                clauses_eval[clause_to_check_pos] = isSat  
                if isSat:
                    unsat_clause_positions.pop(clause_to_check_pos, None)
                else:        
                    unsat_clause_positions[clause_to_check_pos] = True
                unsat_cnt += (isSat_old - isSat)    
                #sys.exit()                
   
    print("succeeded: {}".format(succeeded))
    print("iterations_number: {}".format(iterations_number))


def main():
    global clauses
    global assignment
    global iterations_number
    global var_in_clauses

    iterations_number = 0
    clauses = []    
    assignment = {}
    var_in_clauses = {}

    f = open('./inputs/2sat1.txt')
    lines = f.read().splitlines()
    var_count = int(lines[0])

    # read clauses from the input and remember whether variable occurs only positive or only negative but not both signs
    vars_sign_info = {}
    raw_clauses = []
    for i in lines[1:]:
        c = tuple( map(int, i.split()) )
        for v in c:
            save_sign_info(vars_sign_info, v)
        raw_clauses.append(c)    

    print('reduce')    
    var_count = 0    
    clause_index = 0
    for c in raw_clauses:              
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
                    var_count += 1
                if abs(t) not in var_in_clauses: var_in_clauses[abs(t)] = [] # remember in which clauses variable exists
                var_in_clauses[abs(t)].append(clause_index)
            clauses.append(c)
            clause_index += 1

    print('start')    
    print(var_count)
    papadimitrous_algorithm(var_count)

if __name__ == '__main__':    
    main()