from main.abstractterm import AbstractTerm
from main.variedcoefficient import VariedCoefficient
import numbers

"""
A single term. Can be polynomial, exponential, sine, or cosine.
"""


class SimpleTerm(AbstractTerm):

    def __init__(self, term_type, multiple, power: numbers.Number):
        if not (isinstance(multiple, numbers.Number) or isinstance(multiple, VariedCoefficient)):
            raise TypeError("Multiple must be a number or varied coefficient.")
        self.term_type = term_type
        self.multiple = multiple
        self.power = power
        self.terms = [self]

    def derivative(self):
        new_power = self.power
        new_type = self.term_type
        new_multiple = self.multiple * self.power
        if self.term_type == TermTypes.POLYNOMIAL:
            if new_power == 0:
                new_multiple = 0
            else:
                new_power = new_power - 1
        elif self.term_type == TermTypes.SINE:
            new_type = TermTypes.COSINE
        elif self.term_type == TermTypes.COSINE:
            new_type = TermTypes.SINE
            new_multiple *= -1
        return SimpleTerm(new_type, new_multiple, new_power)

    def __str__(self):
        if self.term_type == TermTypes.POLYNOMIAL:
            if self.power == 0:
                return str(self.multiple)
            elif self.power == 1:
                if self.multiple == 1:
                    return "x"
                else:
                    return str(self.multiple) + "x"
        retval = str(self.power)
        if self.term_type != TermTypes.POLYNOMIAL:
            retval = retval + "x"
        retval = str(self.term_type) + "(" + retval + ")"
        if self.multiple != 1:
            retval = str(self.multiple) + "*" + retval
        return retval

    def __eq__(self, other):
        if not isinstance(other, SimpleTerm):
            return False
        return self.term_type == other.term_type and self.multiple == other.multiple and self.power == other.power

    def __hash__(self):
        return hash((self.term_type, self.multiple, self.power))

    def simplify(self):
        return self
        # from main.multiplyTerm import MultiplyTerm
        # # IF there is a constant multiple
        # if not self.multiple == 1:
        #     # AND I am not already a constant
        #     if not self.term_type == TermTypes.POLYNOMIAL and self.power == 0:
        #         return MultiplyTerm(SimpleTerm(TermTypes.POLYNOMIAL, self.multiple, 0),
        #                             SimpleTerm(self.term_type, 1, self.power))

    def get_signature(self):
        return SimpleTerm(self.term_type, 1, self.power)


class TermTypes:
    POLYNOMIAL = "x^"
    EXPONENTIAL = "e^"
    SINE = "sin"
    COSINE = "cos"
