from collections import deque
import math

from main.addterm import AddTerm
from main.simpleterm import SimpleTerm, TermTypes
from main.variedcoefficient import VariedCoefficient
from main.multiplyterm import MultiplyTerm
from main.abstractterm import AbstractTerm

"""
An equation! Holds terms, should be able to collect and cancel
All add to 0.
"""


class Equation:

    Y_PP = "Y''"
    Y_P = "Y'"
    Y = "Y"

    C1 = "C1"
    C2 = "C2"

    """
    Coef list: y'', y', y
    """
    def __init__(self, coef_list, term_list):
        self.coefs = VariedCoefficient(**{Equation.Y_PP: coef_list[0],
                                          Equation.Y_P: coef_list[1],
                                          Equation.Y: coef_list[2]})

        self.terms = AddTerm(term_list).simplify()

        self.specific_solutions = []
        self.homogenous_solutions = []
        self.var_num = ord('A')  # A, B, C...

    def init_solutions(self):

        self.solve_homogenous()

        homogenous_signatures = [solution.get_signature() for solution in self.homogenous_solutions]
        # for term in homogenous_signatures:
        #     for blah in term:
        #         print(blah, term[blah])
        #     print()
        #     # print(term)

        self.var_num = ord('A')
        self.specific_solutions = []
        for term in self.terms.terms:
            solution_terms = []
            subterms = term.terms
            for subterm in subterms:
                if not isinstance(subterm, SimpleTerm):
                    raise ValueError("Solution init error: Terms not simplified correctly!")
                term_type = subterm.term_type
                if term_type == TermTypes.POLYNOMIAL:
                    polynom_terms = []
                    for i in range(subterm.power + 1):
                        polynom_terms.append(SimpleTerm(TermTypes.POLYNOMIAL, 1, i))
                    solution_terms.append(AddTerm(polynom_terms))
                elif term_type == TermTypes.EXPONENTIAL:
                    solution_terms.append(SimpleTerm(TermTypes.EXPONENTIAL, 1, subterm.power))
                elif (term_type == TermTypes.SINE) or term_type == TermTypes.COSINE:
                    solution_terms.append(AddTerm([SimpleTerm(TermTypes.SINE, 1, subterm.power),
                                                   SimpleTerm(TermTypes.COSINE, 1, subterm.power)]))

            solution_form = MultiplyTerm(solution_terms)
            solution_form = solution_form.simplify()
            names = []
            repeats = 0
            for polyterm in solution_form.terms:

                # Check for solutions that are already part of the general solution
                for signature in homogenous_signatures:
                    if polyterm.get_signature() == signature:
                        repeats += 1

                name = self.__get_next_available_name()
                names.append(name)
                coef = VariedCoefficient(**{name: 1})
                if isinstance(polyterm, SimpleTerm):
                    polyterm.multiple = coef
                    continue
                if not isinstance(polyterm, MultiplyTerm):
                    raise ValueError("Solving error: Failed to simplify properly")
                polyterm.get_coefficient_term().multiple = coef

            # Multiply by t^s
            if not (repeats == 0):
                solution_form = (solution_form * SimpleTerm(TermTypes.POLYNOMIAL, 1, repeats)).simplify()

            self.specific_solutions.append((solution_form, term, names))

    def __get_next_available_name(self):
        var_name = chr(self.var_num)
        self.var_num += 1
        return var_name

    def solve_homogenous(self):
        self.homogenous_solutions = [None, None]
        a = self.coefs.variables[Equation.Y_PP]
        b = self.coefs.variables[Equation.Y_P]
        c = self.coefs.variables[Equation.Y]
        bsq_4ac = b ** 2 - 4 * c * a
        if bsq_4ac > 0:
            # Standard two exponential solutions
            root1 = (-b + math.sqrt(bsq_4ac)) / (2 * a)
            root2 = (-b - math.sqrt(bsq_4ac)) / (2 * a)
            self.homogenous_solutions[0] = SimpleTerm(TermTypes.EXPONENTIAL,
                                                      VariedCoefficient(**{Equation.C1: 1}), root1)
            self.homogenous_solutions[1] = SimpleTerm(TermTypes.EXPONENTIAL,
                                                      VariedCoefficient(**{Equation.C2: 1}), root2)
        elif bsq_4ac < 0:
            # Periodic solution
            b_2a = -b / (2 * a)
            freq_term = math.sqrt(-bsq_4ac)
            self.homogenous_solutions[0] = MultiplyTerm([SimpleTerm(TermTypes.EXPONENTIAL,
                                                                    VariedCoefficient(**{Equation.C1: 1}), b_2a),
                                                         SimpleTerm(TermTypes.SINE, 1, freq_term)])
            self.homogenous_solutions[1] = MultiplyTerm([SimpleTerm(TermTypes.EXPONENTIAL,
                                                                    VariedCoefficient(**{Equation.C2: 1}), b_2a),
                                                         SimpleTerm(TermTypes.COSINE, 1, freq_term)])
        else:
            # Repeated roots
            b_2a = -b / (2 * a)
            self.homogenous_solutions[0] = SimpleTerm(TermTypes.EXPONENTIAL,
                                                      VariedCoefficient(**{Equation.C1: 1}), b_2a)
            self.homogenous_solutions[1] = MultiplyTerm([SimpleTerm(TermTypes.POLYNOMIAL,
                                                                    VariedCoefficient(**{Equation.C2: 1}), 1),
                                                         SimpleTerm(TermTypes.EXPONENTIAL, 1, b_2a)])
        self.homogenous_solutions = list([soln.simplify() for soln in self.homogenous_solutions])

    def solve_all_specific(self):
        self.specific_solutions = [self.solve_specific(solution) for solution in self.specific_solutions]

    def solve_specific(self, solution):
        form = solution[0]  # * SimpleTerm(TermTypes.POLYNOMIAL, 1, 1)).simplify()
        target = solution[1]
        names = solution[2] + [VariedCoefficient.CONST]
        if not isinstance(form, AbstractTerm):
            raise TypeError("Solve: Solution has to be a term!")

        d1 = form.derivative()
        d2 = d1.derivative()

        ypp_coef = self.coefs.variables[Equation.Y_PP]
        yp_coef = self.coefs.variables[Equation.Y_P]
        y_coef = self.coefs.variables[Equation.Y]
        y_term = (y_coef * form).simplify()
        yp_term = (yp_coef * d1).simplify()
        ypp_term = (ypp_coef * d2).simplify()
        # print(ypp_term)
        # print(yp_term)
        # print(y_term)

        total_eqn = AddTerm([ypp_term, yp_term, y_term, -1 * target]).simplify()

        # print()
        # print(total_eqn)

        eqn_list = []
        # print(total_eqn)

        for category in total_eqn.terms:
            coef = category.terms[0].multiple
            if not isinstance(coef, VariedCoefficient):
                raise ValueError("Cannot solve equation!")
            eqn_terms = coef.variables
            eqn_list.append(eqn_terms)

        solutions = Equation.solve_linear_equations(eqn_list, names)

        # print(solutions)
        # print(form)

        if isinstance(form, AddTerm):
            for i in range(len(names) - 1):
                term = form.terms[i]
                # print(term)
                if not isinstance(term, MultiplyTerm):
                    raise ValueError("Failed to simplify properly! Somehow...")
                term.get_coefficient_term().multiple = solutions[names[i]]
        elif isinstance(form, MultiplyTerm):
            form.get_coefficient_term().multiple = solutions[names[0]]
        elif isinstance(form, SimpleTerm):
            form.multiple = solutions[names[0]]
        else:
            raise ValueError("Invalid term type??")
        return form.simplify()



    @staticmethod
    def solve_linear_equations(equations, names):
        # Normalize each row, and eliminate.

        n = len(equations)

        # Convert matrix to a diagonal matrix with ones down the diagonal.
        for i in range(n):

            # find equation with a nonzero term
            eqn = equations[i]
            leading_term = eqn.get(names[i])
            if leading_term == 0:
                # Find an equation that has a nonzero leading term
                sublist = deque(equations[i:])
                for not_infinite in range(n):
                    sublist.rotate()
                    row = list(sublist)[0]
                    # print(row)
                    if names[i] in row:
                        leading_term = list(sublist)[0].get(names[i])
                        if leading_term != 0:
                            break
                equations[i:] = list(sublist)

            if leading_term == 0:
                raise ValueError("FAILED TO FIND SOLUTION")

            # Normalize Equation
            eqn = {term: (eqn[term] / leading_term) for term in eqn}

            equations[i] = eqn

            for j in range(i+1, n):
                row = equations[j]
                if (names[i] not in row) or (row[names[i]] == 0):
                    continue
                cancel_term = row[names[i]]
                for name in names:
                    if (name in eqn) and (name in row):
                        row[name] -= cancel_term * eqn[name]
                equations[j] = row

        # print(equations)

        # Back substitute time!
        var_values = {}
        for i in range(n-1, -1, -1):
            term_sums = 0
            for j in range(n-1, i, -1):
                term_sums += var_values[names[j]] * equations[i][names[j]]
            term_sums += equations[i][VariedCoefficient.CONST]
            var_values[names[i]] = -term_sums
        # print(var_values)
        return var_values

    def __str__(self):
        return "{ " + str(self.coefs) + " = " + str(self.terms) + " }"
