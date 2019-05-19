from expression import Expression


def constraint_for_variable(vars, var_idx, sign):
    coeffs = [0 for i in range(len(vars))]
    coeffs[var_idx] = 1
    bound = vars[var_idx] // 1
    if sign is '>':
        bound += 1
    return Expression(coeffs, sign, bound)


def branch_and_bounds(simplex_table, integral_solutions=[]):
    solution = simplex_table.solve()
    if solution.is_feasible:
        if any([x % 1 != 0 for x in solution.get_X()]):
            Xs = solution.get_X()
            Xnum = solution.get_num_of_vars()
            for i in range(Xnum):
                if Xs[i] % 1 != 0:
                    left_bounded_table = simplex_table.copy().add_constraint(
                        constraint_for_variable(Xs, i, '<'))
                    right_bounded_table = simplex_table.copy().add_constraint(
                        constraint_for_variable(Xs, i, '>'))
                    left_bounded_solution = left_bounded_table.solve()
                    right_bounded_solution = right_bounded_table.solve()
                    if any([left_bounded_solution.is_feasible, right_bounded_solution.is_feasible]):
                        if left_bounded_solution.get_fun() >= right_bounded_solution.get_fun():
                            branch_and_bounds(
                                left_bounded_table, integral_solutions)
                            return integral_solutions
                        else:
                            branch_and_bounds(
                                right_bounded_table, integral_solutions)
                            return integral_solutions
                    return integral_solutions
        else:
            integral_solutions.append(solution)
    return integral_solutions
