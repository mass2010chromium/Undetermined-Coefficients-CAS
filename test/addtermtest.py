import unittest

from main.simpleterm import SimpleTerm, TermTypes
from main.multiplyterm import MultiplyTerm
from main.addterm import AddTerm
from main.variedcoefficient import VariedCoefficient


class MyTestCase(unittest.TestCase):

    def setUp(self):
        a = VariedCoefficient(A=1)
        b = VariedCoefficient(B=1)
        self.term1 = AddTerm([MultiplyTerm([SimpleTerm(TermTypes.POLYNOMIAL, b, 0),
                                            SimpleTerm(TermTypes.POLYNOMIAL, 1, 0)]),
                              SimpleTerm(TermTypes.POLYNOMIAL, a, 0),
                              SimpleTerm(TermTypes.POLYNOMIAL, 6, 0),
                              SimpleTerm(TermTypes.POLYNOMIAL, b + 5, 1)])

    def test_simplify_const(self):
        print(self.term5)
        print(self.term5.simplify())


if __name__ == '__main__':
    unittest.main()
