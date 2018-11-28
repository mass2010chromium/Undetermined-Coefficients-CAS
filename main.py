# from main.variedcoefficient import VariedCoefficient
from main.simpleterm import SimpleTerm, TermTypes
# from main.addterm import AddTerm
from main.multiplyterm import MultiplyTerm
from main.equation import Equation

# x = VariedCoefficient("A")
# x = x * 2 * 7
# print(x)
#
term1 = SimpleTerm(TermTypes.EXPONENTIAL, 3, 2)
term2 = SimpleTerm(TermTypes.POLYNOMIAL, -5, 2)
term4 = MultiplyTerm([SimpleTerm(TermTypes.COSINE, 1, 2),
                      SimpleTerm(TermTypes.POLYNOMIAL, 1, 1)]).simplify()
term5 = SimpleTerm(TermTypes.SINE, 3, 2)
# print(term1)
# print(term2)
# print(term5)
# print(term5.derivative())
# print(term5.simplify())

eqn1 = Equation(coef_list=[1, 0, 1], term_list=[term4, term5])
# eqn1 = Equation(coef_list=[1, 1, 1], term_list=[term2])
eqn1.init_solutions()
print(eqn1)

eqn1.solve_all_specific()
print(eqn1.specific_solutions[0])

eqn1.print_solutions()
