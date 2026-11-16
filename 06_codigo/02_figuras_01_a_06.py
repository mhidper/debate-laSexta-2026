import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import numpy as np

for f in fm.findSystemFonts():
    if "Inter" in f:
        fm.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 11, "axes.edgecolor": "#c9c8c2",
                     "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b"})

BG = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#a5a49c"; GRID = "#e6e5e0"
BLUE = "#2a78d6"
GOOD = "#1b8a5a"; WARN = "#e0a100"; NEUTRAL = "#b9b8b1"; CRIT = "#d03b3b"
FUENTE_BASE = "Fuente: transcripción del debate de laSexta (13-11-2026), elaboración propia."
FIRMA = "@manuj_hidalgo"
CANDS = ["Carlos Cuerpo\n(PSOE)", "Juan Bravo\n(PP)", "José M.ª Figaredo\n(Vox)", "Pablo Bustinduy\n(Frente Amplio)"]


def lienzo(titulo, sub, fuente, h=9):
    fig = plt.figure(figsize=(16, h), dpi=100, facecolor=BG)
    fig.text(0.045, 0.94, titulo, fontsize=27, fontweight="bold", color=INK, va="top")
    fig.text(0.045, 0.865, sub, fontsize=16, color=INK2, va="top")
    fig.text(0.045, 0.035, fuente, fontsize=11.5, color=INK2, va="bottom")
    fig.text(0.955, 0.035, FIRMA, fontsize=12, color=INK2, va="bottom", ha="right", fontweight="medium")
    return fig


def limpio(ax, grid_x=True):
    ax.set_facecolor(BG)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    if grid_x:
        ax.xaxis.grid(True, color=GRID, lw=1); ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=13)


# 1. Reparto de palabras y densidad de cifras -------------------------------
# Palabras con el criterio único de tokens (v2/tokens.py) y cifras citadas (29, 45, 22, 40)
pal = [4302, 4546, 3579, 4217]
cif = [round(c / p * 1000, 1) for c, p in zip([29, 45, 22, 40], pal)]
tot = sum(pal)
fig = lienzo("El tiempo se repartió de forma pareja, las cifras no",
             "Cuota de palabras de cada candidato (un reparto igual sería el 25 %) y cifras citadas por cada 1.000 palabras",
             FUENTE_BASE + " Cifras = números con unidad (%, €, millones, viviendas…).\nPalabras contadas sin signos de puntuación ni marcas de transcripción ([…], [atribución probable]).")
ax1 = fig.add_axes([0.17, 0.14, 0.34, 0.62]); ax2 = fig.add_axes([0.6, 0.14, 0.34, 0.62])
y = np.arange(4)[::-1]
for ax, vals, fmt, ttl, mx in [(ax1, [p / tot * 100 for p in pal], "{:.1f} %", "Cuota de palabras", 32),
                               (ax2, cif, "{:.1f}", "Cifras por cada 1.000 palabras", 11.5)]:
    limpio(ax)
    ax.barh(y, vals, color=MUTED, height=0.56)
    for yi, v in zip(y, vals):
        ax.text(v + mx * 0.015, yi, fmt.format(v).replace(".", ","), va="center", fontsize=15, color=INK, fontweight="medium")
    ax.set_xlim(0, mx); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.xaxis.grid(False)
    ax.set_title(ttl, loc="left", fontsize=15, color=INK2, pad=12)
ax1.set_yticks(y); ax1.set_yticklabels(CANDS, fontsize=14)
ax2.set_yticks(y); ax2.set_yticklabels([])
fig.savefig("01_tiempo_y_cifras.png", facecolor=BG); plt.close(fig)

# 2. Verificaciones -----------------------------------------------------------
cats = ["Correcta", "Necesita contexto", "Sin corroborar o no comparable", "Falsa"]
cols = [GOOD, WARN, NEUTRAL, CRIT]
newtral = {"Cuerpo": [2, 1, 0, 0], "Bravo": [3, 4, 1, 0], "Figaredo": [3, 4, 1, 1], "Bustinduy": [2, 2, 1, 0]}
propia = {"Cuerpo": [2, 0, 0, 0], "Bravo": [1, 2, 2, 0], "Figaredo": [0, 1, 0, 0], "Bustinduy": [0, 1, 1, 0]}
fig = lienzo("Pocos datos falsos, muchos datos sin contexto",
             "Afirmaciones verificadas por candidato y valoración (número de afirmaciones)",
             "Fuente: verificación en directo de Newtral (13-11-2026) y comprobación propia con fuentes públicas enlazadas en el hilo. "
             "Las valoraciones agrupan las explicaciones de Newtral en cuatro categorías.\n"
             "Newtral elige qué verifica: los recuentos no son una muestra aleatoria y no permiten ordenar a los candidatos por fiabilidad.", h=9.6)
for i, (d, ttl) in enumerate([(newtral, "Verificadas por Newtral (25)"), (propia, "Sin verificar por Newtral: comprobación propia (10)")]):
    ax = fig.add_axes([0.17 + i * 0.43, 0.17, 0.34, 0.5]); limpio(ax)
    keys = ["Cuerpo", "Bravo", "Figaredo", "Bustinduy"]
    for yi, k in zip(y, keys):
        left = 0
        for j, v in enumerate(d[k]):
            if v:
                ax.barh(yi, v - 0.06, left=left + 0.03, color=cols[j], height=0.56)
                ax.text(left + v / 2, yi, str(v), ha="center", va="center", fontsize=14,
                        color="white" if j in (0, 3) else INK, fontweight="bold")
            left += v
    ax.set_xlim(0, 9.5); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.xaxis.grid(False)
    ax.set_title(ttl, loc="left", fontsize=15, color=INK2, pad=12)
    ax.set_yticks(y); ax.set_yticklabels(CANDS if i == 0 else [], fontsize=14)
hs = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cols]
fig.legend(hs, cats, loc="upper left", bbox_to_anchor=(0.165, 0.825), ncol=4, frameon=False, fontsize=13.5)
fig.savefig("02_verificaciones.png", facecolor=BG); plt.close(fig)

# 3. Índice de concreción -------------------------------------------------------
# (puntos, naturaleza): V = en vigor, N = instrumento nuevo, M = meta de resultado
punt = {"PSOE": [(3,"N"),(3,"V"),(3,"V"),(3,"V"),(2,"V"),(2,"V"),(2,"N")],
        "Frente Amplio": [(3,"N"),(3,"N"),(3,"N"),(2,"M"),(1,"N"),(1,"N")],
        "PP": [(2,"M"),(2,"M"),(2,"M"),(2,"N"),(2,"N"),(2,"N"),(1,"N"),(1,"N"),(1,"V")],
        "Vox": [(2,"N"),(1,"N"),(1,"N"),(1,"N"),(1,"V"),(0,"M")]}
EST = {"V": dict(color="#1d4f91", edgecolor=BG), "N": dict(color=MUTED, edgecolor=BG), "M": dict(color=BG, edgecolor=INK2)}
fig = lienzo("Cuánto concretó cada partido lo que prometió",
             "Puntuación de cada medida (0-4): un punto por instrumento, cuantía, plazo y financiación dichos en el debate",
             FUENTE_BASE + " La marca azul es la media del partido. PSOE: 2,6 en las 5 medidas en vigor y 2,5 en las 2 nuevas.\n"
             "PP: 1,6 en sus 5 instrumentos nuevos y 2,0 en sus 3 metas de resultado. El índice premia decir cifras, no que la medida sea viable.", h=9.4)
ax = fig.add_axes([0.17, 0.2, 0.77, 0.54]); limpio(ax)
for yi, (k, v) in zip(np.arange(4)[::-1], punt.items()):
    grp = {}
    for s, n in v:
        grp.setdefault(s, []).append(n)
    for s, ns in grp.items():
        ns = sorted(ns, key="VNM".index)
        offs = (np.arange(len(ns)) - (len(ns) - 1) / 2) * 0.13
        for o, n in zip(offs, ns):
            ax.scatter(s, yi + o, s=170, linewidth=2, zorder=3, **EST[n])
    m = np.mean([s for s, _ in v])
    ax.plot([m, m], [yi - 0.36, yi + 0.36], color=BLUE, lw=4, zorder=4, solid_capstyle="round")
    ax.text(m, yi + 0.43, f"media {m:.1f}".replace(".", ","), ha="center", fontsize=14, color=INK, fontweight="bold")
ax.set_yticks(np.arange(4)[::-1]); ax.set_yticklabels([f"{k}  ({len(v)} medidas)" for k, v in punt.items()], fontsize=14)
ax.set_xlim(-0.4, 4.4); ax.set_xticks(range(5)); ax.set_ylim(-0.6, 3.75)
ax.set_xlabel("Puntos (0 = solo una intención; 4 = instrumento, cuantía, plazo y financiación)", fontsize=13)
hs = [plt.Line2D([], [], marker="o", ls="", ms=12, markerfacecolor=EST[k]["color"], markeredgecolor=EST[k]["edgecolor"] if k == "M" else EST[k]["color"], markeredgewidth=2) for k in "VNM"]
fig.legend(hs, ["En vigor (BOE)", "Instrumento nuevo", "Meta o deseo macroeconómico"], loc="upper left", bbox_to_anchor=(0.165, 0.815), ncol=3, frameon=False, fontsize=13.5)
fig.savefig("03_concrecion.png", facecolor=BG); plt.close(fig)

# 4. Mapa de alusiones -------------------------------------------------------------
M = np.array([[np.nan, 36, 10, 1], [23, np.nan, 0, 5], [4, 1, np.nan, 3], [0, 18, 25, np.nan]])
names = ["Cuerpo (PSOE)", "Bravo (PP)", "Figaredo (Vox)", "Bustinduy (FA)"]
fig = lienzo("Dos debates en uno: PSOE contra PP y Frente Amplio contra Vox",
             "Veces que cada candidato (fila) nombra a un rival, a su partido o a su líder (columna)",
             FUENTE_BASE + " Menciones por nombre propio; no incluye alusiones genéricas («el Gobierno», «ustedes»).", h=9.4)
ax = fig.add_axes([0.25, 0.14, 0.5, 0.62]); ax.set_facecolor(BG)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("b", ["#eef4fc", "#1d5fb0"])
ax.imshow(np.nan_to_num(M, nan=-1), cmap=cmap, vmin=0, vmax=36)
for i in range(4):
    for j in range(4):
        if i == j:
            ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, color="#f1f0ec"))
            ax.text(j, i, "—", ha="center", va="center", color=MUTED, fontsize=18)
        else:
            v = int(M[i, j]); ax.text(j, i, str(v), ha="center", va="center", fontsize=20, fontweight="bold",
                                      color="white" if v > 17 else INK)
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=13.5); ax.xaxis.tick_top()
ax.set_yticks(range(4)); ax.set_yticklabels(names, fontsize=13.5)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
for x in np.arange(-.5, 4, 1):
    ax.axhline(x, color=BG, lw=4); ax.axvline(x, color=BG, lw=4)
fig.text(0.78, 0.55, "Bravo no nombró\na Vox ni a Figaredo\nen todo el debate.\n\nFigaredo nombró\nal PP una vez.", fontsize=14.5, color=INK, va="center")
fig.savefig("04_alusiones.png", facecolor=BG); plt.close(fig)

# 5. Tres medidas del bienestar ---------------------------------------------------
fig = lienzo("Mismo país, tres medidas: por qué todos pueden «tener razón»",
             "Variación según el indicador elegido (%). Periodos y conceptos distintos: no son comparables entre sí",
             "Fuentes: OCDE vía Newtral (renta disponible real de los hogares, 1T 2022-4T 2025); cálculo del PP sobre datos de AEAT e INE citado por El Español\n"
             "(salario mediano neto real, 2018-2024); INE, Encuesta de Estructura Salarial vía Newtral (salario modal bruto, nominal, 2018-2024).", h=9.4)
ax = fig.add_axes([0.36, 0.22, 0.58, 0.54]); limpio(ax)
lab = ["Renta disponible real de los hogares\n(la usa Cuerpo)", "Salario mediano neto real\n(la usa el PP)", "Salario más frecuente (moda),\nbruto y sin descontar inflación (la usa Figaredo)"]
val = [8.4, -3.4, -10.6]
yy = np.arange(3)[::-1]
ax.barh(yy, val, color=[GOOD if v > 0 else CRIT for v in val], height=0.5, alpha=0.75)
for yi, v in zip(yy, val):
    ax.text(v + (0.4 if v > 0 else -0.4), yi, f"{v:+.1f} %".replace(".", ","), va="center",
            ha="left" if v > 0 else "right", fontsize=17, fontweight="bold", color=INK)
ax.axvline(0, color=INK2, lw=1.2)
ax.set_xlim(-15, 13); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.xaxis.grid(False)
ax.set_yticks(yy); ax.set_yticklabels(lab, fontsize=13.5)
fig.text(0.36, 0.15, "Verde: sube. Rojo: baja. La moda salarial depende mucho de la composición del empleo\n(más empleo de salario bajo la reduce) y no mide lo que le pasa al sueldo de un trabajador concreto.",
         fontsize=12, color=INK2)
fig.savefig("05_tres_medidas.png", facecolor=BG); plt.close(fig)

# 6. Preguntas sin respuesta ---------------------------------------------------------
fig = lienzo("Preguntas directas que se quedaron sin respuesta",
             "Preguntas concretas (de la moderadora o de un rival) que el candidato no contestó o desvió",
             FUENTE_BASE + " Recuento propio sobre la transcripción; no se ajusta por el número de preguntas recibidas.", h=9)
ax = fig.add_axes([0.2, 0.16, 0.74, 0.6]); limpio(ax)
q = [2, 5, 4, 1]
ej = ["¿Intervención de precios, sí o no?", "¿Cuánto subirá el SMI? ¿Qué votó el PP en 2021?",
      "¿Cuánto invertirá en tren? ¿Cuántas viviendas sociales?", "¿Por qué creer que no se moverá la «línea roja»?"]
ax.barh(y, q, color=MUTED, height=0.56)
for yi, v, e in zip(y, q, ej):
    ax.text(v + 0.08, yi + 0.02, str(v), va="center", fontsize=17, fontweight="bold", color=INK)
    ax.text(v + 0.45, yi + 0.02, e, va="center", fontsize=13, color=INK2)
ax.set_xlim(0, 10); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.xaxis.grid(False)
ax.set_yticks(y); ax.set_yticklabels(CANDS, fontsize=14)
fig.savefig("06_preguntas.png", facecolor=BG); plt.close(fig)
print("ok")
