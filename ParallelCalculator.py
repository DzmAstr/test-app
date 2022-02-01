import ray
import numpy as np
import time 

from ExpressionSeparator import ExpressionSeparator 


ray.init()


@ray.remote
def count_expression(larg, rarg, operation, operation_id = 0):   

    tmp = eval(str(larg) + operation + str(rarg))
    # print(f'operation = {larg , operation , rarg} = {tmp}, id = {operation_id}, time = {time.time()}')
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


        
    def count_value_from_string(self, string):
        self.exp_list = self.separator.convert_string_to_exprs(string)
        self.exp_result = np.zeros(len(self.exp_list), dtype= object)
        self.delegate_operations_exec_from_exp_list()
        return ray.get(self.exp_result[-1])


