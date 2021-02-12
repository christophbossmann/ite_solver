'''
Created on 14.01.2021

@author: Christoph
'''

from graphviz import Digraph
import iteSolver
import satSolver

def ite_branch(node, headname, dot, details):
    if(type(node) == list):
        
        dot.node(''.join((headname, '_0')), node[0])
        
        dot.edge(headname, ''.join((headname, '_0')))
        
        if(details):  
            dot.node(''.join((headname, '_1')), '<ITE<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(node[3], True) + '</FONT>>')
            dot.node(''.join((headname, '_2')), '<ITE<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(node[4], True) + '</FONT>>')
            
            if(len(node[1]) == 1):
                truthful = get_truthful(node[1])
                dot.node(''.join((headname, '_1')), '<' + truthful[0] + '<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(node[3], True) + '</FONT>>', fillcolor=truthful[1], style="filled") 
            else:
                ite_branch(node[1], ''.join((headname, '_1')), dot, details)
            
            if(len(node[2]) == 1):
                truthful = get_truthful(node[2])
                dot.node(''.join((headname, '_2')), '<' + truthful[0] + '<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(node[4], True) + '</FONT>>', fillcolor=truthful[1], style="filled") 
            else:
                ite_branch(node[2], ''.join((headname, '_2')), dot, details)
        else:
            
            dot.node(''.join((headname, '_1')), 'ITE')
            dot.node(''.join((headname, '_2')), 'ITE')
            
            if(len(node[1]) == 1):
                truthful = get_truthful(node[1])
                dot.node(''.join((headname, '_1')), truthful[0], fillcolor=truthful[1], style="filled") 
            else:
                ite_branch(node[1], ''.join((headname, '_1')), dot, details)
            
            if(len(node[2]) == 1):
                truthful = get_truthful(node[2])
                dot.node(''.join((headname, '_2')), truthful[0], fillcolor=truthful[1], style="filled") 
            else:
                ite_branch(node[2], ''.join((headname, '_2')), dot, details)
        
        dot.edge(headname, ''.join((headname, '_1')), color="green3")
        dot.edge(headname, ''.join((headname, '_2')), color="firebrick2")
        
        return
       
    print('error')    

def get_truthful(value):
    if(value[0]):
        return "W", "greenyellow"
    if(not(value[0])):
        return "F", "tomato"
    print("error")
    return

def get_nested_formula_as_string(formula, htmlescape):
    result_array = []
    satSolver.unleash_nested_array(formula, result_array)
    sb = []
    for e in result_array:
        if(e == True):
            sb.append('True')
            continue
        if(e == False):
            sb.append('False')
            continue
        
        if(htmlescape):
            sb2 = []
            for e2 in e:
                if(e2 == '&'):
                    sb2.append('&amp;')
                    continue
                if(e2 == '>'):
                    sb2.append('&gt;')
                    continue
                if(e2 == '<'):
                    sb2.append('&lt;')
                    continue
                sb2.append(e2)
        
            sb.append(''.join(sb2))
            
        else:
            sb.append(e)
            
             
    result = ' '.join(sb)
    result = result.replace("- ", "-")
    return result

def create_ite_graph(formula, details):
    
    result = iteSolver.solve_ite(formula, details)
    
    print("formula: " + get_nested_formula_as_string(result[0][0], False))
    print('')
    
    dot = Digraph(comment='ITE')
    dot.node('root', '<ITE<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(result[0][0], True) + '</FONT>>')
    
    ite_branch(result[1], 'root', dot, details)

    dot.render('output/ite.gv', view=True)  
    'output/ite.gv.pdf'
            
    dot = Digraph(comment='Simplified ITE')
    dot.node('root', '<ITE<br/><FONT POINT-SIZE="8">' + get_nested_formula_as_string(result[0][0], True) + '</FONT>>')
    
    ite_branch(result[2], 'root', dot, False)

    dot.render('output/simplified-ite.gv', view=True)  
    'output/simplified-ite.gv.pdf'

'''
Creation of an ITE tree based on the entered formula. Two ITE trees are created
in PDF format: One prior to simplification and one after simplification.

Example formulas: (X0 & X1) ; ((X0 & X1) | X2) 
'''
def main():
    print("--------------")
    print("ITE Solver: ")
    print('')
    print("by Christoph B.")
    print("--------------")
    print('')
    print('Syntax:')
    print('')
    print('AND: (X0 & X1)')
    print('OR: (X0 | X1)')
    print('NOT: (-X0)')
    print('IMPLICATION (->): (X0 > X1)')
    print('IMPLICATION (<-): (X0 < X1)')
    print('BI-IMPLICATION (<->): (X0 ~ X1)')
    print('')
    print('ITE trees are stored in PDF format in output folder.')
    print("--------------")
    print('')
    formula = input("Enter formula: ")  
    create_ite_graph(formula, True)
    #input("Press any key to exit")
    
main()

