import copy
import numbers

"""
Variables! Woo
EDIT: WTF AM I DOING
"""


class VariedCoefficient:

    """
    Variable name "CONST" reserved for constant term.
    """
    CONST = "CONST"

    def __init__(self, **kwargs):
        self.variables = kwargs
        if VariedCoefficient.CONST not in self.variables:
            self.variables[VariedCoefficient.CONST] = 0

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return VariedCoefficient(**dict((name, self.variables[name] * other) for name in self.variables))
        else:
            raise TypeError("Varied Coefficients must be linear! Nonlinear methods not implemented!")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        tmp_vars = copy.deepcopy(self.variables)
        if isinstance(other, numbers.Number):
            tmp_vars[VariedCoefficient.CONST] = tmp_vars[VariedCoefficient.CONST] + other
        elif isinstance(other, VariedCoefficient):
            for var in other.variables:
                if var in tmp_vars:
                    tmp_vars[var] += other.variables[var]
                else:
                    tmp_vars[var] = other.variables[var]
        else:
            raise TypeError("Varied Coefficients can only be added to numbers or other V.C.")
        return VariedCoefficient(**tmp_vars)

    def __radd__(self, other):
        tmp_vars = copy.deepcopy(self.variables)
        if isinstance(other, numbers.Number):
            tmp_vars[VariedCoefficient.CONST] = tmp_vars[VariedCoefficient.CONST] + other
        else:
            raise TypeError("Varied Coefficients can only be added to numbers or other V.C.")
        return VariedCoefficient(**tmp_vars)

    def __eq__(self, other):
        if isinstance(other, VariedCoefficient):
            return self.variables == other.variables
        if isinstance(other, numbers.Number):
            return (len(list([x for x in self.variables if (self.variables[x] != 0) or x == VariedCoefficient.CONST])) == 1) \
                   and (VariedCoefficient.CONST in self.variables) \
                   and (self.variables[VariedCoefficient.CONST] == other)
        return False

    def __str__(self):
        retvals = []
        for variable in self.variables:
            if (not (variable == VariedCoefficient.CONST)) and (self.variables[variable] != 0):
                string = variable
                if self.variables[variable] != 1:
                    string = str(self.variables[variable]) + string
                retvals.append(string)
        if (VariedCoefficient.CONST in self.variables) and (not (self.variables[VariedCoefficient.CONST] == 0)):
            retvals.append(str(self.variables[VariedCoefficient.CONST]))
        if len(retvals) == 0:
            return "0"
        return " + ".join(retvals)
