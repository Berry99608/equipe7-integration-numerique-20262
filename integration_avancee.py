"""
integration_avancee.py
======================
Module 2 — MGA802 Mini-Projet B
Implémentation des méthodes de trapèze et de Simpson (Python pur + NumPy).
Importe evaluer_poly, solution_analytique et calculer_erreur depuis
integration_rectangles pour éviter tout doublon de code.
"""

import timeit
from numpy import linspace, ones, dot
from integration_rectangles import evaluer_poly, solution_analytique, calculer_erreur
# ─────────────────────────────────────────────
# Méthode de Simpson
# ─────────────────────────────────────────────

def simpson_python(p1, p2, p3, p4, a, b, n):
    """
    Méthode de Simpson composite — boucle Python pure.
    Sur chaque segment [x_i, x_{i+1}], la formule de Simpson est :
        S_i = (h/3) · [f(x_i) + 4·f(milieu) + f(x_{i+1})]
    Ce qui, développé sur n segments, donne les coefficients 1,4,2,4,...,4,1.
    n est forcé pair car la formule classique l'exige.
    Retourne : float - valeur approchée de l'intégrale
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
    """
    Méthode de Simpson composite — vectorisée NumPy.
    Construit directement le vecteur de coefficients [1,4,2,4,...,4,1]
    et effectue un produit scalaire unique pour toute la somme.
    Retourne : float - valeur approchée de l'intégrale
    """
    if n % 2 != 0:
        n += 1

    x = linspace(a, b, n + 1)          # n+1 points : x_0 … x_n
    y = evaluer_poly(x, p1, p2, p3, p4)

    # Coefficients Simpson : 1, 4, 2, 4, 2, …, 4, 1
    coeffs = ones(n + 1)
    coeffs[1:-1:2] = 4   # indices impairs
    coeffs[2:-2:2] = 2   # indices pairs (sauf extrémités)

    h = (b - a) / n
    return dot(coeffs, y) * h / 3

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
    """
    Mesure le temps moyen d'exécution (en secondes) sur `repetitions` appels.
    Retourne : tuple (float, float) - (temps_python, temps_numpy) en secondes par appel
    """
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
    x = linspace(a, b, n + 1)          # n+1 points : x_0 … x_n
    y = evaluer_poly(x, p1, p2, p3, p4)

    # Coefficients trapèzes : 1, 2, 2, …, 2, 1
    coeffs = ones(n + 1)
    coeffs[1:-1] = 2                       # tous les points intérieurs

    h = (b - a) / n
    return dot(coeffs, y) * h / 2


#erreur absolue de chaque methode ,
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