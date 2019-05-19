from simplex_table import CalcDualSimplexTable
from expression import Expression
from data import get_task
from simplex_table import CalcComplexSimplexTable
from algorithms import branch_and_bounds 

task = get_task('Enter name of data file:\n>>> ')
print('File Owner: {}'.format(task['author']))

# extract constraints from the task
constraints = [Expression().set_object(constraint)
               for constraint in task['constraints']]

# extract objective function from the task
objective_function = Expression().set_object(task['objective_function'])

# check if accumulation is conserned
accumulation_is_conserned = task['accumulation_is_concerned']

# read intervals from the task
intervals = task['intervals']

# calculate a simplex table according to the task
st = CalcComplexSimplexTable(constraints, objective_function,
                             accumulation_is_conserned, intervals)

# show the task solution
print('RESULTS:')
print(branch_and_bounds(st, [])[0])
