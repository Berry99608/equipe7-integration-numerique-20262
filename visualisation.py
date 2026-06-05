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

