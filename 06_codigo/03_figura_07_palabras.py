import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from wordcloud import WordCloud
for f in fm.findSystemFonts():
    if "Inter" in f: fm.fontManager.addfont(f)
plt.rcParams["font.family"]="Inter"
FONT=[f for f in fm.findSystemFonts() if f.endswith("Inter-SemiBold.otf")][0]
BG="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"
d=json.load(open("distintivas.json"))
fuera={"torno","materia","directamente","bastante","contar","hablado","prácticamente","cualquier","hablan","producido","decidido","supone","seguir","auténticamente","elemento","principales","necesarias","presentado","poder","importante","baja","redes","costa","arriba","hablado","clave","mano","obra"}
cands=[("Carlos Cuerpo","Carlos Cuerpo (PSOE)"),("Juan Bravo","Juan Bravo (PP)"),("José María Figaredo","José M.ª Figaredo (Vox)"),("Pablo Bustinduy","Pablo Bustinduy (Frente Amplio)")]
fig=plt.figure(figsize=(16,10),dpi=100,facecolor=BG)
fig.text(0.045,0.955,"Las palabras que distinguen a cada candidato",fontsize=27,fontweight="bold",color=INK,va="top")
fig.text(0.045,0.895,"Palabras que cada uno usa mucho más que los otros tres (log-odds con prior informativo). El tamaño refleja cuánto le distingue, no cuántas veces la dijo",fontsize=14.5,color=INK2,va="top")
for i,(k,lab) in enumerate(cands):
    w={a:s for a,s,n in d[k] if a not in fuera and s>0}
    w=dict(sorted(w.items(),key=lambda x:-x[1])[:22])
    wc=WordCloud(width=1000,height=520,background_color=BG,font_path=FONT,prefer_horizontal=1.0,
                 color_func=lambda *a,**kw:"#3b3a37",relative_scaling=0.6,max_font_size=120,min_font_size=18,margin=6,random_state=3).generate_from_frequencies({a:s**2 for a,s in w.items()})
    ax=fig.add_axes([0.045+(i%2)*0.47,0.47-(i//2)*0.39,0.44,0.33])
    ax.imshow(wc,interpolation="bilinear"); ax.axis("off")
    fig.text(0.045+(i%2)*0.47,0.47-(i//2)*0.39+0.345,lab,fontsize=17,fontweight="bold",color=INK)
fig.text(0.045,0.03,"Fuente: transcripción del debate de laSexta (13-11-2026), elaboración propia. Sin palabras vacías ni muletillas; cada uno frente al resto de candidatos (moderadora excluida).",fontsize=11.5,color=INK2)
fig.text(0.955,0.03,"@manuj_hidalgo",fontsize=12,color=INK2,ha="right")
fig.savefig("07_palabras.png",facecolor=BG)
for k,lab in cands:
    print(lab,[a for a,s,n in d[k] if a not in fuera][:22])
