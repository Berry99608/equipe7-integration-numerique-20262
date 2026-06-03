import numpy as np
import pytest
from integration_rectangles import (
    evaluer_poly,
    solution_analytique,
    rectangles_python,
    rectangles_numpy,
    calculer_erreur,
    erreur_vs_segments,
    mesurer_temps_rectangles,
)


@pytest.fixture
def params():
    return {"p1": 1.0, "p2": 2.0, "p3": -1.0, "p4": 0.5, "a": -2.0, "b": 3.0}


# --- evaluer_poly ---

@pytest.mark.parametrize("x, p1, p2, p3, p4, expected", [
    (0, 1, 2, 3, 4, 1.0),
    (1, 1, 2, 3, 4, 10.0),
    (2, 0, 0, 0, 1, 8.0),
])
def test_evaluer_poly_scalaire(x, p1, p2, p3, p4, expected):
    assert evaluer_poly(x, p1, p2, p3, p4) == pytest.approx(expected)

def test_evaluer_poly_array_numpy():
    x = np.array([0.0, 1.0, 2.0])
    result = evaluer_poly(x, 0, 0, 0, 1)
    np.testing.assert_allclose(result, [0.0, 1.0, 8.0])


# --- solution_analytique ---

@pytest.mark.parametrize("p1, p2, p3, p4, a, b, expected", [
    (1, 0, 0, 0, 0, 1, 1.0),       # ∫₀¹ 1 dx = 1
    (0, 1, 0, 0, 0, 1, 0.5),       # ∫₀¹ x dx = 0.5
    (0, 0, 1, 0, 0, 1, 1 / 3),     # ∫₀¹ x² dx = 1/3
    (0, 0, 0, 1, 0, 1, 0.25),      # ∫₀¹ x³ dx = 0.25
    (0, 1, 0, 0, -1, 1, 0.0),      # ∫₋₁¹ x dx = 0 (symétrie)
])
def test_solution_analytique(p1, p2, p3, p4, a, b, expected):
    assert solution_analytique(p1, p2, p3, p4, a, b) == pytest.approx(expected)


# --- rectangles_python ---

def test_rectangles_python_constante_exacte():
    assert rectangles_python(5, 0, 0, 0, 0, 4, 10) == pytest.approx(20.0)

def test_rectangles_python_converge(params):
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(rectangles_python(**params, n=10), i_exact)
    err_1000 = calculer_erreur(rectangles_python(**params, n=1000), i_exact)
    assert err_1000 < err_10

def test_rectangles_python_proche_exact(params):
    result = rectangles_python(**params, n=100)
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    assert calculer_erreur(result, i_exact) < 1.0


# --- rectangles_numpy ---

def test_rectangles_numpy_constante_exacte():
    assert rectangles_numpy(5, 0, 0, 0, 0, 4, 10) == pytest.approx(20.0)

def test_rectangles_numpy_coherent_avec_python(params):
    r_py = rectangles_python(**params, n=500)
    r_np = rectangles_numpy(**params, n=500)
    assert r_py == pytest.approx(r_np, rel=1e-10)

def test_rectangles_numpy_converge(params):
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(rectangles_numpy(**params, n=10), i_exact)
    err_1000 = calculer_erreur(rectangles_numpy(**params, n=1000), i_exact)
    assert err_1000 < err_10


# --- calculer_erreur ---

@pytest.mark.parametrize("a, b, expected", [
    (3.0, 5.0, 2.0),
    (5.0, 3.0, 2.0),
    (4.2, 4.2, 0.0),
])
def test_calculer_erreur(a, b, expected):
    assert calculer_erreur(a, b) == pytest.approx(expected)


# --- erreur_vs_segments ---

def test_erreur_vs_segments_longueur(params):
    liste_n = [10, 50, 100, 500]
    ep, en = erreur_vs_segments(**params, liste_n=liste_n)
    assert len(ep) == len(liste_n)
    assert len(en) == len(liste_n)

def test_erreur_vs_segments_convergence(params):
    liste_n = [10, 100, 1000]
    ep, en = erreur_vs_segments(**params, liste_n=liste_n)
    assert ep[0] > ep[1] > ep[2]
    assert en[0] > en[1] > en[2]

def test_erreur_vs_segments_valeurs_positives(params):
    ep, en = erreur_vs_segments(**params, liste_n=[10, 100])
    assert all(e >= 0 for e in ep)
    assert all(e >= 0 for e in en)


# --- mesurer_temps_rectangles ---

def test_mesurer_temps_retourne_positifs(params):
    tp, tn = mesurer_temps_rectangles(**params, n=100, repetitions=10)
    assert tp > 0
    assert tn > 0

def test_mesurer_temps_numpy_plus_rapide_grand_n(params):
    # NumPy amortit son overhead sur un grand n ; on moyenne sur plusieurs runs
    # pour réduire la variance due à l'ordonnancement OS
    resultats = [
        mesurer_temps_rectangles(**params, n=10_000, repetitions=50)
        for _ in range(5)
    ]
    mediane_py = sorted(r[0] for r in resultats)[2]
    mediane_np = sorted(r[1] for r in resultats)[2]
    assert mediane_np < mediane_py
