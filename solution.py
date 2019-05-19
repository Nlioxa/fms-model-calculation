class Solution(object):
    def __init__(self, is_feasible, C=[], X=[], S=[]):
        self.is_feasible = is_feasible
        self.X = X
        self.S = S
        self.fun_B = self.calc_fun(C, False)
        self.fun_L = self.calc_fun(C, True)

    def calc_fun(self, C, is_integral):
        if self.is_feasible:
            fun = 0
            for i in range(len(C)):
                if is_integral:
                    fun += C[i]*round(self.X[i])
                else:
                    fun += C[i]*self.X[i]
            return fun
        else:
            return 0

    def __str__(self):
        result = 'x: \t{}\n'.format(
            self.X) + 'slack: \t{}\n'.format(self.S) + 'success: {}\n'.format(self.is_feasible)
        result += 'FB: \t{}\n'.format(self.fun_B) + \
            'FL: \t{}\n'.format(self.fun_L)
        return result

    def get_num_of_vars(self):
        return len(self.X)

    def get_X(self):
        return self.X

    def get_fun(self):
        return self.fun_B
