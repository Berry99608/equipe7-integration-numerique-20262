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

# ─── Paramètres globaux ───────────────────────────────────────────────────────

Liste_n    = [5, 10, 20, 50, 100, 200, 500, 1000]
n_ref      = 100
REPETITIONS = 100

FONCTIONS = {
    "Rectangle Python": rectangles_python,
    "Rectangle NumPy":  rectangles_numpy,
    "Trapeze Python":   trapezes_python,
    "Trapeze NumPy":    trapezes_numpy,
    "Simpson Python":   simpson_python,
    "Simpson NumPy":    simpson_numpy,
    "Scipy Trapeze":    scipy_trapezes,
    "Scipy Simpson":    scipy_simpson,
}

MESURER_TEMPS = construire_mesurer_temps(REPETITIONS)

# ─── Valeurs par défaut ───────────────────────────────────────────────────────

A_FIXE, B_FIXE                   = -2.0, 3.0
P1_FIXE, P2_FIXE, P3_FIXE, P4_FIXE = 1.0, -2.0, 0.5, 0.3

df_exp1 = pd.DataFrame({
    "cas": ["cas 1", "cas 2", "cas 3", "cas 4", "cas 5"],
    "p1":  [0.0,  1.0,  1.0,  5.0, 3.0],
    "p2":  [1.0,  2.0, -2.0, -8.0, 0.0],
    "p3":  [0.0,  1.0,  0.5,  3.0, 0.0],
    "p4":  [0.0,  0.0,  0.3,  1.5, 0.0],
    "a":   [A_FIXE] * 5,
    "b":   [B_FIXE] * 5,
})

df_exp2 = pd.DataFrame({
    "cas": ["cas 1", "cas 2", "cas 3", "cas 4", "cas 5"],
    "p1":  [P1_FIXE] * 5,
    "p2":  [P2_FIXE] * 5,
    "p3":  [P3_FIXE] * 5,
    "p4":  [P4_FIXE] * 5,
    "a":   [ 0.0, -1.0, -5.0, -4.0, -3.0],
    "b":   [ 1.0,  2.0,  5.0, -1.0,  0.5],
})

df_exp3 = pd.DataFrame({
    "cas": ["cas A", "cas B", "cas C", "cas D", "cas E"],
    "p1":  [ 2.0,  0.0, -1.0,  4.0, 3.1],
    "p2":  [-3.0,  5.0,  2.0, -2.0, 2.6],
    "p3":  [ 0.5, -1.5,  0.0,  1.0, 0.8],
    "p4":  [ 0.2,  0.8, -0.5,  0.3, 4.0],
    "a":   [-3.0,  0.0, -1.0, -5.0, 6.0],
    "b":   [ 2.0,  4.0,  3.0,  1.0, 4.3],
})

# ─── Utilitaires d'interface ──────────────────────────────────────────────────

SEP = "=" * 62

def afficher_banniere():
    print(f"""
{SEP}
  MGA802 — Mini-Projet B : Intégration numérique
  Rectangles · Trapèzes · Simpson  (Python / NumPy / SciPy)
{SEP}

  Ce programme calcule l'intégrale :

        I = ∫[a,b]  p1 + p2·x + p3·x² + p4·x³  dx

  et compare la précision et le temps d'exécution de
  8 méthodes d'intégration numérique.
{SEP}""")


def demander_float(invite, defaut):
    rep = input(f"  {invite} (défaut = {defaut}) : ").strip()
    if rep == "":
        return defaut
    try:
        return float(rep)
    except ValueError:
        print("  Valeur invalide — valeur par défaut utilisée.")
        return defaut


def saisir_parametres():
    print(f"\n  f(x) = p1 + p2·x + p3·x² + p4·x³")
    print("  Appuyez sur Entrée pour conserver la valeur par défaut.\n")
    p1 = demander_float("p1", P1_FIXE)
    p2 = demander_float("p2", P2_FIXE)
    p3 = demander_float("p3", P3_FIXE)
    p4 = demander_float("p4", P4_FIXE)
    print()
    a = demander_float("a  (borne inférieure)", A_FIXE)
    b = demander_float("b  (borne supérieure)", B_FIXE)
    if a >= b:
        print("  Attention : a >= b — les bornes ont été inversées.")
        a, b = b, a
    return p1, p2, p3, p4, a, b


# ─── Affichage des résultats numériques ───────────────────────────────────────

def afficher_resultats(p1, p2, p3, p4, a, b):
    print(f"\n  Calcul avec n = {n_ref} segments...")
    i_exact = solution_analytique(p1, p2, p3, p4, a, b)
    print(f"\n  Solution analytique exacte  : {i_exact:.10f}\n")
    print(f"  {'Méthode':<22} {'Résultat':>14} {'Erreur abs.':>14} {'Temps (µs)':>12}")
    print(f"  {'─'*64}")
    for nom, func in FONCTIONS.items():
        i_num = func(p1, p2, p3, p4, a, b, n_ref)
        err   = calculer_erreur(i_num, i_exact)
        tps   = MESURER_TEMPS[nom](p1, p2, p3, p4, a, b, n_ref) * 1e6
        print(f"  {nom:<22} {i_num:>14.8f} {err:>14.3e} {tps:>12.2f}")
    print()


# ─── Menu graphiques ──────────────────────────────────────────────────────────

def menu_graphiques(p1, p2, p3, p4, a, b):
    print(f"\n  {'─'*50}")
    print("  Graphiques disponibles :")
    print("    [1] Convergence  — erreur absolue vs nombre de segments")
    print("    [2] Temps        — temps de calcul vs nombre de segments")
    print("    [3] Comparaison  — erreur par méthode et par n (bulles)")
    print("    [4] Tous les graphiques")
    print("    [0] Passer")
    print(f"  {'─'*50}")
    choix = input("  Votre choix : ").strip()

    if choix not in ("1", "2", "3", "4"):
        return

    i_exact = solution_analytique(p1, p2, p3, p4, a, b)

    print("\n  Calcul des erreurs sur tous les n...")
    dict_erreurs = {
        nom: [calculer_erreur(func(p1, p2, p3, p4, a, b, n), i_exact) for n in Liste_n]
        for nom, func in FONCTIONS.items()
    }

    if choix in ("2", "4"):
        print("  Mesure des temps d'exécution (quelques secondes)...")
        dict_temps = {
            nom: [MESURER_TEMPS[nom](p1, p2, p3, p4, a, b, n) for n in Liste_n]
            for nom in FONCTIONS
        }

    if choix in ("1", "4"):
        graphique_convergence(Liste_n, dict_erreurs)

    if choix in ("2", "4"):
        graphique_temps(Liste_n, dict_temps)

    if choix in ("3", "4"):
        graphique_erreur_methodes(Liste_n, dict_erreurs)

    plt.show()


# ─── Expériences prédéfinies ──────────────────────────────────────────────────

def lancer_experience(df_cas, label, prefixe):
    print(f"\n{SEP}\n  {label}\n{SEP}")
    print(f"\n  Cas de test :\n")
    print(df_cas.to_string(index=False))

    print(f"\n  Calcul des résultats à n = {n_ref} segments...")
    df_ref = calculer_df_ref(df_cas, FONCTIONS, MESURER_TEMPS, n_ref, REPETITIONS)

    print("  Calcul des convergences sur tous les n...")
    convergence = calculer_convergences(df_cas, FONCTIONS, MESURER_TEMPS, Liste_n)

    afficher_synthese(df_ref, f"{label} — synthèse")

    # Un seul jeu de 3 graphiques par expérience (cas représentatif = premier cas)
    cas_rep, data_rep = next(iter(convergence.items()))
    print(f"\n  Génération des graphiques (cas représentatif : {cas_rep})...")
    graphique_convergence(Liste_n, data_rep["dict_erreurs"], titre=f"{label} — Convergence")
    graphique_temps(Liste_n, data_rep["dict_temps"], titre=f"{label} — Temps de calcul")
    graphique_erreur_methodes(Liste_n, data_rep["dict_erreurs"], titre=f"{label} — Erreur par méthode")
    print(f"    3 graphiques générés.")

    df_ref.to_csv(f"{prefixe}_resultats.csv", index=False, float_format="%.6e")
    print(f"\n  Résultats exportés dans : {prefixe}_resultats.csv")
    print(f"  {label} terminée.")
    return df_ref, convergence


EXPERIENCES = {
    "1": (df_exp1, "EXP 1 — coefficients p varient, bornes fixes",      "exp1"),
    "2": (df_exp2, "EXP 2 — bornes varient, coefficients p fixes",       "exp2"),
    "3": (df_exp3, "EXP 3 — coefficients p et bornes varient ensemble",  "exp3"),
}


# ─── Programme principal ──────────────────────────────────────────────────────

def main():
    afficher_banniere()

    while True:
        print("""
  Menu principal
  ─────────────────────────────────────────
  [1]  Entrer mes propres valeurs
  [2]  Utiliser les expériences par défaut
  [0]  Quitter
  ─────────────────────────────────────────""")
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            p1, p2, p3, p4, a, b = saisir_parametres()
            print(f"\n  Polynôme : f(x) = {p1} + {p2}·x + {p3}·x² + {p4}·x³  sur [{a}, {b}]")
            afficher_resultats(p1, p2, p3, p4, a, b)
            menu_graphiques(p1, p2, p3, p4, a, b)

        elif choix == "2":
            print("""
  Expériences disponibles
  ─────────────────────────────────────────
  [1]  EXP 1 — coefficients p varient, bornes fixes
  [2]  EXP 2 — bornes varient, coefficients p fixes
  [3]  EXP 3 — coefficients p et bornes varient ensemble
  [4]  Toutes les expériences
  [0]  Retour
  ─────────────────────────────────────────""")
            sub = input("  Votre choix : ").strip()
            if sub == "4":
                for df, label, pref in EXPERIENCES.values():
                    lancer_experience(df, label, pref)
            elif sub in EXPERIENCES:
                df, label, pref = EXPERIENCES[sub]
                lancer_experience(df, label, pref)
            elif sub != "0":
                print("  Choix invalide.")
                continue
            if sub in ("1", "2", "3", "4"):
                plt.show()

        elif choix == "0":
            print("\n  Au revoir !\n")
            break

        else:
            print("  Choix invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()
