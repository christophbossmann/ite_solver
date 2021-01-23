#https://www.youtube.com/watch?v=Wz85Hiwi5MY
#https://www.youtube.com/watch?v=bebqXO8H4eA

def get_formular_as_symbol_list(formular):
    output = []
    i = 0
    atom_list = []
    while(i < len(formular)):

        if(formular[i] == ' '):
            i += 1
            continue
        
        if(formular[i] == 'X'):
            tupel = __evaluate_atom(formular,i)
            i = tupel[0]
            output.append(tupel[1])
            if(not(tupel[1] in atom_list)):
                atom_list.append(tupel[1])
            continue
        
        output.append(formular[i])
        i += 1

    return output, atom_list

def __postpix_to_infix(postfix_list):
    stack = []
    for i in postfix_list:

        if(i == True or i == False or i[0] == 'X'):
            stack.append(i)
            continue

        if(i == '-'):
            op1 = stack.pop()
            if((type(op1) == bool)):
                op1 = str(op1)
            #stack.append(i+op1)
            stack.append([i, op1])

        if(i == '&' or i == '|' or i == '>' or i == '<' or i == '~'):
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(["(", op2, i, op1, ")"])
            
    array = []
    unleash_nested_array([stack.pop()], array)
    return array


def __shunting_yard_algorithm(symbol_list):
    stack = []
    output = []

    for i in symbol_list:
        if(i == True or i == False or i[0] == 'X'):
            output.append(i)
            continue
        if(i == ')'):
            taken = None
            while True:
                taken = __pop(stack)
                if(taken) == -1:
                    break
                if(taken == '('):
                    break
                output.append(taken)
            continue

        if(not(stack)):
            stack.append(i)
            continue

        if(i == '-'):
            taken = stack.append(i)
            continue

        taken = __pop(stack)
        if(taken != -1):
            if(taken == '-' and i != '('):
                output.append(taken)
            else:
                stack.append(taken)

        stack.append(i)

    if(stack):
        while True:
            taken = __pop(stack)
            if(taken == -1):
                break
            if(taken != '(' and taken != ')'):
                output.append(taken)

    return output

def unleash_nested_array(array, elements):
    for a in array:
        if(type(a) in (tuple, list)):
            unleash_nested_array(a, elements)
        else:
            elements.append(a)

def __post_fix_stack_evaluator(postfix_list):
    stack = []
    for i in postfix_list:
        if(i == True or i == False or not(__is_atom(i) == -1)):
            stack.append(i)
            continue

        if(i == '-'):
            e1 = stack.pop()
            if(e1 == False or e1 == True):
                stack.append(not(e1))
            else:
                stack.append([e1, i])
            continue

        if(i == '&'):
            e1 = stack.pop()
            e2 = stack.pop()
            stack.append(__and(e2, e1))
            continue

        if(i == '|'):
            e1 = stack.pop()
            e2 = stack.pop()
            stack.append(__or(e2, e1))
            continue

        if(i == '>'):
            e1 = stack.pop()
            e2 = stack.pop()
            stack.append(__implies_right(e2, e1))
            continue

        if(i == '<'):
            e1 = stack.pop()
            e2 = stack.pop()
            stack.append(__implies_left(e2, e1))
            continue

        if(i == '~'):
            e1 = stack.pop()
            e2 = stack.pop()
            stack.append(__bi_implication(e2, e1))
            continue

        print('Error while parsing: Unsupported symbol!')
        break

    return stack

def __pop(stack):
    if(not(stack)):
        return -1
    return stack.pop()

def __is_atom(e1):
    if(not(type(e1) == str)):
        return -1
    if(not(e1[0] == 'X')):
        return -1
    num_s = ''
    for i in range(1, len(e1)):
        if(not(e1[i].isdigit())):
            return False
        num_s += e1[i]
    return int(num_s)


def __and(e1, e2):
    if(e1 == False or e2 == False):
        return False
    if(e1 == True and e2 == True):
        return True
    return [e1, e2, '&']

def __or(e1, e2):
    if(e1 == True or e2 == True):
        return True
    if(e1 == False and e2 == False):
        return False
    return [e1, e2, '|']

def __implies_right(e1, e2):       
    if(e1 == False):
        return True
    if(e1 == True and e2 == True):
        return True
    if(e1 == True and e2 == False):
        return False
    return [e1, e2, '>']

def __implies_left(e1, e2):       
    if(e2 == False):
        return True
    if(e2 == True and e1 == True):
        return True
    if(e2 == True and e1 == False):
        return False
    return [e1, e2, '<']

def __bi_implication(e1, e2):
    if(e1 == True and e2 == True):
        return True
    if(e1 == True and e2 == False):
        return False
    if(e1 == False and e2 == True):
        return False
    if(e1 == False and e2 == False):
        return True
    return [e1, e2, '~']

def __evaluate_atom(formular, n):
    i = n
    i += 1
    result = ''
    while(i < len(formular) and formular[i].isdigit()):
        result += formular[i]
        i += 1
    return i, ''.join(('X', result))

def set_interpretations_formular_list(formular, interpretations):
    i = 0
    result = []
    for s in formular:
        atom_num = __is_atom(s)
        if(not(atom_num == -1)):
            if(interpretations[atom_num] == True or interpretations[atom_num] == False):
                result.append(interpretations[atom_num])
            else:
                result.append(s)
            i += 1
        else:
            result.append(s)
    return result

def solve_and_simplify(form_symbol_list, interpretations):
    form_symbol_list = set_interpretations_formular_list(
        form_symbol_list, interpretations)
    post_fix = __shunting_yard_algorithm(form_symbol_list)
    post_fix_evaluated = __post_fix_stack_evaluator(post_fix)
    post_fix_evaluated_unleashed = []
    unleash_nested_array(post_fix_evaluated, post_fix_evaluated_unleashed)
    in_fix = __postpix_to_infix(post_fix_evaluated_unleashed)
    return in_fix, form_symbol_list

def test():
    form = get_formular_as_symbol_list("(X0 & (X1 | X2))")
    print(form)
    print(solve_and_simplify(form[0], [False, True, None]))
    
    
#test()

