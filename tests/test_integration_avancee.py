import pytest
import numpy as np
from integration_avancee import (
    trapezes_python,
    trapezes_numpy,
    simpson_python,
    simpson_numpy,
    erreur_vs_segments_trapezes,
    erreur_vs_segments_simpson,
    mesurer_temps_trapezes,
    mesurer_temps_simpson,
)
from integration_rectangles import (
    solution_analytique,
    calculer_erreur,
)


@pytest.fixture
def params():
    return {"p1": 1.0, "p2": 2.0, "p3": -1.0, "p4": 0.5, "a": -2.0, "b": 3.0}


# ═══════════════════════════════════════════════════════════════
# MÉTHODE DES TRAPÈZES
# ═══════════════════════════════════════════════════════════════

# --- trapezes_python ---

def test_trapezes_python_constante_exacte():
    """f(x) = 5 sur [0, 4] → intégrale exacte = 30.0, peu importe n."""
    assert trapezes_python(5, 0, 0, 0, 0, 4, 10) == pytest.approx(20.0)


def test_trapezes_python_lineaire_exacte():
    """f(x) = x sur [0, 2] → ∫₀² x dx = 2.0  (trapèzes exact sur les fonctions linéaires)."""
    assert trapezes_python(0, 1, 0, 0, 0, 2, 4) == pytest.approx(2.0)


def test_trapezes_python_converge(params):
    """Plus n est grand, plus l'erreur doit diminuer."""
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(trapezes_python(**params, n=10), i_exact)
    err_1000 = calculer_erreur(trapezes_python(**params, n=1000), i_exact)
    assert err_1000 < err_10


def test_trapezes_python_proche_exact(params):
    """Erreur absolue < 1.0 avec n = 100."""
    result = trapezes_python(**params, n=100)
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    assert calculer_erreur(result, i_exact) < 1.0


# --- trapezes_numpy ---

def test_trapezes_numpy_constante_exacte():
    """Même cas que Python : f(x) = 5 sur [4, 10] → 30.0."""
    assert trapezes_numpy(5, 0, 0, 0, 4, 10, 10) == pytest.approx(30.0)


def test_trapezes_numpy_lineaire_exacte():
    """f(x) = x sur [0, 2] → 2.0 (exact pour les trapèzes)."""
    assert trapezes_numpy(0, 1, 0, 0, 0, 2, 4) == pytest.approx(2.0)


def test_trapezes_numpy_coherent_avec_python(params):
    """Les deux implémentations doivent produire le même résultat (rel. 1e-10)."""
    r_py = trapezes_python(**params, n=500)
    r_np = trapezes_numpy(**params, n=500)
    assert r_py == pytest.approx(r_np, rel=1e-10)


def test_trapezes_numpy_converge(params):
    """Convergence : erreur à n=1000 < erreur à n=10."""
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(trapezes_numpy(**params, n=10), i_exact)
    err_1000 = calculer_erreur(trapezes_numpy(**params, n=1000), i_exact)
    assert err_1000 < err_10


# --- erreur_vs_segments_trapezes ---

def test_erreur_vs_segments_trapezes_longueur(params):
    """Le nombre d'erreurs retournées correspond à la longueur de liste_n."""
    liste_n = [10, 50, 100, 500]
    ep, en = erreur_vs_segments_trapezes(**params, liste_n=liste_n)
    assert len(ep) == len(liste_n)
    assert len(en) == len(liste_n)


def test_erreur_vs_segments_trapezes_convergence(params):
    """Les erreurs doivent décroître strictement quand n augmente."""
    liste_n = [10, 100, 1000]
    ep, en = erreur_vs_segments_trapezes(**params, liste_n=liste_n)
    assert ep[0] > ep[1] > ep[2]
    assert en[0] > en[1] > en[2]


def test_erreur_vs_segments_trapezes_valeurs_positives(params):
    """Les erreurs absolues sont toutes >= 0."""
    ep, en = erreur_vs_segments_trapezes(**params, liste_n=[10, 100])
    assert all(e >= 0 for e in ep)
    assert all(e >= 0 for e in en)


# --- mesurer_temps_trapezes ---

def test_mesurer_temps_trapezes_retourne_positifs(params):
    """Les temps mesurés doivent être strictement positifs."""
    tp, tn = mesurer_temps_trapezes(**params, n=100, repetitions=10)
    assert tp > 0
    assert tn > 0


def test_mesurer_temps_trapezes_numpy_plus_rapide_grand_n(params):
    """NumPy doit être plus rapide que Python pur pour un grand n (médiane sur 5 runs)."""
    resultats = [
        mesurer_temps_trapezes(**params, n=10_000, repetitions=50)
        for _ in range(5)
    ]
    mediane_py = sorted(r[0] for r in resultats)[2]
    mediane_np = sorted(r[1] for r in resultats)[2]
    assert mediane_np < mediane_py


# ═══════════════════════════════════════════════════════════════
# MÉTHODE DE SIMPSON
# ═══════════════════════════════════════════════════════════════

# --- simpson_python ---


def test_simpson_python_constante_exacte():
    """f(x) = 5 sur [4, 10] → intégrale exacte = 30.0."""
    assert simpson_python(5, 0, 0, 0, 4, 10, 10) == pytest.approx(30.0)


def test_simpson_python_cubique_exacte():
    """Simpson est exact pour les polynômes de degré ≤ 3.
    ∫₀¹ (x³ + x² + x + 1) dx = 0.25 + 1/3 + 0.5 + 1 = 25/12 ≈ 2.08333…
    """
    expected = 0.25 + 1 / 3 + 0.5 + 1.0
    assert simpson_python(1, 1, 1, 1, 0, 1, 4) == pytest.approx(expected)


def test_simpson_python_converge(params):
    """Plus n est grand, plus l'erreur doit diminuer (ou déjà à la précision machine)."""
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(simpson_python(**params, n=10), i_exact)
    err_1000 = calculer_erreur(simpson_python(**params, n=1000), i_exact)
    assert err_1000 < err_10 or err_10 < 1e-12


def test_simpson_python_proche_exact(params):
    """Erreur absolue < 1.0 avec n = 100."""
    result = simpson_python(**params, n=100)
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    assert calculer_erreur(result, i_exact) < 1.0


def test_simpson_python_n_impair_accepte(params):
    """Un n impair passé en entrée ne doit pas lever d'exception (correction interne)."""
    try:
        simpson_python(**params, n=11)
    except Exception as e:
        pytest.fail(f"simpson_python a levé une exception avec n impair : {e}")


# --- simpson_numpy ---

def test_simpson_numpy_constante_exacte():
    """Même cas que Python : f(x) = 5 sur [4, 10] → 30.0."""
    assert simpson_numpy(5, 0, 0, 0, 4, 10, 10) == pytest.approx(30.0)


def test_simpson_numpy_cubique_exacte():
    """Simpson vectorisé : exact pour les polynômes de degré ≤ 3."""
    expected = 0.25 + 1 / 3 + 0.5 + 1.0
    assert simpson_numpy(1, 1, 1, 1, 0, 1, 4) == pytest.approx(expected)


def test_simpson_numpy_coherent_avec_python(params):
    """Les deux implémentations doivent produire le même résultat (rel. 1e-10)."""
    r_py = simpson_python(**params, n=500)
    r_np = simpson_numpy(**params, n=500)
    assert r_py == pytest.approx(r_np, rel=1e-10)


def test_simpson_numpy_converge(params):
    """Convergence : erreur à n=1000 < erreur à n=10 (ou déjà à la précision machine)."""
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    err_10 = calculer_erreur(simpson_numpy(**params, n=10), i_exact)
    err_1000 = calculer_erreur(simpson_numpy(**params, n=1000), i_exact)
    assert err_1000 < err_10 or err_10 < 1e-12


def test_simpson_numpy_n_impair_accepte(params):
    """Un n impair passé en entrée ne doit pas lever d'exception (correction interne)."""
    try:
        simpson_numpy(**params, n=11)
    except Exception as e:
        pytest.fail(f"simpson_numpy a levé une exception avec n impair : {e}")


# --- erreur_vs_segments_simpson ---

def test_erreur_vs_segments_simpson_longueur(params):
    """Le nombre d'erreurs retournées correspond à la longueur de liste_n."""
    liste_n = [10, 50, 100, 500]
    ep, en = erreur_vs_segments_simpson(**params, liste_n=liste_n)
    assert len(ep) == len(liste_n)
    assert len(en) == len(liste_n)


def test_erreur_vs_segments_simpson_convergence(params):
    """Les erreurs décroissent quand n augmente, ou sont déjà à la précision machine."""
    liste_n = [10, 100, 1000]
    ep, en = erreur_vs_segments_simpson(**params, liste_n=liste_n)
    assert ep[0] > ep[1] > ep[2] or ep[0] < 1e-12
    assert en[0] > en[1] > en[2] or en[0] < 1e-12


def test_erreur_vs_segments_simpson_valeurs_positives(params):
    """Les erreurs absolues sont toutes >= 0."""
    ep, en = erreur_vs_segments_simpson(**params, liste_n=[10, 100])
    assert all(e >= 0 for e in ep)
    assert all(e >= 0 for e in en)


def test_erreur_vs_segments_simpson_meilleur_que_trapezes(params):
    """Pour un même n, Simpson doit être plus précis que les trapèzes.
    Vrai pour les polynômes de degré > 2 (ordre de convergence supérieur).
    """
    from integration_avancee import trapezes_python
    i_exact = solution_analytique(**{k: params[k] for k in ("p1", "p2", "p3", "p4", "a", "b")})
    n = 10
    err_trap = calculer_erreur(trapezes_python(**params, n=n), i_exact)
    err_simp = calculer_erreur(simpson_python(**params, n=n), i_exact)
    assert err_simp < err_trap


# --- mesurer_temps_simpson ---

def test_mesurer_temps_simpson_retourne_positifs(params):
    """Les temps mesurés doivent être strictement positifs."""
    tp, tn = mesurer_temps_simpson(**params, n=100, repetitions=10)
    assert tp > 0
    assert tn > 0


def test_mesurer_temps_simpson_numpy_plus_rapide_grand_n(params):
    """NumPy doit être plus rapide que Python pur pour un grand n (médiane sur 5 runs)."""
    resultats = [
        mesurer_temps_simpson(**params, n=10_000, repetitions=50)
        for _ in range(5)
    ]
    mediane_py = sorted(r[0] for r in resultats)[2]
    mediane_np = sorted(r[1] for r in resultats)[2]
    assert mediane_np < mediane_py
