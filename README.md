# Mini-Projet B — Intégration Numérique

MGA 802 — Introduction à la programmation avec Python

## Objectif

Calculer numériquement l'intégrale d'un polynôme du 3e ordre et comparer la précision et la performance de plusieurs méthodes d'intégration :

$$I = \int_a^b f(x)\,dx \quad \text{avec} \quad f(x) = p_1 + p_2 x + p_3 x^2 + p_4 x^3$$

## Structure du projet

```
equipe7-integration-numerique/
├── integration_rectangles.py   # Méthode des rectangles (Python pur + NumPy)
├── integration_avancee.py      # Méthodes des trapèzes et de Simpson
├── visualisation.py            # Graphiques et méthodes SciPy
├── Analyse.py                  # Calcul des erreurs et convergences
├── main.py                     # Point d'entrée interactif
└── tests/
    ├── test_integration_rectangles.py
    └── test_integration_avancee.py
```

## Modules Python requis

```
numpy
matplotlib
scipy
timeit
pandas
```

Installation :

```bash
pip install numpy matplotlib scipy pandas
```

## Utilisation

```bash
python3 main.py
```
Le programme affiche un menu interactif à deux niveaux :

- **[1] Mes propres valeurs** — saisir p1, p2, p3, p4, a, b manuellement (ou Entrée pour les valeurs par défaut), puis choisir les graphiques à afficher
- **[2] Expériences prédéfinies** — lancer un des trois scénarios :
  - **EXP 1** — bornes fixes, coefficients p varient
  - **EXP 2** — coefficients fixes, bornes varient
  - **EXP 3** — coefficients et bornes varient simultanément → génère des graphiques 3D
- **[0] Quitter**

Les graphiques s'affichent à l'écran via `plt.show()`. Après fermeture des fenêtres, le programme demande si vous souhaitez sauvegarder les figures ; si oui, indiquez un dossier et un préfixe (ex: `figures/exp1`) et les fichiers seront exportés en PDF.

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

### `Analyse.py`

| Fonction | Description |
|---|---|
| `construire_mesurer_temps(repetitions)` | Retourne le dictionnaire des 8 fonctions de mesure de temps |
| `calculer_df_ref(df_cas, fonctions, mesurer_temps_dict, n_ref, repetitions)` | DataFrame (cas × méthode) : valeur numérique, erreur et temps à n_ref |
| `calculer_convergences(df_cas, fonctions, mesurer_temps_dict, liste_n)` | Dict `{cas: {dict_erreurs, dict_temps}}` sur toute liste_n |
| `afficher_synthese(df_ref, titre)` | Affiche classement global et meilleure méthode par cas dans le terminal |

### `visualisation.py`

| Fonction | Description |
|---|---|
| `scipy_trapezes(p1, p2, p3, p4, a, b, n)` | Trapèzes via `scipy.integrate` |
| `scipy_simpson(p1, p2, p3, p4, a, b, n)` | Simpson via `scipy.integrate` |
| `mesurer_temps(func, args, repetitions)` | Wrapper `timeit` générique |
| `graphique_convergence(liste_n, dict_erreurs, titre, save_path)` | Courbes erreur absolue vs n (log-log), repère de pente −2, bande précision machine |
| `graphique_temps(liste_n, dict_temps, titre, save_path)` | Courbes temps de calcul vs n (log-log), annotation du point de croisement Python/NumPy |
| `graphique_erreur_methodes(liste_n, dict_erreurs, titre, save_path)` | Heatmap log₁₀\|erreur\| par méthode et par n, avec barre de couleur arrondie |
| `graphique_convergence_3d(liste_n, convergence, titre, save_path)` | Courbes 3D erreur vs n vs cas — utilisé pour EXP 3 |
| `graphique_temps_3d(liste_n, convergence, titre, save_path)` | Courbes 3D temps vs n vs cas — utilisé pour EXP 3 |
| `graphique_erreur_3d(liste_n, convergence, titre, save_path)` | Pillules 3D hauteur = précision par méthode — utilisé pour EXP 3 |

**Système visuel unifié** — palette Okabe-Ito (daltonisme) :

La couleur encode la **méthode mathématique**, le style de trait encode l'**implémentation** ; les deux dimensions sont indépendantes.

| Dimension | Valeur | Signification |
|---|---|---|
| Couleur | `#0072B2` bleu | Rectangle |
| Couleur | `#E69F00` ambre | Trapèze |
| Couleur | `#009E73` vert | Simpson |
| Trait | `—` solide | Python pur |
| Trait | `--` tirets longs | NumPy |
| Trait | `··` pointillés | SciPy |

## Tests

```bash
python3 -m pytest tests/ -v
```

52 tests répartis sur deux fichiers :

- `test_integration_rectangles.py` — 23 tests (évaluation du polynôme, solution analytique, rectangles Python/NumPy, erreurs, temps)
- `test_integration_avancee.py` — 29 tests (trapèzes et Simpson Python/NumPy, convergence, temps)

> **Note** : les tests de convergence Simpson acceptent le cas où l'erreur est déjà à la précision machine (< 10⁻¹²), car Simpson est exact pour les polynômes de degré ≤ 3.

## Auteurs

Projet réalisé en équipe dans le cadre du cours MGA 802.

- Bouchra Berrissoul
- Syndia Jean
- Théophile Kevin Tsala Noah
