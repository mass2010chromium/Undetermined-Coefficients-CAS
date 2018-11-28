from main.abstractterm import AbstractTerm
from main.simpleterm import SimpleTerm, TermTypes

from typing import List


class AddTerm(AbstractTerm):

    def __init__(self, terms: List[AbstractTerm]):
        self.terms = terms

    def derivative(self):
        return AddTerm(list([t.derivative() for t in self.terms]))

    def simplify(self):
        from main.multiplyterm import MultiplyTerm
        # "Flatten" any weird nested AddTerms.
        tmp_terms = [term.simplify() for term in self.terms]  # Possibly redundant
        terms = []
        for term in tmp_terms:
            if isinstance(term, AddTerm):
                terms = terms + term.terms
            else:
                terms.append(term)

        # REAL simplest case: Only one term.
        if len(terms) == 1:
            return terms[0]

        term_signatures = {}  # Signature, coef

        for term in terms:
            term = term.simplify()  # Simplify again after breaking up nested add terms
            signature = {}  # KEY: term, VALUE: count
            coef = 0
            if isinstance(term, MultiplyTerm):
                coef = term.get_coefficient_term().multiple
                signature = term.get_signature()
            elif isinstance(term, SimpleTerm):
                coef = term.multiple
                signature[SimpleTerm(term.term_type, 1, term.power)] = 1
            else:
                raise ValueError("Term Type not recognized!")
            frozen_key = frozenset(signature.items())
            AbstractTerm.increment_map(term_signatures, frozen_key, coef)
        retvals = []
        for signature in term_signatures:
            const_val = term_signatures[signature]
            if not (const_val == 0):
                # print(const_val)
                const_term = SimpleTerm(TermTypes.POLYNOMIAL, const_val, 0)
                retvals.append(MultiplyTerm([const_term] + list(dict(signature))))
        return AddTerm(retvals)

    def __str__(self):
        term_str = [(("(" + str(x) + ")") if not isinstance(x, AddTerm) else str(x))
                    for x in self.terms]
        return " + ".join(term_str)
