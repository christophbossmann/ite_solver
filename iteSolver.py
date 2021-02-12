import satSolver
'''
Created on Jan 10, 2021

@author: Christoph
'''

def __ite(formula , atoms, interpretations, details, counter):
    
    '''for i in range(0, len(atoms)):
        if(interpretations[i] == None):
            current_index = i
            break'''
                   
    indexes = []
    for i in range(0, len(atoms)):
        if(atoms[i] == 'X'+str(counter)):
            indexes.append(i)       
        
    counter = counter + 1
    current_index = counter -1
    
    interpretations_true = interpretations.copy()
    
    for i in range(0, len(interpretations)):      
        if(i in indexes):
            interpretations_true[i] = True
        
    result_formula_true = satSolver.solve_and_simplify(formula, interpretations_true, atoms)
    
    interpretations_false = interpretations.copy()
    
    for i in range(0, len(interpretations)):
        if(i in indexes):     
            interpretations_false[i] = False
        
    result_formula_false = satSolver.solve_and_simplify(formula, interpretations_false, atoms)
    
    if(len(result_formula_true[0]) == 1 and type(result_formula_true[0][0]) == bool) and (len(result_formula_false[0]) == 1 and type(result_formula_false[0][0]) == bool):
        if(details):
            return ['X'+str(current_index), result_formula_true[0],  result_formula_false[0], result_formula_true[1], result_formula_false[1]]
        else:
            return ['X'+str(current_index), result_formula_true[0], result_formula_false[0]]
    else:          
        true_branch = __ite(result_formula_true[0], atoms, interpretations_true, details, counter)
        false_branch = __ite(result_formula_false[0], atoms, interpretations_false, details, counter)
    
        if(details):
            return ['X'+str(current_index), true_branch, false_branch, result_formula_true[1],  result_formula_false[1]]
        else:
            return ['X'+str(current_index), true_branch, false_branch]

def post_simplify(tree):
    
    if(len(tree) == 1):
        return [tree[0]]
    
    branch_true = post_simplify(tree[1])
    branch_false = post_simplify(tree[2])
                               
    if(branch_true == branch_false):
        return branch_true
    
    return [tree[0], branch_true, branch_false]


'''
Creates an ITE Tree for a formula as recursive array.

:formula_string formula for which an ITE tree is to be created
:details boolean value whether formulas prior to assignment of atoms should be attached

:return Used formula
:return result array which corresponds to the ITE tree (prior to simplification)
:return result array which corresponds to the ITE tree (after simplification)

The result array is a recursive array which corresponds to the ITE tree. The first element
is the atom (X0, X1, ...) which is assigned at this step. 
The second element is the sub tree where the particular atom is assigned with 'true'. 
Accordingly, the third element is the sub tree assigned with 'false'. 
The sub trees follow now the same rules: 
    first element: assigned atom at this (next) step, 
    second element: sub-tree assigned atom at this (next) step with true
    third element: sub-tree assigned atom at this (next) step with false
This continues recursively until all atoms have been assigned where the array contains
either true or false depending if the truth value here of the particular variable assignment
for the formula is true or false.
'''    
def solve_ite(formula_string, details):
    
    formula = satSolver.get_formular_as_symbol_list(formula_string)
    
    atoms = formula[1]
    interpretations = []
    for a in atoms:
        interpretations.append(None) 
    
    pre_simplify_result = __ite(formula[0], atoms, interpretations, details, 0)
    
    post_simplify_result = post_simplify(pre_simplify_result)
    
    return formula, pre_simplify_result, post_simplify_result

def test():
    print(solve_ite("(X0 & X1)", False))

#test()


    
    
