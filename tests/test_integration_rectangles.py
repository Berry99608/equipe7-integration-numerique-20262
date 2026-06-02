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

# Paramètres communs réutilisés dans plusieurs tests
P1, P2, P3, P4 = 1.0, 2.0, -1.0, 0.5
A, B = -2.0, 3.0


# --- evaluer_poly ---

def test_evaluer_poly_scalaire():
    assert evaluer_poly(0, 1, 2, 3, 4) == pytest.approx(1.0)
    assert evaluer_poly(1, 1, 2, 3, 4) == pytest.approx(10.0)

def test_evaluer_poly_cubique_pur():
    # f(x) = x³ → f(2) = 8
    assert evaluer_poly(2, 0, 0, 0, 1) == pytest.approx(8.0)

def test_evaluer_poly_array_numpy():
    x = np.array([0.0, 1.0, 2.0])
    result = evaluer_poly(x, 0, 0, 0, 1)  # f(x) = x³
    np.testing.assert_allclose(result, [0.0, 1.0, 8.0])


# --- solution_analytique ---

def test_solution_analytique_constante():
    # ∫₀¹ 1 dx = 1
    assert solution_analytique(1, 0, 0, 0, 0, 1) == pytest.approx(1.0)

def test_solution_analytique_lineaire():
    # ∫₀¹ x dx = 0.5
    assert solution_analytique(0, 1, 0, 0, 0, 1) == pytest.approx(0.5)

def test_solution_analytique_quadratique():
    # ∫₀¹ x² dx = 1/3
    assert solution_analytique(0, 0, 1, 0, 0, 1) == pytest.approx(1 / 3)

def test_solution_analytique_cubique():
    # ∫₀¹ x³ dx = 0.25
    assert solution_analytique(0, 0, 0, 1, 0, 1) == pytest.approx(0.25)

def test_solution_analytique_intervalle_negatif():
    # Symétrie : ∫₋₁¹ x dx = 0
    assert solution_analytique(0, 1, 0, 0, -1, 1) == pytest.approx(0.0)


# --- rectangles_python ---

def test_rectangles_python_constante_exacte():
    # La méthode des rectangles est exacte pour une fonction constante
    assert rectangles_python(5, 0, 0, 0, 0, 4, 10) == pytest.approx(20.0)

def test_rectangles_python_converge():
    # L'erreur doit diminuer quand n augmente
    i_exact = solution_analytique(P1, P2, P3, P4, A, B)
    err_10 = calculer_erreur(rectangles_python(P1, P2, P3, P4, A, B, 10), i_exact)
    err_1000 = calculer_erreur(rectangles_python(P1, P2, P3, P4, A, B, 1000), i_exact)
    assert err_1000 < err_10

def test_rectangles_python_resultat_positif_n():
    result = rectangles_python(P1, P2, P3, P4, A, B, 100)
    i_exact = solution_analytique(P1, P2, P3, P4, A, B)
    assert calculer_erreur(result, i_exact) < 1.0


# --- rectangles_numpy ---

def test_rectangles_numpy_constante_exacte():
    assert rectangles_numpy(5, 0, 0, 0, 0, 4, 10) == pytest.approx(20.0)

def test_rectangles_numpy_coherent_avec_python():
    # Les deux implémentations doivent donner le même résultat
    r_py = rectangles_python(P1, P2, P3, P4, A, B, 500)
    r_np = rectangles_numpy(P1, P2, P3, P4, A, B, 500)
    assert r_py == pytest.approx(r_np, rel=1e-10)

def test_rectangles_numpy_converge():
    i_exact = solution_analytique(P1, P2, P3, P4, A, B)
    err_10 = calculer_erreur(rectangles_numpy(P1, P2, P3, P4, A, B, 10), i_exact)
    err_1000 = calculer_erreur(rectangles_numpy(P1, P2, P3, P4, A, B, 1000), i_exact)
    assert err_1000 < err_10


# --- calculer_erreur ---

def test_calculer_erreur_positive():
    assert calculer_erreur(3.0, 5.0) == pytest.approx(2.0)

def test_calculer_erreur_symetrie():
    # L'erreur est absolue, l'ordre n'importe pas
    assert calculer_erreur(3.0, 5.0) == calculer_erreur(5.0, 3.0)

def test_calculer_erreur_nulle():
    assert calculer_erreur(4.2, 4.2) == pytest.approx(0.0)


# --- erreur_vs_segments ---

def test_erreur_vs_segments_longueur():
    liste_n = [10, 50, 100, 500]
    ep, en = erreur_vs_segments(P1, P2, P3, P4, A, B, liste_n)
    assert len(ep) == len(liste_n)
    assert len(en) == len(liste_n)

def test_erreur_vs_segments_convergence():
    # Les erreurs doivent être décroissantes quand n augmente
    liste_n = [10, 100, 1000]
    ep, en = erreur_vs_segments(P1, P2, P3, P4, A, B, liste_n)
    assert ep[0] > ep[1] > ep[2]
    assert en[0] > en[1] > en[2]

def test_erreur_vs_segments_valeurs_positives():
    liste_n = [10, 100]
    ep, en = erreur_vs_segments(P1, P2, P3, P4, A, B, liste_n)
    assert all(e >= 0 for e in ep)
    assert all(e >= 0 for e in en)


# --- mesurer_temps_rectangles ---

def test_mesurer_temps_retourne_positifs():
    tp, tn = mesurer_temps_rectangles(P1, P2, P3, P4, A, B, 100, repetitions=10)
    assert tp > 0
    assert tn > 0

def test_mesurer_temps_numpy_plus_rapide_grand_n():
    # NumPy doit être plus rapide que Python pur pour un grand n
    tp, tn = mesurer_temps_rectangles(P1, P2, P3, P4, A, B, 10_000, repetitions=20)
    assert tn < tp
