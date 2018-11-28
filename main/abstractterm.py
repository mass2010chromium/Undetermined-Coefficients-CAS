from __future__ import annotations

from abc import ABC, abstractmethod
import numbers

"""
Abstract term class.
"""


class AbstractTerm(ABC):

    def __init__(self):
        self.terms = None
        raise TypeError("Cannot instantiate AbstractTerm")

    @abstractmethod
    def derivative(self) -> AbstractTerm:
        pass

    """
    Tries to flatten this term into constant * blahblah, etc.
    """
    @abstractmethod
    def simplify(self) -> AbstractTerm:
        pass

    def __mul__(self, other):
        from main.multiplyterm import MultiplyTerm
        from main.simpleterm import SimpleTerm, TermTypes

        if isinstance(other, numbers.Number):
            return MultiplyTerm([self, SimpleTerm(TermTypes.POLYNOMIAL, other, 0)])
        elif isinstance(other, AbstractTerm):
            return MultiplyTerm([self, other])
        else:
            raise TypeError("Multiplying SimpleTerm with thing that is not a number or term")

    def __rmul__(self, other):
        from main.multiplyterm import MultiplyTerm
        from main.simpleterm import SimpleTerm, TermTypes

        if isinstance(other, numbers.Number):
            return MultiplyTerm([self, SimpleTerm(TermTypes.POLYNOMIAL, other, 0)])
        else:
            raise TypeError("Multiplying SimpleTerm with thing that is not a number or term")

    @staticmethod
    def increment_map(target_map, key, value):
        if key in target_map:
            target_map[key] = target_map[key] + value
        else:
            target_map[key] = value
