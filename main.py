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
from Analyse import construire_mesurer_temps, calculer_convergences, calculer_df_ref, afficher_synthese

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

#Fonction utilitaire
def lancer_experience(df_cas, label, prefixe):
    print(f"\n{'='*62}\n  {label}\n{'='*62}")
    print(df_cas.to_string(index=False))
    df_ref = calculer_df_ref(df_cas, FONCTIONS, MESURER_TEMPS, n_ref, REPETITIONS)
    convergence = calculer_convergences(df_cas, FONCTIONS, MESURER_TEMPS, Liste_n)
    afficher_synthese(df_ref, f"{label} - synthese")
    for cas, data in convergence.items():
        slug = cas[:8].strip().replace(" ", "_")
        graphique_convergence(Liste_n, data["dict_erreurs"], titre=f"{label} - Convergence - {cas}", save_path=f"{prefixe}_convergence_{slug}.png")
        graphique_temps(Liste_n, data["dict_temps"], titre=f"{label} - Temps - {cas}", save_path=f"{prefixe}_temps_{slug}.png")
        graphique_erreur_methodes(Liste_n, data["dict_erreurs"], titre=f"{label} - Erreur x methode - {cas}", save_path=f"{prefixe}_bubble_{slug}.png")
    df_ref.to_csv(f"{prefixe}_resultats.csv", index=False, float_format="%.6e")
    print(f"OK - {label} termine")
    return df_ref, convergence

#TEST
df_ref1, conv1 = lancer_experience(df_exp1, "EXP 1 — variation p", "exp1")

plt.show()
print("\nProjet termine.")