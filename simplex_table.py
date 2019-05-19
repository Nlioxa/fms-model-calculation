from numpy import array
from scipy.optimize import linprog
from solution import Solution
from expression import Expression


class SimplexTable(object):
    def __init__(self, constraints, objective_function):
        self.constraints = constraints
        self.objective_function = objective_function
        self.solution = None

    def add_constraint(self, constraint):
        self.constraints.append(constraint)
        return self

    def remove_constraint(self, constraint):
        self.constraints.remove(constraint)
        return self

    def copy(self):
        copy_constraints = [c.copy() for c in self.constraints]
        copy_obj_func = self.objective_function.copy()
        copy_table = SimplexTable(copy_constraints, copy_obj_func)
        return copy_table

    def solve(self):
        if self.solution is None:
            A = [array(c.get_lt_coeffs()) * c.get_sign()
                 for c in self.constraints]
            B = [c.get_rt_coeff() * c.get_sign() for c in self.constraints]
            C = array(self.objective_function.get_lt_coeffs()) * \
                self.objective_function.get_sign()
            res = linprog(c=C,
                          A_ub=A,
                          b_ub=B)
            res['fun'] *= -1
            if res['success']:
                self.solution = Solution(
                    res['success'], self.objective_function.get_lt_coeffs(), res['x'], res['slack'])
            else:
                self.solution = Solution(res['success'])
        return self.solution


def CalcComplexSimplexTable(constraints, objective_function, accumulation_is_conserned, intervals):
    num_of_intervals = len(intervals)
    new_obj_func = objective_function.copy()
    for i in range(num_of_intervals - 1):
        new_obj_func.get_lt_coeffs().extend(objective_function.get_lt_coeffs())
    num_of_vars = objective_function.get_lt_coeffs().__len__()
    new_constraints = []
    for constraint in constraints:
        initial_lt_coeffs = constraint.get_lt_coeffs()
        initial_rt_coeff = constraint.get_rt_coeff()
        for i in range(num_of_intervals):
            rt_coeff = initial_rt_coeff * intervals[i] / sum(intervals)
            lt_coeffs = []
            start_pos = i * num_of_vars
            end_pos = (i + 1) * num_of_vars
            for j in range(num_of_vars*num_of_intervals):
                if j >= start_pos and j < end_pos:
                    lt_coeffs.append(
                        initial_lt_coeffs[constrain(j, num_of_vars)])
                else:
                    lt_coeffs.append(0)
            if constraint.is_accumulative and accumulation_is_conserned:
                if i > 0:
                    rt_coeff += new_constraints[-1].rt_coeff
                for k in range(i):
                    start_pos = num_of_vars*k
                    end_pos = num_of_vars*(k+1)
                    for j in range(num_of_vars):
                        lt_coeffs[j + start_pos] = initial_lt_coeffs[j]
            new_constraints.append(Expression(
                lt_coeffs, constraint.sign, rt_coeff))
    return SimplexTable(new_constraints, new_obj_func)


def CalcDualSimplexTable(simplex_table):
    primal_st = simplex_table.copy()
    primal_cnstrs = primal_st.constraints
    primal_obj_f = primal_st.objective_function
    for cnstr in primal_cnstrs:
        if cnstr.sign is '>':
            for i in range(cnstr.lt_coeffs.__len__()):
                cnstr.lt_coeffs[i] *= -1
            cnstr.rt_coeff *= -1
            cnstr.sign = '<'
    dual_obj_f = Expression([coeff.rt_coeff for coeff in primal_cnstrs], '<')
    dual_cnstrs = []
    num_of_dual_cnstrs = primal_obj_f.lt_coeffs.__len__()
    num_of_dual_vars = primal_cnstrs.__len__()
    for i in range(num_of_dual_cnstrs):
        lt_coeffs = []
        for j in range(num_of_dual_vars):
            lt_coeffs.append(primal_cnstrs[j].lt_coeffs[i])
        dual_cnstrs.append(Expression(
            lt_coeffs, '>', primal_obj_f.lt_coeffs[i]))
    return SimplexTable(dual_cnstrs, dual_obj_f)


def constrain(value, max_value):
    return value % max_value
