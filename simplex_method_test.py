from data import read_data, get_task
from simplex_table import SimplexTable, CalcComplexSimplexTable, Expression

task = get_task('Enter name of data file:\n>>> ')
print('File Owner: {}'.format(task['author']))


# extract constraints from the task
constraints = [Expression().set_object(item) for item in task['constraints']]

# extract objective function from the task
objective_function = Expression().set_object(task['objective_function'])

# solve the task
solution = SimplexTable(constraints, objective_function).solve()

# show the task
print(solution)
