import re
from client import Client
from constants import SERVER_PORTS

def eval_full_expression(expression):
  # strip all whitespace from the message
  expression = re.sub(r'\s+', '', expression)

  # split all the numbers and operators into items in a list
  exp_list = list(filter(None, re.split(r'(\+|\-|\*|/|\(|\))',expression)))

  # evaluate all the parenthesis first
  exp_list = eval_paren(exp_list)

  # evaluate the rest of the expression with the results from the parenthesis
  result = perform_ops(exp_list)

  return(result)



def eval_operations(exp_list, op1, op2):
  '''
  Input : exp_list -> every element (numbers or operators) of expression split up into list i.e ['5', '*', '92', '+', '15']
          op1 -> operator to search for
          op2 -> second operator to look for
          Note: op1 and op2 should have equal priority (think pemdas) i.e multiplication with division or addition with subtraction
  Output : exp_list after evaluating all instances of op1 and op2
  '''

  completed = False

  while not completed:
      
      # look for index of op1
      try:
        op1_index = exp_list.index(op1)
      except ValueError as e:
        op1_index = float('inf')

      # look for index of op2
      try:
        op2_index = exp_list.index(op2)
      except ValueError as e:
        op2_index = float('inf')

      # if both were not found set completed to True
      if(op2_index == float('inf') and op1_index == float('inf')):
        completed = True
      else:
        # if op1_index smaller (i.e more left)
        if op1_index < op2_index:
          
          # init the expression variable
          # set it to a list including [element before operator, operator, element after operator]
              # Ex. ['4', '/', '2']
          expression = exp_list[op1_index - 1: op1_index + 2]
          
          # pass the operator and expression to the eval_exp method
          result = eval_exp(op1, expression)

          # pass in the result and the operator index to update function
          update_exp_list(result, op1_index, exp_list)

        elif op2_index < op1_index:

          # init the expression variable (see above for more details)
          expression = exp_list[op2_index - 1: op2_index + 2]

          # do the division netork call
          result = eval_exp(op2, expression)

          # pass in the result and the operator index to update function
          update_exp_list(result, op2_index, exp_list)

  return exp_list


def update_exp_list(result, op_index, exp_list):
  '''
  Takes the result from a single operation (i.e 6 + 9 = 15)
  And places the result (15) at the index of the operator (+)
  Then deletes the values at the index one above (9) and one below (6) the index of the operator
  '''
  print(f"Update exp list function here the vars : \n\t {op_index}\n\t{exp_list}")
  exp_list[op_index] = result
  del exp_list[op_index + 1]
  del exp_list[op_index - 1]


def eval_exp(operator, expression):

  # I think I need to send to the operation sockets at this point

  print(f"here is the incoming expression for eval_exp {expression}")
  expression = ''.join(expression)

  if(operator == '*'):
    return Client(None, SERVER_PORTS['mult'], expression).return_msg
    # print(f"multiply {expression} = {eval(expression)}")
    # return str(eval(expression))

  elif(operator == '/'):
    return Client(None, SERVER_PORTS['div'], expression).return_msg
    # print(f"divide {expression} = {eval(expression)}")
    # return str(eval(expression))

  elif(operator == '+'):
    return Client(None, SERVER_PORTS['add'], expression).return_msg
    # print(f"add {expression} = {eval(expression)}")
    # return str(eval(expression))

  elif(operator == '-'):
    return Client(None, SERVER_PORTS['sub'], expression).return_msg
    # print(f"subtract {expression} = {eval(expression)}")
    # return str(eval(expression))
    

def eval_paren(exp_list):
  '''
  Input : expression list
  Output : expression list with all parenthesis evaluated
  '''

  # check to see if the parenthesis are valid
  valid, paren_indexes = valid_paren(exp_list)

  # if not valid syntax
  if not valid:
    # error should be sent here
    # could use sys module for stderr

    print("Parenthesis are not valid")
    return None
  
  else:

    for open_paren_index, close_paren_index in paren_indexes:

      # grab contents within the parenthesis (not including the actual parenthesis)
      paren_exp_list = exp_list[open_paren_index + 1 : close_paren_index]

      # evaluate the operations within the parenthesis
      result = perform_ops(paren_exp_list)

      # put the result into the index of the open parenthesis
      exp_list[open_paren_index] = result

      # change all other values (including the close paren) to empty strings
      for i in range(open_paren_index + 1, close_paren_index + 1):
        exp_list[i] = ''

    # filter out the None values and return as a list
    return list(filter(None, exp_list))


def valid_paren(exp_list):
  '''
  Input : full expression
  Output : tup (bool of if valid parenthesis, [(index of start paren, index of end paren)])
  The output list of tuples will be the parenthesis indexes in the order they should be evaluated in
  i.e inner most parenthesis first
  '''

  open_paren = []

  enclosed_paren_exp_indexes = []

  # loop index and elements of the expression list
  for index, elem in enumerate(exp_list):

    print(index, elem)

    # if an open paren
    if elem == '(':
      
      # index and elem as tuple to the open_paren list
      open_paren.append(index)

    # if close paren 
    elif elem == ')':

      # if len of open_paren list is 0 return false
      if(len(open_paren) == 0):
        return (False, [])

      else:

        # pop off the open_paren list (the open paren index that pairs with the current closed paren)
        open_paren_index = open_paren.pop()

        enclosed_paren_exp_indexes.append((open_paren_index, index))
  
  if(len(open_paren) == 0):
    print("HERE THE ENCLOSED PARENT LIST")
    print(enclosed_paren_exp_indexes)
    return(True, enclosed_paren_exp_indexes)
  else:
    return(False, [])

def perform_ops(exp_list):

  # filter the input exp_list to remove empty values. This is done because the 
  # main expression must maintain consistent length so that the open and closed parenthesis indexes are valid
  # so the input passed into this function may have many empty strings. Filter first before using eval_operations method
  # to prevent errors arising from trying to do math operations on an empty string
  exp_list = list(filter(None, exp_list))

  print(f"Here the exp_list after first filter -----> {exp_list}")

  eval_operations(exp_list, '*', '/')
  eval_operations(exp_list, '+', '-')

  exp_list = list(filter(None, exp_list))

  if len(exp_list) == 1:
    return exp_list[0]
  else:
    print(f"Something went wrong....\nThere is more than one element remaining in the exp_list\n\t{exp_list}")
