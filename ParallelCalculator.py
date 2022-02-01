import ray
import numpy as np

import time 


from ExpressionSeparator import ExpressionSeparator , Expression

ray.init()

@ray.remote
def send_result(res):
    pass

@ray.remote
def count_expression(larg, rarg, operation, operation_id = 0):   
    tmp = 0
    if type(larg) == type('') and type(rarg) == type(''):
        tmp = eval(larg + operation + rarg)
    elif type(rarg) == type('') and type(larg) != type('') :
        tmp = eval(str(larg) + operation + rarg)
    elif type(rarg) != type('') and type(larg) == type('') :
        tmp = eval(larg + operation + str(rarg))
    elif type(rarg) != type('') and type(larg) != type('') :
        tmp = eval(str(larg) + operation + str(rarg))
    time.sleep(3)
    print(f'operation = {larg , operation , rarg} = {tmp}, id = {operation_id}, time = {time.time()}')
    return tmp


class ParallelCalculator:
    
    def __init__(self) -> None:
        self.exp_list = []
        self.exp_result = []
        self.separator = ExpressionSeparator()

    def delegate_operations_exec_from_exp_list(self):
        # exp_sorted = sorted(self.exp_list, key=lambda ex: ex.priority, reverse=True)

        operations = []
        tmp_arr = []
        for idx, exp in enumerate(self.exp_list):
            # operations.append( "".join(exp.operation_txt))
            
            larg = exp.larg
            rarg = exp.rarg
            operation = exp.operation
            
            if 'exp' in exp.larg:                
                tmp = eval(exp.larg)
                larg = self.exp_result[tmp.id]                

            if 'exp' in exp.rarg:
                tmp = eval(exp.rarg)
                rarg = self.exp_result[tmp.id]    
            

            self.exp_result[idx] = count_expression.remote(larg, rarg, operation, exp.id) #.remote

        while(1):
            pass


        
    def count_value_from_string(self, string):
        self.exp_list = self.separator.convert_string_to_exprs(string)
        self.exp_result = np.zeros(len(self.exp_list), dtype= object)
        self.delegate_operations_exec_from_exp_list()
