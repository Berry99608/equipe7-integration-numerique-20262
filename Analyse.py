import numpy as np
from integration_rectangles import solution_analytique, calculer_erreur, mesurer_temps_rectangles
from integration_avancee import mesurer_temps_trapezes, mesurer_temps_simpson
from visualisation import scipy_trapezes, scipy_simpson, mesurer_temps
import pandas as pd

def construire_mesurer_temps(repetitions):
    r = repetitions
    return {"Rectangle Python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, r)[0],
            "Rectangle NumPy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, r)[1],
            "Trapeze Python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_trapezes(p1, p2, p3, p4, a, b, n, r)[0],
            "Trapeze NumPy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_trapezes(p1, p2, p3, p4, a, b, n, r)[1],
            "Simpson Python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_simpson(p1, p2, p3, p4, a, b, n, r)[0],
            "Simpson NumPy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_simpson(p1, p2, p3, p4, a, b, n, r)[1],
            "Scipy Trapeze": lambda p1, p2, p3, p4, a, b, n: mesurer_temps(scipy_trapezes, (p1, p2, p3, p4, a, b, n), r),
            "Scipy Simpson": lambda p1, p2, p3, p4, a, b, n: mesurer_temps(scipy_simpson, (p1, p2, p3, p4, a, b, n), r),}

def calculer_df_ref(df_cas, fonctions, mesurer_temps_dict, n_ref, repetitions):
    rows = []
    for _, row in df_cas.iterrows():
        p1,p2,p3,p4 = row["p1"], row["p2"], row["p3"], row["p4"]
        a, b        = row["a"], row["b"]
        i_exact     = solution_analytique(p1, p2, p3, p4, a, b)
        for methode, func in fonctions.items():
            i_num  = func(p1, p2, p3, p4, a, b, n_ref)
            erreur = calculer_erreur(i_num, i_exact)
            temps  = mesurer_temps_dict[methode](p1, p2, p3, p4, a, b, n_ref)
            rows.append({
                "cas":      row["cas"],
                "methode":  methode,
                "i_exact":  round(i_exact, 8),
                "i_num":    round(i_num,   8),
                "erreur":   erreur,
                "temps_us": temps * 1e6,})
    return pd.DataFrame(rows)

def calculer_convergences(df_cas, fonctions, mesurer_temps_dict, liste_n):
    resultats = {}
    for _, row in df_cas.iterrows():
        p1,p2,p3,p4 = row["p1"], row["p2"], row["p3"], row["p4"]
        a, b        = row["a"], row["b"]
        i_exact     = solution_analytique(p1, p2, p3, p4, a, b)
        d_err   = {m: [] for m in fonctions}
        d_temps = {m: [] for m in fonctions}
        for n in liste_n:
            for methode, func in fonctions.items():
                d_err[methode].append(calculer_erreur(func(p1,p2,p3,p4,a,b,n), i_exact))
                d_temps[methode].append(mesurer_temps_dict[methode](p1,p2,p3,p4,a,b,n))
        resultats[row["cas"]] = {"dict_erreurs": d_err, "dict_temps": d_temps}
    return resultats

def afficher_synthese(df_ref, titre):
    print(f"\n{'='*62}\n  {titre}\n{'='*62}")
    classement = df_ref.groupby("methode")["erreur"].mean().sort_values()
    print("\n  Classement global (erreur moyenne) :")
    print(classement.to_string(float_format=lambda x: f"{x:.3e}"))
    meilleurs = df_ref.loc[df_ref.groupby("cas")["erreur"].idxmin(),
                           ["cas", "methode", "erreur", "temps_us"]]
    print("\n  Meilleure méthode par cas :")
    print(meilleurs.to_string(index=False, float_format=lambda x: f"{x:.3e}"))