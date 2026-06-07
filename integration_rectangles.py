"""
integration_rectangles.py
=========================
Module 1 — MGA802 Mini-Projet B
Implémentation de la méthode des rectangles (point milieu) en Python pur
et en NumPy, ainsi que les fonctions utilitaires partagées par tous les modules.
"""

from numpy import linspace, sum as npsum
import timeit


def evaluer_poly(x, p1, p2, p3, p4):
    """
    Évalue le polynôme f(x) = p1 + p2·x + p3·x² + p4·x³.
    Fonctionne avec un scalaire ou un tableau NumPy
    Retourne : float ou nd.ndarray
    """
    return p1 + p2 * x + p3 * x**2 + p4 * x**3

def solution_analytique(p1, p2, p3, p4, a, b):
    """
    Calcule l'intégrale exacte de f sur [a, b] via la primitive.
    La primitive de f est :
        F(x) = p1·x + p2·x²/2 + p3·x³/3 + p4·x⁴/4
    L'intégrale vaut F(b) - F(a).
    Retourne : float - valeur exacte de l'intégrale
    """
    def F(x):
        return p1 * x + p2 * x**2 / 2 + p3 * x**3 / 3 + p4 * x**4 / 4
    return F(b) - F(a)

def rectangles_python(p1, p2, p3, p4, a, b, n):
    """
    Intégration par la méthode des rectangles (point milieu) — Python pur.
    L'intervalle [a, b] est divisé en n segments de largeur h = (b-a)/n.
    f est évaluée au centre de chaque segment x_i = a + (i + 0.5)·h.
    L'intégrale est approchée par la somme h · Σ f(x_i).
    Retourne : float - valeur approchée de l'intégrale
    """
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        total += evaluer_poly(x_mid, p1, p2, p3, p4)
    return total * h

def rectangles_numpy(p1, p2, p3, p4, a, b, n):
    """
    Intégration par la méthode des rectangles (point milieu) — NumPy vectorisé.
    Identique à rectangles_python mais sans boucle Python :
    tous les points milieux sont calculés en une seule opération NumPy.
    Retourne : float - valeur approchée de l'intégrale
    """
    h = (b - a) / n
    x_mid = linspace(a + h / 2, b - h / 2, n)
    return npsum(evaluer_poly(x_mid, p1, p2, p3, p4)) * h


def calculer_erreur(i_numerique, i_exact):
    """
    Retourne l'erreur absolue entre une valeur numérique et la valeur exacte.
    float - |i_numerique - i_exact|
    """
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
    """
    Mesure le temps moyen d'exécution des deux variantes rectangles via timeit.
    Retourne : tuple (float, float) - (temps_python, temps_numpy) en secondes par appel
    """
    temps_python = timeit.timeit(
        lambda: rectangles_python(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions
    temps_numpy = timeit.timeit(
        lambda: rectangles_numpy(p1, p2, p3, p4, a, b, n),
        number=repetitions
    ) / repetitions
    return temps_python, temps_numpy