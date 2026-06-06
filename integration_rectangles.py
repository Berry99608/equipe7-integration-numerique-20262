from numpy import linspace, sum as npsum
import timeit


def evaluer_poly(x, p1, p2, p3, p4):
    # Fonctionne avec un scalaire ou un tableau NumPy
    return p1 + p2 * x + p3 * x**2 + p4 * x**3

def solution_analytique(p1, p2, p3, p4, a, b):
    def F(x):
        return p1 * x + p2 * x**2 / 2 + p3 * x**3 / 3 + p4 * x**4 / 4
    return F(b) - F(a)

def rectangles_python(p1, p2, p3, p4, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        total += evaluer_poly(x_mid, p1, p2, p3, p4)
    return total * h

def rectangles_numpy(p1, p2, p3, p4, a, b, n):
    h = (b - a) / n
    x_mid = linspace(a + h / 2, b - h / 2, n)
    return npsum(evaluer_poly(x_mid, p1, p2, p3, p4)) * h


def calculer_erreur(i_numerique, i_exact):
    return abs(i_numerique - i_exact)


def erreur_vs_segments(p1, p2, p3, p4, a, b, liste_n):
    i_exact = solution_analytique(p1, p2, p3, p4, a, b)
    erreurs_python = []
    erreurs_numpy = []
    for n in liste_n:
        i_python = rectangles_python(p1, p2, p3, p4, a, b, n)
        i_numpy = rectangles_numpy(p1, p2, p3, p4, a, b, n)
        erreurs_python.append(calculer_erreur(i_python, i_exact))
        erreurs_numpy.append(calculer_erreur(i_numpy, i_exact))
    return erreurs_python, erreurs_numpy

def mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, repetitions=100):
    temps_python = timeit.timeit(
        lambda: rectangles_python(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions
    temps_numpy = timeit.timeit(
        lambda: rectangles_numpy(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions
    return temps_python, temps_numpy