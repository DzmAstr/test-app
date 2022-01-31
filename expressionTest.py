from ExpressionSeparator import ExpressionSeparator as sepr
import ParallelCalculator as calc





string = '((1-1)+6+7)*2+3*(1-3+4)+10/2'

separ = sepr()


arr = separ.convert_string_to_exprs(string)


print(arr)

