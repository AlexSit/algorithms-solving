import sys
import random
import math


def get_flip_var_pos(unsat_clause_positions, unsat_clauses_len, clauses):
    r1 = random.randint(0, unsat_clauses_len-1)
    r2 = random.randint(0, 1)
    return abs(clauses[unsat_clause_positions[r1]][r2])    


def shift_clause_var_to_zero_based(s):
    i = int(s)
    if not i:
        raise ValueError
    return int(i - i/abs(i)) # negatives allowed, but later they'll be processed


def check_clauses(clauses, assignment):
    try:
        unsat_clause_positions = []
        l = len(clauses)

        for c_index in range(l):
            c = clauses[c_index]

            has_var1_not_operator = False
            has_var2_not_operator = False
            var1_pos = c[0]    
            var2_pos = c[1]    

            case = False
            if(var1_pos == -1 and var2_pos == -2):
                case = True
            #TODO: -1 -> 0 => can't recognize @not operator

            if var1_pos < 0:
                has_var1_not_operator = True
                var1_pos = -var1_pos
            if var2_pos < 0:
                has_var2_not_operator = True
                var2_pos = -var2_pos

            val1 = not assignment[var1_pos] if has_var1_not_operator else assignment[var1_pos]
            val2 = not assignment[var2_pos] if has_var2_not_operator else assignment[var2_pos]
            if not (val1 or val2):
                unsat_clause_positions.append(c_index)

        return unsat_clause_positions
    except:
        print(var1_pos)
        print(var2_pos)
        print(l)
        raise

    return True



f = open('./inputs/tests/2-unsat.txt')
lines = f.read().splitlines()
var_count = int(lines[0])


# read clauses from the input
clauses = []
for i in lines[1:]:
    clauses.append(tuple( map(shift_clause_var_to_zero_based, i.split()) ))

succeeded = False
iter_count = round(math.log(var_count, 2))
print("iter_count: {}".format(iter_count))
local_search_iter_count = 2*(var_count**2)
print("local_search_iter_count: {}".format(local_search_iter_count))

for attempt in range(iter_count):
    if succeeded:        
        break;
    # initialize array of variables values, assign them with some inital values, uniformly at random
    assignment = [bool(random.getrandbits(1)) for i in range(var_count)]    
    for local_search_index in range(local_search_iter_count):    
        # check if initial assignment is satisfying
        unsat_clause_positions = check_clauses(clauses, assignment)
        unsat_clauses_len = len(unsat_clause_positions)
        if(not unsat_clauses_len):
            succeeded = True
            print(assignment)
            break;
        
        flip_var_pos = get_flip_var_pos(unsat_clause_positions, unsat_clauses_len, clauses)
        assignment[flip_var_pos] = not assignment[flip_var_pos]        


print("succeeded: {}".format(succeeded))