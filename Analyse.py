import numpy as np
from integration_rectangles import solution_analytique, calculer_erreur, mesurer_temps_rectangles
from integration_avancee import mesurer_temps_trapezes, mesurer_temps_simpson
from visualisation import scipy_trapezes, scipy_simpson, mesurer_temps

def construire_mesurer_temps(repetitions):
    r = repetitions
    return {"Rectangle Python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, r)[0],
            "Rectangle Numpy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, r)[1],
            "Trapeze Python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_trapezes(p1, p2, p3, p4, a, b, n, r)[0],
            "Trapeze Numpy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_trapezes(p1, p2, p3, p4, a, b, n, r)[1],
            "Simpson python": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_simpson(p1, p2, p3, p4, a, b, n, r)[0],
            "Simpson Numpy": lambda p1, p2, p3, p4, a, b, n: mesurer_temps_simpson(p1, p2, p3, p4, a, b, n, r)[1],
            "Scipy Trapeze": lambda p1, p2, p3, p4, a, b, n: mesurer_temps(scipy_trapezes, (p1, p2, p3, p4, a, b, n), r),
            "Scipy Simpson": lambda p1, p2, p3, p4, a, b, n: mesurer_temps(scipy_simpson, (p1, p2, p3, p4, a, b, n), r),}

