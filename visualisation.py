import timeit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import integrate
from integration_rectangles import evaluer_poly

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

