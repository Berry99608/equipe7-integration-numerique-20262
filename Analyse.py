"""
Analyse.py
==========
Module 4 — MGA802 Mini-Projet B
Orchestration des calculs d'analyse numérique:
    - construction du dictionnaire de fonctions de mesure de temps
    - calcul des erreurs et temps à n fixé
    - calcul des erreur et temps sur toute une liste de n
    - affichage console du classement et de la meilleure méthode par cas
"""

from integration_rectangles import solution_analytique, calculer_erreur, mesurer_temps_rectangles
from integration_avancee import mesurer_temps_trapezes, mesurer_temps_simpson
from visualisation import scipy_trapezes, scipy_simpson, mesurer_temps
from pandas import DataFrame

def construire_mesurer_temps(repetitions):
    """
    Construit et retourne le dictionnaire des fonctions de mesure de temps.
    Chaque entrée est une lambda qui prend les 4 coefficients, les 2 bornes et le nombre de répétitions n
    et retourne le temps moyen par appel en secondes pour la méthode correspondante
    Les fonctions mésurer temps retournent le temps python et le temps numpy, on sélectionne [0] (python pur) ou [1] (numpy pur) selon la variante
    """
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
    """
    Calcule erreur et temps à n_ref pour chaque combinaison cas x méthode
    Elle itère sur chaque ligne de DataFrame de cas, puis calcule la solution
    exacte et ensuite pour chaque méthode la valeur numérique, l'erreur, et le temps moyen d'exécution
    Retourne DataFrame : colonne cas, methode, i_exact, i_num, erreur, temps_us
    """
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
    return DataFrame(rows)

def calculer_convergences(df_cas, fonctions, mesurer_temps_dict, liste_n):
    """
    Calcule erreurs et temps sur toute la liste de n pour chaque cas.
    Pour chaque cas du DataFrame et pour chaque n de liste_n, calcule
    l'erreur absolue et le temps de chaque méthode. Résultat utilisé
    pour tracer les courbes de convergence et de temps.
    Retourne dict : {cas: {"dict_erreurs": {methode: [...]},
                            "dict_temps":   {methode: [...]}}}
    """
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
    """
    Affiche dans le terminal le classement global et la meilleure méthode par cas.
    Deux tableaux sont imprimés :
      1. Classement des méthodes par erreur moyenne sur tous les cas
      2. Meilleure méthode (erreur minimale) pour chaque cas
    """
    print(f"\n{'='*62}\n  {titre}\n{'='*62}")
    ordre = df_ref.groupby("methode")["erreur"].mean().sort_values().index
    classement = (df_ref.groupby("methode")[["erreur","temps_us"]]
                        .mean()
                        .loc[ordre]
                        .reset_index())
    print("\n  Classement global (erreur moyenne) :")
    print(classement.to_string(index=False,float_format=lambda x: f"{x:.3e}"))
    meilleurs = df_ref.loc[df_ref.groupby("cas")["erreur"].idxmin(),
                           ["cas", "methode", "erreur", "temps_us"]]
    print("\n  Meilleure méthode par cas :")
    print(meilleurs.to_string(index=False, float_format=lambda x: f"{x:.3e}"))