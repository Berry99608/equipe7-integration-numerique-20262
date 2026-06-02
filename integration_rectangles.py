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

def rectangles_python(p1, p2, p3, p4, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h  # Point milieu du segment i
        total += evaluer_poly(x_mid, p1, p2, p3, p4)
    return total * h

def rectangles_numpy(p1, p2, p3, p4, a, b, n):
    h = (b - a) / n
    # Génère tous les points milieux en une seule opération vectorisée
    x_mid = np.linspace(a + h / 2, b - h / 2, n)
    return np.sum(evaluer_poly(x_mid, p1, p2, p3, p4)) * h
