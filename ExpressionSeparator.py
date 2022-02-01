from distutils.util import subst_vars
from typing import Dict, List

import numpy as np



class Expression:

    def __init__(self, operation_txt, priority = 0) -> None:
        self.operation_txt = operation_txt
        self.priority = priority
        self.larg, self.operation, self.rarg = operation_txt
        self.id = 0

    def set_id(self, id):
        self.id = id

    def rise_priority(self) -> None:
        self.priority += 1
        
    def __str__ (self):
        return f"Expression: {self.operation_txt}, priority = {self.priority}"



class ExpressionSeparator:

    exp_list = []
    exp_full_str = ''

    def __init__(self) -> None:
        self.supported = list('*/+-')
        self.parenthesis = list('()')
        self.numbers = list('1234567890')
        

    def add_expression_to_list(self, string:str, priority = 0):
        string = [ elem if type(elem) != type([]) else elem[0] for elem in string ]
        self.exp_list.append(Expression(string, priority))
        self.exp_list[-1].set_id(len(self.exp_list)-1)

    
    def convert_string_to_exprs(self, string:str) -> List[Expression]:
        self.exp_full_str = list(string)
        self.exp_full_str = self.fix_separated_numbers(self.exp_full_str)
        self.exp_full_str = self.fix_subtraction_operations(self.exp_full_str)
        clean_list = self.extract_parenthesis(self.exp_full_str)
        self.rise_all_priorities()
        self.define_exp_for_prepared_data(clean_list)
        return self.exp_list
        # self.fix_complex_elements_in_exp_list()


    def define_exp_for_prepared_data(self, arr):
        equation = ''
        operations_not_defined = 1
        while(operations_not_defined):
            for idx, elem in enumerate(arr):
                
                if type(elem) == type(list([])):
                    while(type(elem) == type(list([])) and len(elem)>1 ):

                        equation = self.define_exp_operation_for_math_eq(elem)
                        arr[idx] = equation
                        elem = equation


            equation = self.define_exp_operation_for_math_eq(arr)
            arr = equation

            if arr is None:
                operations_not_defined = 0
            elif(all(np.isin(arr, 'exp'))):
                operations_not_defined = 0

        
     
    # def fix_complex_elements_in_exp_list(self):
    #     for elem in self.exp_list:
    #         _counter = 0
    #         for operator in self.supported:
    #             unique, _counter = np.unique(elem.operation_txt, return_counts=True)
    #             print(_counter)



    def define_exp_operation_for_math_eq(self, equation):

        equation =  np.array(equation, dtype=object)
        for operator in self.supported:
            if any(np.isin(equation, operator)) :
                operator_index = np.argmax(equation == operator)
                if operator_index > 0:
                    new_exp = equation[operator_index-1 : operator_index+2].copy()
                    np.array([*zip(*equation)]).ravel()
                    self.add_expression_to_list(new_exp,1)
                    equation[operator_index+1] = f'self.exp_list[{self.get_free_exp_cell_idx()}]'
                    equation[operator_index-1 : operator_index+1] = ''
                    equation = equation[equation.nonzero()]
                    self.rise_all_priorities()
                    return equation.tolist() # [*equation] #.tolist()
          
 
    def rise_all_priorities(self):
        for e in self.exp_list: e.rise_priority()

    def get_free_exp_cell_idx(self):
            return len(self.exp_list)-1

    def fix_separated_numbers(self, arr):
        arr = np.array(arr)
        mask = np.isin(arr, self.numbers)
        _arr = []
        _full_number = '' #np.array('')
        _last_numerical_elem_cnt = 0
        for idx, elem in enumerate(arr):    

            if mask[idx] == True:
                _last_numerical_elem_cnt += 1
                _full_number += elem
                if idx == len(arr)-1:
                    _arr.append(elem)
            elif _last_numerical_elem_cnt >= 1:
                _arr.append(''.join(_full_number))
                _full_number = []
                _last_numerical_elem_cnt = 0
                _arr.append(elem)
            else:
                _arr.append(elem)
                _last_numerical_elem_cnt = 0
        return _arr

    def fix_subtraction_operations(self, arr):
        subst_char = '-'
        out = []
        for idx, charr in enumerate(arr):
            if(charr == subst_char): 
                out.append('+')
                out.append('-1')
                out.append('*')
            else:
                out.append(charr)
        return out


    def extract_parenthesis(self, string:str):
        
        arr_no_parenth = []
        
        supported = list('*/+-')
        parenthesis = list('()')

        patenth_tmp = []
        parenth_idx = []
        right_parenth_cnt = 0
        left_parenth_cnt = 0
        '(1-1+(6+7))*2+3*(1-3+4)+10/2'
        for idx, char in enumerate(string[:]):
                if char == '(' :
                    parenth_idx.append(idx)
                    right_parenth_cnt +=1
                elif char == ')' :
                    parenth_idx.append(idx)
                    left_parenth_cnt += 1
                    if right_parenth_cnt != left_parenth_cnt:
                        continue
                    if len(parenth_idx) == 2:
                        parenthesis_exp = string[parenth_idx[0]:(parenth_idx[-1]+1)]
                        parenthesis_exp =  parenthesis_exp[1:-1]#parenthesis_exp.replace("(",'', 1).replace(")",'', 1)
                        exp_tmp = parenthesis_exp
                        while(len(exp_tmp)>1):
                            exp_tmp = self.define_exp_operation_for_math_eq(exp_tmp)
                        
                        arr_no_parenth.append(exp_tmp) #(f'self.exp_list[{self.get_free_exp_cell_idx()}]')
                        # self.add_expression_to_list(parenthesis_exp,1)
                        
                        parenth_idx = []
                        left_parenth_cnt = 0
                        right_parenth_cnt = 0
                    elif len(parenth_idx)%2 == 0 and char == ')':
                        parenthesis_exp = string[parenth_idx[0]:(parenth_idx[-1]+1)]
                        parenthesis_exp = parenthesis_exp[1:-1]
                        _arr = self.extract_parenthesis(parenthesis_exp)
                        while(len(_arr)>1):
                            _arr = self.define_exp_operation_for_math_eq(_arr)
                        arr_no_parenth.append(_arr)
                        parenth_idx = []
                        left_parenth_cnt = 0
                        right_parenth_cnt = 0

                elif len(parenth_idx) == 0:
                    arr_no_parenth.append(char)
  
        return arr_no_parenth


