import unittest

from main.simpleterm import SimpleTerm, TermTypes
from main.multiplyterm import MultiplyTerm
# from main.variedcoefficient import VariedCoefficient


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # a = VariedCoefficient(A=1)
        # b = VariedCoefficient(B=1)
        self.term1 = SimpleTerm(TermTypes.POLYNOMIAL, -5, 1)
        self.term2 = SimpleTerm(TermTypes.EXPONENTIAL, 3, 3)
        self.term3 = SimpleTerm(TermTypes.POLYNOMIAL, 4, 3)
        self.term4 = SimpleTerm(TermTypes.SINE, 2, 8)

    def test_simplify_nested(self):
        self.mult_term = MultiplyTerm([self.term1, self.term2])
        self.assertEqual(str(self.mult_term.simplify()), "(-15) * (x) * (e^(3x))")

    def test_add_mult(self):
        # term5 = MultiplyTerm([AddTerm([self.term1, self.term2]),
        #                       AddTerm([self.term3, self.term4])])
        # self.assertEqual(str(term5.simplify()), "((-20) * (x^(4))) + ((-10) * (sin(8x)) * (x)) + "
        #                                         "((12) * (x^(3)) * (e^(3x))) + ((6) * (sin(8x)) * (e^(3x)))")

        # term6 = MultiplyTerm([AddTerm([self.term1, self.term2]),
        #                       AddTerm([self.term1, -1 * self.term2])]).simplify()
        # term_compare = AddTerm([SimpleTerm(TermTypes.POLYNOMIAL,
        #                                    self.term1.multiple ** 2,
        #                                    self.term1.power * 2),
        #                         SimpleTerm(TermTypes.EXPONENTIAL,
        #                                    -self.term2.multiple ** 2,
        #                                    self.term2.power * 2)]).simplify()
        # print(AddTerm([self.term1, self.term2]))
        # print(AddTerm([self.term1, -1 * self.term2]))
        # print(term6)
        # print(term_compare)
        pass


if __name__ == '__main__':
    unittest.main()
