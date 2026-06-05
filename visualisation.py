"""
visualisation.py
================
MGA802 — Mini-Projet B : Intégration numérique
Fonctions de visualisation pour les 3 figures comparatives.

Système visuel :
  - Couleur  = méthode mathématique  (Rectangle / Trapèze / Simpson)
  - Trait    = implémentation         (Python pur / NumPy / SciPy)
  - Palette Okabe–Ito, sûre pour le daltonisme
"""

import timeit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy import integrate
from integration_rectangles import evaluer_poly

# ─── Paramètres globaux — style verre ────────────────────────────────────────
# Fond figure : blanc légèrement bleuté, translucide
# Fond axes   : blanc très transparent pour laisser passer le fond figure
_FIG_FC  = "#F7F9FC"       # fond figure très légèrement bleuté
_AXES_FC = (1, 1, 1, 0.82) # fond axes quasi-opaque, juste un souffle de transparence
_GRID_C  = "#DDE3ED"

plt.rcParams.update({
    "figure.figsize":       (10, 6),
    "figure.dpi":           120,
    "figure.facecolor":     _FIG_FC,
    "axes.facecolor":       _AXES_FC,
    "font.family":          "DejaVu Sans",
    "font.size":            11,
    "axes.titlesize":       14,
    "axes.titleweight":     "bold",
    "axes.labelsize":       11,
    "axes.spines.top":      False,
    "axes.spines.right":    False,
    "axes.edgecolor":       "#C4CCDA",
    "axes.grid":            True,
    "grid.color":           _GRID_C,
    "grid.linewidth":       0.7,
    "legend.frameon":       True,
    "legend.framealpha":    0.75,
    "legend.edgecolor":     "#D0D8E8",
    "legend.facecolor":     "#FAFCFF",
    "legend.fontsize":      10,
    "xtick.labelsize":      10,
    "ytick.labelsize":      10,
})

# ─── Système couleur / trait ──────────────────────────────────────────────────

# Palette Okabe–Ito  →  couleur = méthode mathématique
COL = {"rect": "#0072B2", "trap": "#E69F00", "simp": "#009E73"}
# Style de trait     →  implémentation
LS  = {"python": "-", "numpy": "--", "scipy": ":"}
# Marqueurs par série
_MK = {
    "Rectangle Python": "o", "Rectangle NumPy": "s",
    "Trapeze Python":   "^", "Trapeze NumPy":   "v",
    "Simpson Python":   "D", "Simpson NumPy":   "P",
    "Scipy Trapeze":    "*", "Scipy Simpson":   "X",
}


def _style(nom):
    """Retourne (couleur, linestyle, marker) pour une série donnée."""
    n = nom.lower()
    c  = COL["rect"] if "rect" in n else COL["trap"] if "trap" in n else COL["simp"] if "simp" in n else "#555"
    ls = LS["scipy"] if "scipy" in n else LS["numpy"] if "numpy" in n else LS["python"]
    mk = _MK.get(nom, "o")
    return c, ls, mk


def _legende_2blocs(ax):
    """
    Légende en deux blocs hors cadre (à droite) :
      1. Couleur = méthode  →  Rectangle / Trapèze / Simpson
      2. Trait   = impl.    →  Python / NumPy / SciPy
    """
    sep = Line2D([], [], color="none", label="trait = implémentation")
    handles = [
        Line2D([0], [0], color=COL["rect"], lw=2.0, label="Rectangle"),
        Line2D([0], [0], color=COL["trap"], lw=2.0, label="Trapèze"),
        Line2D([0], [0], color=COL["simp"], lw=2.0, label="Simpson"),
        sep,
        Line2D([0], [0], color="#333", ls="-",  lw=1.5, label="Python"),
        Line2D([0], [0], color="#333", ls="--", lw=1.5, label="NumPy"),
        Line2D([0], [0], color="#333", ls=":",  lw=1.5, label="SciPy"),
    ]
    leg = ax.legend(handles=handles, loc="center left",
                    bbox_to_anchor=(1.02, 0.5), borderaxespad=0,
                    fontsize=10, handlelength=2.2)
    for txt in leg.get_texts():
        if txt.get_text() == "trait = implémentation":
            txt.set_style("italic")
            txt.set_color("#999999")
            txt.set_fontsize(9)
    return leg


# ─── Fonctions de calcul (inchangées) ────────────────────────────────────────

def scipy_trapezes(p1, p2, p3, p4, a, b, n):
    x = np.linspace(a, b, n + 1)
    return float(integrate.trapezoid(evaluer_poly(x, p1, p2, p3, p4), x))


def scipy_simpson(p1, p2, p3, p4, a, b, n):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    return float(integrate.simpson(evaluer_poly(x, p1, p2, p3, p4), x))


def mesurer_temps(func, args, repetitions=200):
    return timeit.Timer(lambda: func(*args)).timeit(number=repetitions) / repetitions


# ─── Figure 1 : Convergence des méthodes ─────────────────────────────────────

def graphique_convergence(liste_n, dict_erreurs,
                           titre="Convergence des méthodes", save_path=None):
    n = np.array(liste_n, dtype=float)
    fig, ax = plt.subplots()

    for nom, vals in dict_erreurs.items():
        c, ls, mk = _style(nom)
        ax.loglog(n, vals, color=c, ls=ls, marker=mk, lw=1.8,
                  markevery=2, markersize=5,
                  markerfacecolor="white", markeredgewidth=1.4)

    # ── Repère de pente −2 (ordre 2) ─────────────────────────────────────────
    vals_ordre2 = [v for v in dict_erreurs.values() if v[0] > 1e-10]
    if vals_ordre2:
        ref   = max(v[0] for v in vals_ordre2) * 1.3
        guide = ref * (n[0] / n) ** 2
        ax.plot(n, guide, color="#9A958C", ls=(0, (5, 4)), lw=1.2, zorder=0)
        ax.text(n[3] * 1.05, guide[3] * 0.38,
                "pente −2,  ordre 2", color="#6B665E", fontsize=9, rotation=-26)

    # ── Bande précision machine ───────────────────────────────────────────────
    ax.axhspan(1e-16, 4e-14, color=COL["simp"], alpha=0.07)
    ax.text(n[0] * 1.1, 7e-15,
            r"précision machine  ε ≈ 2,2·10$^{-16}$",
            color="#1C7A5B", fontsize=9)

    # ── Annotation « ≈ 10 ordres de grandeur » ───────────────────────────────
    vals_haut = [v[-1] for v in dict_erreurs.values() if v[-1] > 1e-10]
    vals_bas  = [v[-1] for v in dict_erreurs.values() if v[-1] < 1e-10]
    if vals_haut and vals_bas:
        y_h = min(vals_haut)
        y_b = max(vals_bas) * 50
        ax.annotate("", xy=(n[-1], y_b), xytext=(n[-1], y_h * 0.6),
                    arrowprops=dict(arrowstyle="<->", color="#9A958C", lw=1.3))
        ax.text(n[-1] * 1.06, (y_h * y_b) ** 0.5,
                "≈ 10 ordres\nde grandeur",
                color="#6B665E", fontsize=9, va="center")

    ax.set(xlabel="Nombre de segments n",
           ylabel=r"Erreur absolue $|I_{num} - I_{exact}|$",
           title=titre, ylim=(1e-16, 3))
    ax.grid(True, which="minor", lw=0.4, color="#EFEDE8")
    _legende_2blocs(ax)
    fig.subplots_adjust(left=0.1, right=0.78, top=0.92, bottom=0.12)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


# ─── Figure 2 : Temps de calcul vs segments ───────────────────────────────────

def graphique_temps(liste_n, dict_temps,
                    titre="Temps de calcul vs segments", save_path=None):
    n = np.array(liste_n, dtype=float)
    fig, ax = plt.subplots()

    for nom, vals in dict_temps.items():
        c, ls, mk = _style(nom)
        ax.loglog(n, vals, color=c, ls=ls, marker=mk, lw=1.8,
                  markevery=2, markersize=5,
                  markerfacecolor="white", markeredgewidth=1.4)

    # ── Annotation point de croisement Python → NumPy ────────────────────────
    noms_py = [k for k in dict_temps if "python" in k.lower() and "rect" in k.lower()]
    noms_np = [k for k in dict_temps if "numpy"  in k.lower() and "rect" in k.lower()]
    if noms_py and noms_np:
        t_py = np.array(dict_temps[noms_py[0]])
        t_np = np.array(dict_temps[noms_np[0]])
        idx  = np.where(np.diff(np.sign(t_np - t_py)))[0]
        n_cross = int(liste_n[idx[0]]) if len(idx) > 0 else 40
        y_cross = dict_temps[noms_np[0]][idx[0]] if len(idx) > 0 else 1e-5
        ax.axvline(n_cross, color="#9A958C", ls=":", lw=1.3, zorder=0)
        ax.annotate(
            f"au-delà de n ≈ {n_cross},\nle vectorisé NumPy l'emporte",
            xy=(n_cross, y_cross),
            xytext=(n_cross * 4, y_cross * 0.28),
            fontsize=9.5, color="#23211C",
            arrowprops=dict(arrowstyle="->", color="#9A958C", lw=1.2),
        )

    ax.set(xlabel="Nombre de segments n",
           ylabel="Temps moyen par appel (s)",
           title=titre)
    ax.grid(True, which="minor", lw=0.4, color="#EFEDE8")
    _legende_2blocs(ax)
    fig.subplots_adjust(left=0.1, right=0.78, top=0.92, bottom=0.12)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


# ─── Figure 3 : Heatmap erreur par méthode ────────────────────────────────────

_ORDRE_METHODES = [
    "Rectangle Python", "Rectangle NumPy",
    "Trapeze Python",   "Trapeze NumPy",
    "Simpson Python",   "Simpson NumPy",
    "Scipy Trapeze",    "Scipy Simpson",
]

# Colormap : rouille (erreur élevée) → vert foncé (précision machine)
_CMAP_ERREUR = LinearSegmentedColormap.from_list("erreur_cmap", [
    (0.00, "#2E7D40"),   # vert foncé   — précision machine (plus négatif)
    (0.35, "#6FAF3A"),   # vert clair
    (0.55, "#A8A830"),   # olive
    (0.75, "#B89040"),   # kaki
    (1.00, "#C06848"),   # rouille      — erreur élevée (proche de 0)
])


def graphique_erreur_methodes(liste_n, dict_erreurs,
                               titre="Erreur par méthode et par nombre de segments",
                               save_path=None):
    methodes = [m for m in _ORDRE_METHODES if m in dict_erreurs]
    methodes += [m for m in dict_erreurs if m not in methodes]

    erreurs = np.array([dict_erreurs[m] for m in methodes])
    data    = np.log10(np.clip(erreurs, 1e-16, None))

    n_rows, n_cols = len(methodes), len(liste_n)
    norm = Normalize(vmin=min(data.min(), -15), vmax=0)

    # ── Dimensions de la grille ───────────────────────────────────────────────
    cell_w, cell_h, gap = 1.0, 0.72, 0.14
    left_margin  = 3.1
    bottom_extra = 1.2   # espace pour le label n + barre de légende

    total_w = (left_margin + n_cols * (cell_w + gap)) * 0.88
    total_h = (0.7 + n_rows * (cell_h + gap) + bottom_extra) * 0.88

    fig, ax = plt.subplots(figsize=(total_w, total_h))
    ax.set_xlim(-left_margin, n_cols * (cell_w + gap) + 0.5)
    ax.set_ylim(-(cell_h + gap) * 0.2 - bottom_extra,
                n_rows * (cell_h + gap) + 1.45)
    ax.axis("off")
    fig.patch.set_facecolor(_FIG_FC)

    # ── Cellules de la grille ─────────────────────────────────────────────────
    for i, meth in enumerate(methodes):
        row_y = (n_rows - 1 - i) * (cell_h + gap)

        ax.text(-0.18, row_y + cell_h / 2, meth,
                ha="right", va="center", fontsize=10.5,
                fontfamily="DejaVu Sans Mono", color="#2D3748")

        for j in range(n_cols):
            val = data[i, j]
            t   = norm(val)
            r, g, b, _ = _CMAP_ERREUR(t)
            x   = j * (cell_w + gap)

            patch = FancyBboxPatch(
                (x + 0.04, row_y + 0.04),
                cell_w - 0.08, cell_h - 0.08,
                boxstyle="round,pad=0.07",
                facecolor=(r, g, b, 0.90),
                edgecolor=(1, 1, 1, 0.6),
                linewidth=0.6,
            )
            ax.add_patch(patch)

            txt_col = "white" if t < 0.55 else "#2E1A0E"
            ax.text(x + cell_w / 2, row_y + cell_h / 2,
                    f"{val:.1f}",
                    ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=txt_col,
                    fontfamily="DejaVu Sans Mono")

    # ── Étiquettes n en haut ──────────────────────────────────────────────────
    top_y = n_rows * (cell_h + gap) + 0.08
    for j, nv in enumerate(liste_n):
        ax.text(j * (cell_w + gap) + cell_w / 2, top_y,
                str(nv), ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    mid_x  = (n_cols * (cell_w + gap) - gap) / 2
    top_hd = n_rows * (cell_h + gap)
    # titre principal
    ax.text(mid_x, top_hd + 1.05, titre,
            ha="center", va="bottom", fontsize=14, fontweight="bold")
    # sous-titre explicatif (une ligne en dessous)
    ax.text(mid_x, top_hd + 0.58,
            r"chaque cellule = $\log_{10}|I_{num}-I_{exact}|$  "
            r"(ex. : $-14 \Rightarrow$ erreur $\approx 10^{-14}$)",
            ha="center", va="bottom", fontsize=9, color="#888888", style="italic")

    # ── Label « Nombre de segments n → » ─────────────────────────────────────
    label_y = -(cell_h + gap) * 0.25
    ax.text(mid_x, label_y, "Nombre de segments n →",
            ha="center", va="top", fontsize=10, color="#888888")

    # ── Barre de légende arrondie ─────────────────────────────────────────────
    bar_y     = label_y - 0.45
    bar_left  = 0.0
    bar_right = n_cols * (cell_w + gap) - gap
    bar_h     = 0.28

    # gradient 1D rouille → vert, dessiné directement sur ax
    grad = np.linspace(1, 0, 256).reshape(1, -1)
    im = ax.imshow(
        grad, aspect="auto", cmap=_CMAP_ERREUR,
        extent=[bar_left, bar_right, bar_y, bar_y + bar_h],
        zorder=2,
    )

    # clip arrondi de la barre
    pad_r = 0.14
    clip  = FancyBboxPatch(
        (bar_left  - pad_r, bar_y - pad_r * 0.4),
        bar_right - bar_left + 2 * pad_r,
        bar_h + pad_r * 0.8,
        boxstyle="round,pad=0.0",
        transform=ax.transData,
        facecolor="none", edgecolor="none",
    )
    ax.add_patch(clip)
    im.set_clip_path(clip)

    # labels de la barre
    ax.text(bar_left - 0.2, bar_y + bar_h / 2, "erreur élevée\n(log₁₀ ≈ 0)",
            ha="right", va="center", fontsize=9, color="#666666")
    ax.text(bar_right + 0.2, bar_y + bar_h / 2, "précision machine\n(log₁₀ ≈ −16)",
            ha="left", va="center", fontsize=9, color="#666666")

    fig.tight_layout(pad=0.4)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight", facecolor="white")
    return fig
