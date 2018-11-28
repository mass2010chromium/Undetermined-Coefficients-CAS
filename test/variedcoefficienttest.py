import unittest

from main.variedcoefficient import VariedCoefficient


class MyTestCase(unittest.TestCase):

    def test_str(self):
        string = str(VariedCoefficient(CONST=1,X=2))
        self.assertEqual(string, "2X + 1")

    def test_add(self):
        var1 = VariedCoefficient(X=2, Y=4, CONST=4)
        var2 = VariedCoefficient(CONST=-3, X=1, Y=-3)
        var3 = var1 + var2
        var_compare = VariedCoefficient(X=3, Y=1, CONST=1)
        self.assertEqual(var3.variables, var_compare.variables)

        var4 = VariedCoefficient(A=3, B=5, X=2)
        var5 = var1 + var4
        var6 = var4 + var1
        var_compare_2 = VariedCoefficient(A=3, B=5, X=4, Y=4, CONST=4)
        self.assertEqual(var5.variables, var_compare_2.variables)
        self.assertEqual(var6.variables, var_compare_2.variables)

        var7 = var1 + 6
        var8 = 6 + var1
        var_compare_3 = VariedCoefficient(X=2, Y=4, CONST=10)
        self.assertEqual(var7.variables, var_compare_3.variables)
        self.assertEqual(var8.variables, var_compare_3.variables)

    def test_mult(self):
        var1 = VariedCoefficient(X=2, Y=4, CONST=4)
        var2 = var1 * 4
        var3 = 4 * var1
        var4 = VariedCoefficient(X=8, Y=16, CONST=16)
        self.assertEqual(var2.variables, var4.variables)
        self.assertEqual(var3.variables, var4.variables)

if __name__ == '__main__':
    unittest.main()
