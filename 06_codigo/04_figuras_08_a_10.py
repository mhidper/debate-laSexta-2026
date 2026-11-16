exec(open('figuras.py').read().split('# 1. Reparto')[0])
from matplotlib.colors import LinearSegmentedColormap
y=np.arange(4)[::-1]
# 8. Tono
fig=lienzo("El tono más negativo fue el de Figaredo y el más positivo, el de Cuerpo",
           "Porcentaje de oraciones de cada candidato con saldo negativo según el léxico de sentimiento ML-SentiCon",
           "Fuente: elaboración propia con ML-SentiCon (Cruz, Troyano, Pontes y Ortega, 2014, Universidad de Sevilla), con lematización y negación simple.\n"
           "Punto claro: solo palabras revisadas a mano (capas 1-4). Punto oscuro: léxico completo. Quien defiende su gestión tiende a sonar más positivo.",h=9.4)
ax=fig.add_axes([0.2,0.2,0.74,0.56]);limpio(ax)
rev=[3.1,4.2,7.4,5.5]; full=[6.2,7.5,17.9,10.3]
for yi,a,b in zip(y,rev,full):
    ax.plot([a,b],[yi,yi],color=GRID,lw=6,solid_capstyle='round',zorder=1)
    ax.scatter(a,yi,s=260,color="#9cc0ea",zorder=3);ax.scatter(b,yi,s=260,color=BLUE,zorder=3)
    ax.text(a-0.6,yi,f"{a:.1f} %".replace('.',','),ha='right',va='center',fontsize=14,color=INK2)
    ax.text(b+0.6,yi,f"{b:.1f} %".replace('.',','),ha='left',va='center',fontsize=15,color=INK,fontweight='bold')
ax.set_yticks(y);ax.set_yticklabels(CANDS,fontsize=14);ax.set_xlim(0,21);ax.set_xticks([0,5,10,15,20]);ax.set_xticklabels(['0 %','5 %','10 %','15 %','20 %'])
ax.set_ylim(-0.6,3.6)
fig.savefig("08_tono.png",facecolor=BG);plt.close(fig)

# 9. Incivilidad
cats=["Acusar de mentir","Descalificación personal","Desprecio del discurso ajeno","Atribuir malas intenciones"]
cols=["#1d4f91","#2a78d6","#7fb0e8","#bcd5f3"]
import json as _j
_r=_j.load(open("/home/claude/v2/incivilidad_resumen.json"))
_k={"Cuerpo":"Carlos Cuerpo","Bravo":"Juan Bravo","Figaredo":"José María Figaredo","Bustinduy":"Pablo Bustinduy"}
d={k:_r[v]["cats"] for k,v in _k.items()}
w={k:_r[v]["palabras"] for k,v in _k.items()}
fig=lienzo("La agresividad verbal, medida con un esquema habitual en la literatura",
           "Expresiones incívicas dirigidas a rivales presentes, por cada 1.000 palabras (categorías inspiradas en Coe, Kenski y Rains, 2014)",
           "Fuente: elaboración propia. Diccionario, revisión manual en contexto y deduplicación (una oración o una misma expresión repetida en la misma intervención cuenta una vez).\n"
           "Se excluyen términos dirigidos a terceros ausentes (fondos, migrantes…). Recuento depurado: Cuerpo 5, Bravo 12, Figaredo 10, Bustinduy 15.",h=9.6)
ax=fig.add_axes([0.2,0.2,0.74,0.52]);limpio(ax)
for yi,k in zip(y,d):
    left=0
    for j,v in enumerate(d[k]):
        r=v/w[k]*1000
        if v: ax.barh(yi,r-0.03,left=left+0.015,color=cols[j],height=0.56)
        left+=r
    ax.text(left+0.06,yi,f"{left:.1f}".replace('.',','),va='center',fontsize=16,fontweight='bold',color=INK)
ax.set_yticks(y);ax.set_yticklabels(CANDS,fontsize=14);ax.set_xlim(0,4.8);ax.set_xticks([])
ax.spines['bottom'].set_visible(False);ax.xaxis.grid(False)
hs=[plt.Rectangle((0,0),1,1,color=c) for c in cols]
fig.legend(hs,cats,loc='upper left',bbox_to_anchor=(0.195,0.80),ncol=4,frameon=False,fontsize=13)
fig.savefig("09_incivilidad.png",facecolor=BG);plt.close(fig)

# 10. Agenda de crecimiento
terms=["Productividad","Competitividad","I+D+i y tecnología","Inversión empresarial\no productiva","Industria","Inversión pública\n(infraestructuras)"]
M=np.array([[1,0,0,0,0,17],[6,6,1,2,0,6],[0,0,1,0,9,4],[0,0,0,1,1,4]])
names=["Cuerpo (PSOE)","Bravo (PP)","Figaredo (Vox)","Bustinduy (FA)"]
fig=lienzo("¿Quién habló de productividad, tecnología e inversión?",
           "Menciones de cada término por candidato, clasificadas a mano según su sentido en cada frase",
           "Fuente: elaboración propia sobre la transcripción. No se cuentan «fondos de inversión» ni «inversores» en vivienda (5 de Bustinduy), ni «investigación» de accidentes.\n"
           "«Productividad» cuenta solo la palabra; «economía productiva» o «sectores productivos» (3 de Figaredo, 3 de Bustinduy) quedan fuera.",h=9.6)
ax=fig.add_axes([0.2,0.17,0.62,0.56]);ax.set_facecolor(BG)
cmap=LinearSegmentedColormap.from_list("b",["#f3f7fd","#1d5fb0"])
ax.imshow(M,cmap=cmap,vmin=0,vmax=17,aspect='auto')
for i in range(4):
    for j in range(6):
        v=M[i,j];ax.text(j,i,str(v),ha='center',va='center',fontsize=19,fontweight='bold',color='white' if v>8 else (MUTED if v==0 else INK))
ax.set_xticks(range(6));ax.set_xticklabels(terms,fontsize=12.5);ax.xaxis.tick_top()
ax.set_yticks(range(4));ax.set_yticklabels(names,fontsize=13.5)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
for x in np.arange(-.5,6,1): ax.axvline(x,color=BG,lw=4)
for x in np.arange(-.5,4,1): ax.axhline(x,color=BG,lw=4)
ax.axvline(4.5,color=INK2,lw=1.2,ls=(0,(3,3)))
fig.text(0.84,0.45,"Bravo es quien más\nnombra productividad\ny competitividad (12),\npero sin medidas salvo\nI+D+i en Sociedades y\nlibertad de amortización.\n\nCuerpo habla de\ninversión casi solo\nen infraestructuras.",fontsize=13,color=INK,va='center')
fig.savefig("10_agenda_crecimiento.png",facecolor=BG);plt.close(fig)
print('ok')
