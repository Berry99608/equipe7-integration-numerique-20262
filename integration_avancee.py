import numpy as np
from scipy import integrate
from integration_rectangles import *
# ─────────────────────────────────────────────
# Méthode de Simpson
# ─────────────────────────────────────────────

def simpson_python(p1, p2, p3, p4, a, b, n):
    """Méthode de Simpson composite — boucle Python pure.
    n doit être pair
    """
    if n % 2 != 0:
        n += 1  # Simpson exige un nombre pair de sous-intervalles

    h = (b - a) / n
    total = evaluer_poly(a, p1, p2, p3, p4) + evaluer_poly(b, p1, p2, p3, p4)

    for i in range(1, n):
        x_i = a + i * h
        if i % 2 == 0:
            total += 2 * evaluer_poly(x_i, p1, p2, p3, p4)  # points pairs
        else:
            total += 4 * evaluer_poly(x_i, p1, p2, p3, p4)  # points impairs

    return total * h / 3


def simpson_numpy(p1, p2, p3, p4, a, b, n):
    """Méthode de Simpson composite — vectorisée NumPy."""
    if n % 2 != 0:
        n += 1

    x = np.linspace(a, b, n + 1)          # n+1 points : x_0 … x_n
    y = evaluer_poly(x, p1, p2, p3, p4)

    # Coefficients Simpson : 1, 4, 2, 4, 2, …, 4, 1
    coeffs = np.ones(n + 1)
    coeffs[1:-1:2] = 4   # indices impairs
    coeffs[2:-2:2] = 2   # indices pairs (sauf extrémités)

    h = (b - a) / n
    return np.dot(coeffs, y) * h / 3

def erreur_vs_segments_simpson(p1, p2, p3, p4, a, b, liste_n):
    """Retourne les erreurs absolues de chaque méthode pour chaque n."""
    i_exact = solution_analytique(p1, p2, p3, p4, a, b)
    erreurs_python = []
    erreurs_numpy  = []

    for n in liste_n:
        i_python = simpson_python(p1, p2, p3, p4, a, b, n)
        i_numpy  = simpson_numpy (p1, p2, p3, p4, a, b, n)
        erreurs_python.append(calculer_erreur(i_python, i_exact))
        erreurs_numpy .append(calculer_erreur(i_numpy,  i_exact))

    return erreurs_python, erreurs_numpy


def mesurer_temps_simpson(p1, p2, p3, p4, a, b, n, repetitions=100):
    """Mesure le temps moyen d'exécution (en secondes) sur `repetitions` appels."""
    temps_python = timeit.timeit(
        lambda: simpson_python(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions

    temps_numpy = timeit.timeit(
        lambda: simpson_numpy(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions
    return temps_python, temps_numpy

# ─────────────────────────────────────────────
# Méthode des trapèzes
# ─────────────────────────────────────────────

def trapezes_python(p1, p2, p3, p4, a, b, n):
    """Méthode des trapèzes composite — boucle Python pure."""
    h = (b - a) / n
    total = evaluer_poly(a, p1, p2, p3, p4) + evaluer_poly(b, p1, p2, p3, p4)

    for i in range(1, n):
        x_i = a + i * h
        total += 2 * evaluer_poly(x_i, p1, p2, p3, p4)  # points intérieurs × 2

    return total * h / 2


def trapezes_numpy(p1, p2, p3, p4, a, b, n):
    """Méthode des trapèzes composite — vectorisée NumPy."""
    x = np.linspace(a, b, n + 1)          # n+1 points : x_0 … x_n
    y = evaluer_poly(x, p1, p2, p3, p4)

    # Coefficients trapèzes : 1, 2, 2, …, 2, 1
    coeffs = np.ones(n + 1)
    coeffs[1:-1] = 2                       # tous les points intérieurs

    h = (b - a) / n
    return np.dot(coeffs, y) * h / 2


def erreur_vs_segments_trapezes(p1, p2, p3, p4, a, b, liste_n):
    """Retourne les erreurs absolues de chaque méthode pour chaque n."""
    i_exact = solution_analytique(p1, p2, p3, p4, a, b)
    erreurs_python = []
    erreurs_numpy  = []

    for n in liste_n:
        i_python = trapezes_python(p1, p2, p3, p4, a, b, n)
        i_numpy  = trapezes_numpy (p1, p2, p3, p4, a, b, n)
        erreurs_python.append(calculer_erreur(i_python, i_exact))
        erreurs_numpy .append(calculer_erreur(i_numpy,  i_exact))

    return erreurs_python, erreurs_numpy


def mesurer_temps_trapezes(p1, p2, p3, p4, a, b, n, repetitions=100):
    """Mesure le temps moyen d'exécution (en secondes) sur `repetitions` appels."""
    temps_python = timeit.timeit(
        lambda: trapezes_python(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions

    temps_numpy = timeit.timeit(
        lambda: trapezes_numpy(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions

    return temps_python, temps_numpy