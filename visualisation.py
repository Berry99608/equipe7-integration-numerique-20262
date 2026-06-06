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
from numpy import array, clip, diff, linspace, log10, sign, where
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy import integrate
from integration_rectangles import evaluer_poly

# ─── Polices SF Pro (système Apple) ──────────────────────────────────────────
for _f in ("/System/Library/Fonts/SFNS.ttf",
           "/System/Library/Fonts/SFNSItalic.ttf",
           "/System/Library/Fonts/SFNSMono.ttf"):
    _fm.fontManager.addfont(_f)

_SF      = "System Font"    # SF Pro — tout le texte
_SF_MONO = ".SF NS Mono"    # SF Mono — valeurs numériques heatmap

# ─── Palette de couleurs Apple ────────────────────────────────────────────────
_FIG_FC  = "#F5F5F7"   # fond figure : gris clair Apple
_AXES_FC = "#FFFFFF"   # fond axes : blanc pur
_GRID_C  = "#E8E8ED"   # séparateur Apple
_C_TITLE = "#1D1D1F"   # noir Apple (titre)
_C_LABEL = "#6E6E73"   # gris secondaire Apple (axes, légendes)
_C_SPINE = "#D2D2D7"   # gris tertiaire Apple (bordures)

plt.rcParams.update({
    "figure.figsize":        (10, 6),
    "figure.dpi":            140,
    "figure.facecolor":      _AXES_FC,
    "axes.facecolor":        _AXES_FC,
    "savefig.facecolor":     _AXES_FC,
    "font.family":           _SF,
    "font.size":             11,
    "text.color":            _C_TITLE,
    "axes.titlesize":        17,
    "axes.titleweight":      "semibold",
    "axes.titlecolor":       _C_TITLE,
    "axes.labelsize":        12,
    "axes.labelcolor":       _C_LABEL,
    "axes.spines.top":       False,
    "axes.spines.right":     False,
    "axes.spines.left":      False,
    "axes.spines.bottom":    False,
    "axes.axisbelow":        True,
    "axes.grid":             True,
    "grid.color":            "#E5E5EA",
    "grid.linewidth":        1.0,
    "xtick.color":           "#8E8E93",
    "ytick.color":           "#8E8E93",
    "xtick.labelsize":       11,
    "ytick.labelsize":       11,
    "xtick.major.size":      0,
    "ytick.major.size":      0,
    "legend.frameon":        False,
    "legend.fontsize":       10.5,
})

# ─── Système couleur / trait ──────────────────────────────────────────────────

# Palette Okabe–Ito  →  couleur = méthode mathématique
COL = {"rect": "#0072B2", "trap": "#E69F00", "simp": "#009E73"}
# Style de trait     →  implémentation
LS  = {"python": "-", "numpy": (0, (5, 3)), "scipy": (0, (1, 2.5))}
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
    x = linspace(a, b, n + 1)
    return float(integrate.trapezoid(evaluer_poly(x, p1, p2, p3, p4), x))


def scipy_simpson(p1, p2, p3, p4, a, b, n):
    if n % 2 != 0:
        n += 1
    x = linspace(a, b, n + 1)
    return float(integrate.simpson(evaluer_poly(x, p1, p2, p3, p4), x))


def mesurer_temps(func, args, repetitions=200):
    return timeit.Timer(lambda: func(*args)).timeit(number=repetitions) / repetitions


# ─── Helpers style Apple WWDC ────────────────────────────────────────────────

def _apple_line(ax, x, y, meth, impl):
    """Ligne épaisse arrondie + petit point blanc à chaque mesure."""
    c  = COL[meth]
    ls = LS[impl]
    ax.plot(x, y, color=c, ls=ls, lw=3,
            solid_capstyle="round", dash_capstyle="round",
            solid_joinstyle="round", zorder=3)
    ax.plot(x, y, "o", color=c, ms=4,
            markerfacecolor="white", markeredgewidth=1.6, zorder=4)


def _label_fin(ax, x, y, txt, meth):
    """Étiquette colorée en bout de courbe."""
    ax.annotate(txt, xy=(x, y), xytext=(8, 0),
                textcoords="offset points",
                color=COL[meth], fontsize=12, fontweight="semibold",
                va="center")


def _cle_impl(ax):
    """Petite légende de style de trait sous le graphe."""
    ax.text(0.0, -0.15,
            "⸻ Python      – – NumPy      ·· SciPy",
            transform=ax.transAxes,
            color="#8E8E93", fontsize=10)


# ─── Figure 1 : Convergence des méthodes ─────────────────────────────────────

def graphique_convergence(liste_n, dict_erreurs,
                           titre="Convergence des méthodes", save_path=None):
    n = array(liste_n, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, axis="y")
    ax.grid(False, axis="x")

    for nom, vals in dict_erreurs.items():
        nn   = nom.lower()
        meth = "rect" if "rect" in nn else "trap" if "trap" in nn else "simp"
        impl = "scipy" if "scipy" in nn else "numpy" if "numpy" in nn else "python"
        _apple_line(ax, n, vals, meth, impl)

    # ── Bande précision machine ───────────────────────────────────────────────
    ax.axhspan(1e-16, 1e-14, color=COL["simp"], alpha=0.08, lw=0)
    ax.text(n[0] * 1.1, 3e-15, "précision machine",
            color=COL["simp"], fontsize=9.5)

    # ── Repère de pente −2 ────────────────────────────────────────────────────
    vals_ordre2 = [v for v in dict_erreurs.values() if v[0] > 1e-10]
    if vals_ordre2:
        ref   = max(v[0] for v in vals_ordre2) * 1.4
        guide = ref * (n[0] / n) ** 2
        ax.plot(n, guide, color="#C7C7CC", ls=(0, (5, 4)), lw=1.2, zorder=0)
        ax.text(n[3] * 1.05, guide[3] * 0.38,
                "pente −2", color="#C7C7CC", fontsize=9, rotation=-26)

    # ── Étiquettes au bout — écartées si trop proches en log ─────────────────
    targets = []
    for meth_key, label in [("rect", "Rectangle"), ("trap", "Trapèze"), ("simp", "Simpson")]:
        candidats = {k: v for k, v in dict_erreurs.items()
                     if meth_key in k.lower() and "python" in k.lower()}
        if candidats:
            vals = list(candidats.values())[0]
            targets.append((max(vals[-1], 2e-16), label, meth_key))

    targets.sort(key=lambda t: t[0], reverse=True)
    MIN_GAP = 1.2  # décades minimum entre deux étiquettes
    adjusted, prev_log = [], None
    for y_end, label, meth_key in targets:
        log_y = log10(y_end)
        if prev_log is not None and prev_log - log_y < MIN_GAP:
            log_y = prev_log - MIN_GAP
        adjusted.append((10 ** log_y, label, meth_key))
        prev_log = log_y
    for y_end, label, meth_key in adjusted:
        _label_fin(ax, n[-1], y_end, label, meth_key)

    all_vals = [v for vals in dict_erreurs.values() for v in vals if v > 0]
    ymax = max(all_vals) * 5 if all_vals else 3
    ax.set_xlim(n[0] * 0.8, n[-1] * 4.0)
    ax.set_ylim(1e-16, ymax)
    ax.set_xlabel("Nombre de segments n")
    ax.set_ylabel("Erreur absolue")
    ax.set_title(titre, loc="left", pad=16)
    _cle_impl(ax)
    fig.subplots_adjust(left=0.11, right=0.80, top=0.90, bottom=0.19)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


# ─── Figure 2 : Temps de calcul vs segments ───────────────────────────────────

def graphique_temps(liste_n, dict_temps,
                    titre="Temps de calcul vs segments", save_path=None):
    n = array(liste_n, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, axis="y")
    ax.grid(False, axis="x")

    for nom, vals in dict_temps.items():
        nn   = nom.lower()
        meth = "rect" if "rect" in nn else "trap" if "trap" in nn else "simp"
        impl = "scipy" if "scipy" in nn else "numpy" if "numpy" in nn else "python"
        _apple_line(ax, n, vals, meth, impl)

    # ── Point de croisement Python → NumPy ───────────────────────────────────
    noms_py = [k for k in dict_temps if "python" in k.lower() and "rect" in k.lower()]
    noms_np = [k for k in dict_temps if "numpy"  in k.lower() and "rect" in k.lower()]
    if noms_py and noms_np:
        t_py = array(dict_temps[noms_py[0]])
        t_np = array(dict_temps[noms_np[0]])
        idx  = where(diff(sign(t_np - t_py)))[0]
        if len(idx) > 0:
            n_cross = int(liste_n[idx[0]])
            y_cross = dict_temps[noms_np[0]][idx[0]]
        else:
            n_cross, y_cross = 40, 1e-5
        ax.axvline(n_cross, color="#C7C7CC", ls=":", lw=1.5, zorder=0)
        ax.annotate(
            f"n ≈ {n_cross} : NumPy\nl'emporte",
            xy=(n_cross, y_cross),
            xytext=(n_cross * 4, y_cross * 3),
            fontsize=9.5, color=_C_TITLE,
            arrowprops=dict(arrowstyle="->", color="#C7C7CC", lw=1.4),
        )

    # ── Légende en bas à gauche (zone la moins chargée) ──────────────────────
    handles = [
        Line2D([0], [0], color=COL["rect"], lw=2.5, label="Rectangle"),
        Line2D([0], [0], color=COL["trap"], lw=2.5, label="Trapèze"),
        Line2D([0], [0], color=COL["simp"], lw=2.5, label="Simpson"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=10, frameon=False)

    ax.set_xlabel("Nombre de segments n")
    ax.set_ylabel("Temps moyen par appel (s)")
    ax.set_title(titre, loc="left", pad=16)
    _cle_impl(ax)
    fig.subplots_adjust(left=0.11, right=0.95, top=0.90, bottom=0.19)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


# ─── Figures 3D (EXP 3 — coefficients p et bornes varient) ──────────────────

def _setup_ax3d(ax, fig):
    """Style Apple minimal pour axes 3D."""
    fig.patch.set_facecolor(_AXES_FC)
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.fill = False
        pane.set_edgecolor(_GRID_C)
    ax.tick_params(labelsize=9, colors="#8E8E93")
    ax.xaxis.label.set_color(_C_LABEL)
    ax.yaxis.label.set_color(_C_LABEL)
    ax.zaxis.label.set_color(_C_LABEL)


def graphique_convergence_3d(liste_n, convergence,
                              titre="Convergence 3D", save_path=None):
    """Courbes 3D : X=log₁₀(n), Y=cas, Z=log₁₀(erreur), couleur=méthode."""
    cas_labels = list(convergence.keys())
    log_n = log10(array(liste_n, dtype=float))

    fig = plt.figure(figsize=(8, 4.8))
    ax  = fig.add_subplot(111, projection="3d")
    _setup_ax3d(ax, fig)

    for meth_key, label, color in [
        ("rect", "Rectangle", COL["rect"]),
        ("trap", "Trapèze",   COL["trap"]),
        ("simp", "Simpson",   COL["simp"]),
    ]:
        for i, cas in enumerate(cas_labels):
            d     = convergence[cas]["dict_erreurs"]
            serie = next((v for k, v in d.items()
                          if meth_key in k.lower() and "python" in k.lower()), None)
            if serie is None:
                continue
            z = log10(clip(array(serie, dtype=float), 1e-16, None))
            ax.plot(log_n, [i] * len(log_n), z,
                    color=color, lw=2.2, alpha=0.85,
                    solid_capstyle="round", solid_joinstyle="round")

    ax.set_xlabel("log₁₀(n)", labelpad=6)
    ax.set_ylabel("Cas", labelpad=6)
    ax.set_zlabel("log₁₀(erreur)", labelpad=6)
    ax.set_yticks(range(len(cas_labels)))
    ax.set_yticklabels(cas_labels)
    ax.set_title(titre, fontsize=14, fontweight="semibold", color=_C_TITLE)

    handles = [Line2D([0], [0], color=COL[k], lw=2, label=l)
               for k, l in [("rect", "Rectangle"), ("trap", "Trapèze"), ("simp", "Simpson")]]
    ax.legend(handles=handles, fontsize=9, frameon=False)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def graphique_temps_3d(liste_n, convergence,
                        titre="Temps de calcul 3D", save_path=None):
    """Courbes 3D : X=log₁₀(n), Y=cas, Z=log₁₀(temps), couleur=méthode."""
    cas_labels = list(convergence.keys())
    log_n = log10(array(liste_n, dtype=float))

    fig = plt.figure(figsize=(8, 4.8))
    ax  = fig.add_subplot(111, projection="3d")
    _setup_ax3d(ax, fig)

    for meth_key, label, color in [
        ("rect", "Rectangle", COL["rect"]),
        ("trap", "Trapèze",   COL["trap"]),
        ("simp", "Simpson",   COL["simp"]),
    ]:
        for i, cas in enumerate(cas_labels):
            d     = convergence[cas]["dict_temps"]
            serie = next((v for k, v in d.items()
                          if meth_key in k.lower() and "python" in k.lower()), None)
            if serie is None:
                continue
            z = log10(clip(array(serie, dtype=float), 1e-20, None))
            ax.plot(log_n, [i] * len(log_n), z,
                    color=color, lw=2.2, alpha=0.85,
                    solid_capstyle="round", solid_joinstyle="round")

    ax.set_xlabel("log₁₀(n)", labelpad=6)
    ax.set_ylabel("Cas", labelpad=6)
    ax.set_zlabel("log₁₀(temps s)", labelpad=6)
    ax.set_yticks(range(len(cas_labels)))
    ax.set_yticklabels(cas_labels)
    ax.set_title(titre, fontsize=14, fontweight="semibold", color=_C_TITLE)

    handles = [Line2D([0], [0], color=COL[k], lw=2, label=l)
               for k, l in [("rect", "Rectangle"), ("trap", "Trapèze"), ("simp", "Simpson")]]
    ax.legend(handles=handles, fontsize=9, frameon=False)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def _pill3d(ax, cx, cy, height, radius, color, alpha=0.82):
    """Cylindre surmonté d'un dôme hémisphérique (pillule 3D debout à z=0)."""
    if height <= 0:
        return
    from numpy import linspace, cos, sin, pi, zeros_like, meshgrid as mg

    n_th   = 32
    theta  = linspace(0, 2 * pi, n_th)
    dome_r = min(radius, height * 0.40)
    cyl_h  = height - dome_r
    kw = dict(color=color, alpha=alpha, linewidth=0, antialiased=True, shade=True)

    # Corps cylindrique
    T, Z = mg(theta, linspace(0, cyl_h, 24))
    ax.plot_surface(cx + radius * cos(T), cy + radius * sin(T), Z, **kw)

    # Dôme hémisphérique (phi : équateur → pôle)
    T2, P = mg(theta, linspace(pi / 2, 0, 16))
    ax.plot_surface(cx + dome_r * sin(P) * cos(T2),
                    cy + dome_r * sin(P) * sin(T2),
                    cyl_h + dome_r * cos(P), **kw)

    # Fond plat
    T3, R = mg(theta, linspace(0, radius, 8))
    ax.plot_surface(cx + R * cos(T3), cy + R * sin(T3),
                    zeros_like(R), **{**kw, "shade": False})


def graphique_erreur_3d(liste_n, convergence,
                         titre="Erreur par méthode — vue 3D", save_path=None):
    """Pillules 3D : X=cas, Y=méthode, hauteur=−log₁₀(erreur) à n max."""
    cas_labels = list(convergence.keys())
    meth_items = [
        ("rect", "Rectangle", COL["rect"]),
        ("trap", "Trapèze",   COL["trap"]),
        ("simp", "Simpson",   COL["simp"]),
    ]

    fig = plt.figure(figsize=(8, 4.8))
    ax  = fig.add_subplot(111, projection="3d")
    _setup_ax3d(ax, fig)

    for j, (meth_key, label, color) in enumerate(meth_items):
        for i, cas in enumerate(cas_labels):
            d     = convergence[cas]["dict_erreurs"]
            serie = next((v for k, v in d.items()
                          if meth_key in k.lower() and "python" in k.lower()), None)
            if serie is None:
                continue
            height = -log10(max(serie[-1], 1e-16))
            _pill3d(ax, i, j, height, radius=0.22, color=color)

    ax.set_xlabel("Cas", labelpad=6)
    ax.set_ylabel("Méthode", labelpad=6)
    ax.set_zlabel("−log₁₀(erreur)", labelpad=6)
    ax.set_xticks(range(len(cas_labels)))
    ax.set_xticklabels(cas_labels)
    ax.set_yticks(range(len(meth_items)))
    ax.set_yticklabels([l for _, l, _ in meth_items])
    ax.set_title(titre, fontsize=14, fontweight="semibold", color=_C_TITLE)

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

    erreurs = array([dict_erreurs[m] for m in methodes])
    data    = log10(clip(erreurs, 1e-16, None))

    n_rows, n_cols = len(methodes), len(liste_n)
    norm = Normalize(vmin=min(data.min(), -15), vmax=0)

    # ── Dimensions de la grille ───────────────────────────────────────────────
    cell_w, cell_h, gap = 1.0, 0.72, 0.14
    left_margin  = 3.1
    bottom_extra = 1.2   # espace pour le label n + barre de légende

    total_w = (left_margin + n_cols * (cell_w + gap)) * 0.74
    total_h = (0.7 + n_rows * (cell_h + gap) + bottom_extra) * 0.74

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
                fontfamily=_SF_MONO, color=_C_TITLE)

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

            txt_col = "#FFFFFF" if t < 0.55 else _C_TITLE
            ax.text(x + cell_w / 2, row_y + cell_h / 2,
                    f"{val:.1f}",
                    ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=txt_col,
                    fontfamily=_SF_MONO)

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
            ha="center", va="bottom", fontsize=14, fontweight="semibold",
            fontfamily=_SF)
    # sous-titre explicatif (une ligne en dessous)
    ax.text(mid_x, top_hd + 0.58,
            r"chaque cellule = $\log_{10}|I_{num}-I_{exact}|$  "
            r"(ex. : $-14 \Rightarrow$ erreur $\approx 10^{-14}$)",
            ha="center", va="bottom", fontsize=9, color=_C_LABEL, style="italic")

    # ── Label « Nombre de segments n → » ─────────────────────────────────────
    label_y = -(cell_h + gap) * 0.25
    ax.text(mid_x, label_y, "Nombre de segments n →",
            ha="center", va="top", fontsize=10, color=_C_LABEL)

    # ── Barre de légende arrondie ─────────────────────────────────────────────
    bar_y     = label_y - 0.45
    bar_left  = 0.0
    bar_right = n_cols * (cell_w + gap) - gap
    bar_h     = 0.28

    # gradient 1D rouille → vert, dessiné directement sur ax
    grad = linspace(1, 0, 256).reshape(1, -1)
    im = ax.imshow(
        grad, aspect="auto", cmap=_CMAP_ERREUR,
        extent=[bar_left, bar_right, bar_y, bar_y + bar_h],
        zorder=2,
    )

    # forme pillule : rounding_size = moitié de la hauteur
    bar_clip = FancyBboxPatch(
        (bar_left, bar_y),
        bar_right - bar_left, bar_h,
        boxstyle=f"round,pad=0,rounding_size={bar_h / 2}",
        transform=ax.transData,
        facecolor="none", edgecolor="none",
    )
    ax.add_patch(bar_clip)
    im.set_clip_path(bar_clip)

    # labels de la barre
    ax.text(bar_left - 0.2, bar_y + bar_h / 2, "erreur élevée\n(log₁₀ ≈ 0)",
            ha="right", va="center", fontsize=9, color=_C_LABEL)
    ax.text(bar_right + 0.2, bar_y + bar_h / 2, "précision machine\n(log₁₀ ≈ −16)",
            ha="left", va="center", fontsize=9, color=_C_LABEL)

    fig.tight_layout(pad=0.4)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=_FIG_FC)
    return fig
