from copy import deepcopy


class Expression(object):
    def __init__(self, lt_coeffs=[], sign='<', rt_coeff=0, is_accumulative=False):
        self.lt_coeffs = lt_coeffs
        self.rt_coeff = rt_coeff
        self.sign = sign
        self.is_accumulative = is_accumulative

    def set_object(self, jsonable):
        self.lt_coeffs = jsonable['lt_coeffs']
        self.rt_coeff = jsonable['rt_coeff']
        self.sign = jsonable['sign']
        self.is_accumulative = jsonable['is_accumulative']
        return self

    def get_sign(self):
        if self.sign is '<':
            return 1
        if self.sign is '>':
            return -1
        else:
            return 1

    def get_lt_coeffs(self):
        return self.lt_coeffs

    def get_rt_coeff(self):
        return self.rt_coeff

    def copy(self):
        copy_expression = Expression(deepcopy(self.lt_coeffs), deepcopy(
            self.sign), deepcopy(self.rt_coeff))
        return copy_expression

    def jsonable(self):
        data = {
            'lt_coeffs': self.lt_coeffs,
            'sign': self.sign,
            'rt_coeff': self.rt_coeff,
            'is_accumulative': self.is_accumulative
        }
        return data

    def inverse_sign(self):
        if self.sign is '<':
            self.sign = '>'
        else:
            self.sign = '<'
        return self
