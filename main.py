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
from Analyse import construire_mesurer_temps

Liste_n = [5, 10, 20, 50, 100, 200, 500, 1000]
n_ref = 100
REPETITIONS = 100

FONCTIONS = {"Rectangle Python": rectangles_python,
             "Rectangle NumPy": rectangles_numpy,
             "Trapeze Python": trapezes_python,
             "Trapeze NumPy": trapezes_numpy,
             "Simpson Python": simpson_python,
             "Simpson NumPy": simpson_numpy,
             "Scipy Trapeze": scipy_trapezes,
             "Scipy Simpson": scipy_simpson,}

MESURER_TEMPS = construire_mesurer_temps(REPETITIONS)

#Tableaux pandas pour les données d'entrées

A_FIXE, B_FIXE = -2.0, 3.0
P1_FIXE, P2_FIXE, P3_FIXE, P4_FIXE = 1.0, -2.0, 0.5, 0.3

#TEST BORNES FIXES, COEFFICIENTS P VARIENT

df_exp1 = pd.DataFrame({
    "cas": ["cas 1", "cas 2", "cas 3", "cas 4", "cas 5"],
    "p1": [0.0, 1.0, 1.0, 5.0, 3.0],
    "p2": [1.0, 2.0, -2.0, -8.0, 0.0],
    "p3": [0.0, 1.0, 0.5, 3.0, 0.0],
    "p4": [0.0, 0.0, 0.3, 1.5, 0.0],
    "a": [A_FIXE] * 5,
    "b": [B_FIXE] * 5,})

#TEST COEFFICIENTS P FIXES, BORNES VARIENT

df_exp2 = pd.DataFrame({
    "cas": ["cas 1", "cas 2", "cas 3", "cas 4", "cas 5"],
    "p1": [P1_FIXE] * 5,
    "p2": [P2_FIXE] * 5,
    "p3": [P3_FIXE] * 5,
    "p4": [P4_FIXE] * 5,
    "a":  [ 0.0, -1.0, -5.0, -4.0, -3.0],
    "b":  [ 1.0,  2.0,  5.0, -1.0,  0.5],})

#TEST COEFFICIENTS P ET BORNES VARIENT SIMULTANÉMENT

df_exp3 = pd.DataFrame({
    "cas": ["cas A", "cas B", "cas C", "cas D", "cas E"],
    "p1": [ 2.0,  0.0, -1.0,  4.0, 3.1],
    "p2": [-3.0,  5.0,  2.0, -2.0, 2.6],
    "p3": [ 0.5, -1.5,  0.0,  1.0, 0.8],
    "p4": [ 0.2,  0.8, -0.5,  0.3, 4.0],
    "a":  [-3.0,  0.0, -1.0, -5.0, 6.0],
    "b":  [ 2.0,  4.0,  3.0,  1.0, 4.3],})
