# Mini-Projet B — Intégration Numérique

MGA 802 — Introduction à la programmation avec Python

## Objectif

Calculer numériquement l'intégrale d'un polynôme du 3e ordre et comparer la précision et la performance de plusieurs méthodes d'intégration :

$$I = \int_a^b f(x)\,dx \quad \text{avec} \quad f(x) = p_1 + p_2 x + p_3 x^2 + p_4 x^3$$

## Structure du projet

```
mini_projet_b/
├── integration_rectangles.py   # Méthode des rectangles (Python pur + NumPy)
├── integration_avancee.py      # Méthodes des trapèzes et de Simpson
├── visualisation.py            # Graphiques et méthodes scipy
├── main.py                     # Point d'entrée principal
└── tests/
    └── test_integration_rectangles.py
```

## Modules Python requis

```
numpy
matplotlib
scipy
timeit
```

Installation :

```bash
pip install numpy matplotlib scipy
```

## Utilisation

```bash
python3 main.py
```

## Modules

### `integration_rectangles.py`

| Fonction | Description |
|---|---|
| `evaluer_poly(x, p1, p2, p3, p4)` | Évalue f(x), compatible scalaire et array NumPy |
| `solution_analytique(p1, p2, p3, p4, a, b)` | Calcule l'intégrale exacte via l'antidérivée |
| `rectangles_python(p1, p2, p3, p4, a, b, n)` | Méthode des rectangles en Python pur |
| `rectangles_numpy(p1, p2, p3, p4, a, b, n)` | Méthode des rectangles vectorisée avec NumPy |
| `calculer_erreur(i_numerique, i_exact)` | Retourne l'erreur absolue |
| `erreur_vs_segments(p1, p2, p3, p4, a, b, liste_n)` | Erreur pour chaque n de la liste (Python + NumPy) |
| `mesurer_temps_rectangles(p1, p2, p3, p4, a, b, n, repetitions)` | Temps moyen d'exécution via `timeit` |

### `integration_avancee.py`

| Fonction | Description |
|---|---|
| `trapezes_python(p1, p2, p3, p4, a, b, n)` | Méthode des trapèzes en Python pur |
| `trapezes_numpy(p1, p2, p3, p4, a, b, n)` | Méthode des trapèzes avec NumPy |
| `simpson_python(p1, p2, p3, p4, a, b, n)` | Méthode de Simpson en Python pur |
| `simpson_numpy(p1, p2, p3, p4, a, b, n)` | Méthode de Simpson avec NumPy |

### `visualisation.py`

| Fonction | Description |
|---|---|
| `scipy_trapezes(p1, p2, p3, p4, a, b, n)` | Trapèzes via `scipy.integrate` |
| `scipy_simpson(p1, p2, p3, p4, a, b, n)` | Simpson via `scipy.integrate` |
| `mesurer_temps(func, args, repetitions)` | Wrapper `timeit` générique |
| `graphique_convergence(liste_n, dict_erreurs)` | Courbes erreur vs nombre de segments |
| `graphique_temps(liste_n, dict_temps)` | Courbes temps de calcul vs nombre de segments |
| `graphique_erreur_methodes(liste_n, dict_erreurs)` | Comparaison des erreurs par méthode |

## Tests

```bash
python3 -m pytest tests/ -v
```

22 tests couvrant toutes les fonctions de `integration_rectangles.py`.

## Auteurs

Projet réalisé en équipe dans le cadre du cours MGA 802.

- Bouchra Berrissoul
- Syndia Jean
- Théophile Kevin Tsala Noah
