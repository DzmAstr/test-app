from typing import Dict, List
from attr import define

import numpy as np



class Expression:
    
    def __init__(self, operation_txt:str, priority = 0) -> None:
        self.operation_txt = operation_txt
        self.priority = priority

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
        self.exp_list.append(Expression(string, priority))

    
    def convert_string_to_exprs(self, string:str) -> List[Expression]:
        self.exp_full_str = list(string)
        self.exp_full_str = self.fix_separated_numbers(self.exp_full_str)
        clean_list = self.extract_parenthesis(self.exp_full_str)
        self.rise_all_priorities()
        self.define_exp_for_prepared_data(clean_list)
        self.fix_complex_elements_in_exp_list()


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

        equation =  np.array(equation)
        for operator in self.supported:
            if any(np.isin(equation, operator)) :
                operator_index = np.argmax(equation == operator)
                if operator_index > 0:
                    new_exp = equation[operator_index-1 : operator_index+2].copy()
                    
                    self.add_expression_to_list(new_exp,1)
                    equation[operator_index+1] = f'self.exp_list[{self.get_free_exp_cell_idx()}]'
                    equation[operator_index-1 : operator_index+1] = ''
                    equation = equation[equation.nonzero()]
                    self.rise_all_priorities()
                    return equation.tolist()
          
 
    def rise_all_priorities(self):
        for e in self.exp_list: e.rise_priority()

    def get_free_exp_cell_idx(self):
            return len(self.exp_list)

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



    def extract_parenthesis(self, string:str):

        
        
        arr_no_parenth = []
        exp = []
        supported = list('*/+-')
        parenthesis = list('()')

        patenth_tmp = []
        parenth_idx = []
        right_parenth_cnt = 0

        for idx, char in enumerate(string[:]):
                if char == '(' :
                    parenth_idx.append(idx)
                    right_parenth_cnt +=1
                elif char == ')' :
                    parenth_idx.append(idx)
                    if len(parenth_idx) == 2:
                        parenthesis_exp = string[parenth_idx[0]:(parenth_idx[-1]+1)]
                        parenthesis_exp =  parenthesis_exp[1:-1]#parenthesis_exp.replace("(",'', 1).replace(")",'', 1)
                        arr_no_parenth.append(f'self.exp_list[{self.get_free_exp_cell_idx()}]')
                        self.add_expression_to_list(parenthesis_exp,1)
                        exp.append(parenthesis_exp)
                        parenth_idx = []
                        right_parenth_cnt = 0
                    elif len(parenth_idx)%2 == 0 and char == ')':
                        parenthesis_exp = string[parenth_idx[0]:(parenth_idx[-1]+1)]
                        parenthesis_exp = parenthesis_exp[1:-1]
                        _arr = self.extract_parenthesis(parenthesis_exp)
                        arr_no_parenth.append(_arr)
                        parenth_idx = []
                        right_parenth_cnt = 0
                    # else:
                    #     pass
                
                # elif right_parenth_cnt >1:
                #     right_parenth_cnt -=1                

                elif len(parenth_idx) == 0:
                    arr_no_parenth.append(char)
            
        # exp = [str.replace("(",'', 1).replace(")",'', 1) for str in exp] 
        return arr_no_parenth


