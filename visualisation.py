import timeit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import integrate
from integration_rectangles import evaluer_poly

_COULEURS = ["#0072BD", "#D95319", "#EDB120", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F"]
_EPAISSEUR = [1.2, 2.2, 1.2, 2.2, 1.2, 2.2, 1.8, 1.8]
_STYLES = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
_MARKERS = ["o", "s", "^", "v", "D", "P", "*", "X"]

_NOMS = ["Rectangle Python", "Rectangle NumPy",
         "Trapeze Python", "Trapeze NumPy",
         "Simpson Python", "Simpson NumPy",
         "SciPy Trapeze",  "SciPy Simpson"]

STYLE_PAR_METHODE = {nom: {"couleur": _COULEURS[i % 7], "trait": _STYLES[i],
                      "epaisseur": _EPAISSEUR[i], "marker": _MARKERS[i], "ms": 5}
                for i, nom in enumerate(_NOMS)}

STYLE_PAR_DEFAUT = {"couleur": "black", "trait": "-", "epaisseur": 1.3,
                    "marker":"o", "ms": 5}

COULEURS_PAR_CAS = ["#0072BD", "#D95319", "#EDB120", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F", "#333333"]

def scipy_trapezes(p1, p2, p3, p4, a, b, n):
    x = np.linspace(a, b, n+1)
    return float(integrate.trapezoid(evaluer_poly(x, p1, p2, p3, p4), x))

def scipy_simpson(p1, p2, p3, p4, a, b, n):
    if n%2 == 0: # ajout de l'option n paire que scipy.integrate.simpson demande
        n += 1
    x = np.linspace(a, b, n+1)
    return float(integrate.simpson(evaluer_poly(x, p1, p2, p3, p4), x))

#------------------------------------------------------------------------------------------
# TEMPS
#------------------------------------------------------------------------------------------

def mesurer_temps(func, args, repetitions=200):
    return timeit.Timer(lambda: func(*args)).timeit(number=repetitions)/repetitions

#------------------------------------------------------------------------------------------
# GRAPHIQUES
#------------------------------------------------------------------------------------------

def _loglog(liste_n, dict_data, ylabel, titre, save_path):
    fig, ax = plt.subplots(figsize=(10, 6))
    for nom, vals in dict_data.items():
        s = STYLE_PAR_METHODE.get(nom, STYLE_PAR_DEFAUT)
        ax.plot(liste_n, vals, color=s["couleur"], ls=s["trait"], lw=s["epaisseur"], marker=s["marker"],
                markerfacecolor="white", markeredgewidth=1.2, label=nom)
    ax.set(xscale="log", yscale="log", xlabel="Nombre de segments n", ylabel=ylabel, title=titre)
    ax.legend(fontsize=8.5, framealpha=0.9)
    ax.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig

def graphique_convergence(liste_n, dict_erreurs, titre="Convergence des méthodes", save_path=None):
    return _loglog(liste_n, dict_erreurs, "Erreur absolue |I_num − I_exact|", titre, save_path)

def graphique_temps(liste_n, dict_temps, titre="Temps de calcul vs segments", save_path=None):
    return _loglog(liste_n, dict_temps, "Temps moyen par appel (s)", titre, save_path)

def graphique_erreur_methodes(liste_n, dict_erreurs, titre="Comparaison erreur x méthode", save_path=None):
    methodes = list(dict_erreurs.keys())
    log_erreurs = np.log10(np.clip([dict_erreurs[i] for i in methodes], 1e-16, None))
    xs, ys = np.meshgrid(range(len(methodes)), liste_n, indexing="ij")
    fig, ax = plt.subplots(figsize=(13, 7))
    sc = ax.scatter(xs.ravel(), ys.ravel(), s=np.maximum(20, 1200 + log_erreurs.ravel()*120),
                    c=log_erreurs.ravel(), cmap=LinearSegmentedColormap.from_list("matlab", ["#77AC30", "#EDB120", "#D95319"]),
                    alpha=0.80, edgecolors="white", linewidths=0.8)
    for (i,j), v in np.ndenumerate(log_erreurs):
        ax.text(i, liste_n[j], f"{v:.1f}", ha="center", va="center", fontsize=6.5, color="white", fontweight="bold")
    ax.set_xticks(range(len(methodes)))
    ax.set_xticklabels(methodes, rotation=30, ha="right", fontsize=9)
    ax.set_yticks(liste_n)
    ax.set_yticklabels(liste_n, fontsize=9)
    ax.grid(True, axis="y", ls="--", lw=0.5, alpha=0.4)
    ax.text(0.01, 0.01, "Petite bulle verte = erreur faible  Grosse bulle rouge = erreur élevée", transform=ax.transAxes, fontsize=7.5, color="gray", va="bottom")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig

