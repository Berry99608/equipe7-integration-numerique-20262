import numpy as np
import timeit


def evaluer_poly(x, p1, p2, p3, p4):
    # Fonctionne avec un scalaire ou un tableau NumPy
    return p1 + p2 * x + p3 * x**2 + p4 * x**3

def solution_analytique(p1, p2, p3, p4, a, b):
    # Antidérivée de f(x) : F(x) = p1*x + p2*x²/2 + p3*x³/3 + p4*x⁴/4
    def antiderivee(x):
        return p1 * x + p2 * x**2 / 2 + p3 * x**3 / 3 + p4 * x**4 / 4
    return antiderivee(b) - antiderivee(a)
