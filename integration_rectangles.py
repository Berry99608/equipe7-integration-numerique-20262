import numpy as np
import timeit


def evaluer_poly(x, p1, p2, p3, p4):
    # Fonctionne avec un scalaire ou un tableau NumPy
    return p1 + p2 * x + p3 * x**2 + p4 * x**3