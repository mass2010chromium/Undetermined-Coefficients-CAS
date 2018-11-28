from main.abstractterm import AbstractTerm
from main.simpleterm import SimpleTerm, TermTypes
from main.addterm import AddTerm

import functools
import itertools

"""
Two terms multiplied together.
"""


class MultiplyTerm(AbstractTerm):

    def __init__(self, terms):
        self.terms = terms

    def derivative(self):
        iter_range = range(len(self.terms))
        return AddTerm([MultiplyTerm([self.terms[j].derivative() if j == i else self.terms[j]
                                     for j in iter_range])
                        for i in iter_range])

    def simplify(self):
        # Simplify, and "Flatten" any weird nested MultiplyTerms.
        tmp_terms = [term.simplify() for term in self.terms]
        terms = []
        # coef = self.coefficient
        # print(coef)
        for term in tmp_terms:
            if isinstance(term, MultiplyTerm):
                terms = terms + term.terms
                # coef *= term.coefficient
            else:
                terms.append(term)

        # REAL simplest case: Only one term.
        if len(terms) == 1:
            return terms[0]  # * coef

        # Stupid add terms screwing everything up
        add_terms = [term.terms for term in terms if isinstance(term, AddTerm)]
        other_terms = [term for term in terms if not isinstance(term, AddTerm)]

        # Split up the "other terms" into core components
        coefficient, polynom_accum, exp_accum, sin_cos_terms = MultiplyTerm.__split_expression(other_terms)

        # coefficient *= coef

        if len(add_terms) == 0:
            accumulated_terms = [SimpleTerm(TermTypes.POLYNOMIAL, coefficient, 0)]
            if not (polynom_accum == 0):
                accumulated_terms.append(SimpleTerm(TermTypes.POLYNOMIAL, 1, polynom_accum))
            if not (exp_accum == 0):
                accumulated_terms.append(SimpleTerm(TermTypes.EXPONENTIAL, 1, exp_accum))
            if (len(accumulated_terms) == 1) and (len(sin_cos_terms) == 0):
                return accumulated_terms[0]
            return MultiplyTerm(accumulated_terms + sin_cos_terms)

        retvals = []
        for combo in itertools.product(*add_terms):
            mult_tmp = MultiplyTerm(list(combo)).simplify()
            tmp_coef, tmp_polynom_accum, tmp_exp_accum, tmp_sin_cos_terms = \
                MultiplyTerm.__split_expression(mult_tmp.terms)
            total_coefficient = coefficient * tmp_coef
            if total_coefficient == 0:
                continue
            total_polynom_accum = polynom_accum + tmp_polynom_accum
            total_exp_accum = exp_accum + tmp_exp_accum
            total_sin_cos_terms = sin_cos_terms + tmp_sin_cos_terms
            accumulated_terms = [SimpleTerm(TermTypes.POLYNOMIAL, total_coefficient, 0)]
            if not (total_polynom_accum == 0):
                accumulated_terms.append(SimpleTerm(TermTypes.POLYNOMIAL, 1, total_polynom_accum))
            if not (total_exp_accum == 0):
                accumulated_terms.append(SimpleTerm(TermTypes.EXPONENTIAL, 1, total_exp_accum))

            if (len(accumulated_terms) == 1) and (len(total_sin_cos_terms) == 0):
                retvals.append(accumulated_terms[0])
            else:
                retvals.append(MultiplyTerm(accumulated_terms + total_sin_cos_terms))
        if len(retvals) == 0:
            return SimpleTerm(TermTypes.POLYNOMIAL, 0, 0)
        return AddTerm(retvals).simplify()

    def get_coefficient_term(self) -> SimpleTerm:
        # TODO FIX
        return self.terms[0]

    def get_signature(self):
        signature = {}  # KEY: term, VALUE: count
        for subterm in self.terms:
            if not ((subterm.term_type == TermTypes.POLYNOMIAL) and (subterm.power == 0)):
                subterm_sig = SimpleTerm(subterm.term_type, 1, subterm.power)
                AbstractTerm.increment_map(signature, subterm_sig, 1)
        return signature

    @staticmethod
    def __split_expression(terms):
        coefficient = functools.reduce(lambda x, y: x * y.multiple, terms, 1)
        exp_accum = 0
        polynom_accum = 0
        sin_cos_terms = []
        for term in terms:
            if (term.term_type == TermTypes.SINE) or (term.term_type == TermTypes.COSINE):
                sin_cos_terms.append(SimpleTerm(term.term_type, 1, term.power))
            elif term.term_type == TermTypes.POLYNOMIAL:
                polynom_accum += term.power
            elif term.term_type == TermTypes.EXPONENTIAL:
                exp_accum += term.power
            else:
                raise ValueError("Illegal Term Type!")
        return coefficient, polynom_accum, exp_accum, sin_cos_terms

    def __str__(self):
        term_str = [(("(" + str(x) + ")") if not isinstance(x, MultiplyTerm) else str(x))
                    for x in self.terms]
        return " * ".join(term_str)

