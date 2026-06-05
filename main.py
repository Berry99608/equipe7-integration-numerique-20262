"""
main.py
=======
MGA802 — Mini-Projet B : Intégration numérique
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from integration_rectangles import solution_analytique, rectangles_python, rectangles_numpy, calculer_erreur
from integration_avancee import trapezes_numpy, trapezes_python, simpson_numpy, simpson_python
from visualisation import scipy_trapezes, scipy_simpson, graphique_convergence, graphique_temps, graphique_erreur_methodes

Liste_n = [5, 10, 20, 50, 100, 200, 500, 1000]
n_ref = 100
repetitions = 100

FONCTIONS = {"Rectangle Python": rectangles_python,
             "Rectangle NumPy": rectangles_numpy,
             "Trapeze Python": trapezes_python,
             "Trapeze NumPy": trapezes_numpy,
             "Simpson Python": simpson_python,
             "Simpson NumPy": simpson_python,
             "Scipy Trapeze": scipy_trapezes,
             "Scipy Simpson": scipy_simpson,}

