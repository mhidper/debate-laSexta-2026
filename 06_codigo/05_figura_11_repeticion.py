exec(open('figuras.py').read().split('# 1. Reparto')[0])
y=np.arange(4)[::-1]
fig=lienzo("Bravo tuvo el discurso más variado y los otros tres, muy parecidos",
           "Diversidad léxica y repetición de frases de cada candidato",
           "Fuente: elaboración propia sobre la transcripción. Izquierda: proporción media de palabras distintas en tramos de 100 palabras (medida similar a MATTR), con intervalo\n"
           "de confianza al 95 % por bootstrap. MTLD y HD-D dan el mismo orden para Bravo. Derecha: porcentaje de secuencias de cinco palabras que el candidato repite.",h=9.6)
ax1=fig.add_axes([0.2,0.2,0.36,0.52]);ax2=fig.add_axes([0.66,0.2,0.28,0.52])
m=[0.655, 0.679, 0.645, 0.651];lo=[0.64, 0.664, 0.631, 0.635];hi=[0.67, 0.694, 0.661, 0.668]
limpio(ax1)
for yi,a,l,h in zip(y,m,lo,hi):
    col=BLUE if a==max(m) else MUTED
    ax1.plot([l,h],[yi,yi],color=col,lw=3,solid_capstyle='round');ax1.scatter(a,yi,s=230,color=col,zorder=3,edgecolor=BG,linewidth=2)
    ax1.text(h+0.003,yi,f"{a:.3f}".replace('.',','),va='center',fontsize=15,fontweight='bold',color=INK)
ax1.set_xlim(0.615,0.705);ax1.set_xticks([0.62,0.64,0.66,0.68,0.70]);ax1.set_xticklabels(['0,62','0,64','0,66','0,68','0,70'])
ax1.set_yticks(y);ax1.set_yticklabels(CANDS,fontsize=14);ax1.set_ylim(-0.6,3.6)
ax1.set_title("Diversidad léxica (más alto = menos repetitivo)",loc='left',fontsize=14.5,color=INK2,pad=12)
limpio(ax2)
r5=[1.7, 1.7, 2.3, 3.1]
ax2.barh(y,r5,color=MUTED,height=0.5)
for yi,v in zip(y,r5): ax2.text(v+0.06,yi,f"{v:.1f} %".replace('.',','),va='center',fontsize=15,fontweight='bold',color=INK)
ax2.set_xlim(0,3.9);ax2.set_xticks([]);ax2.spines['bottom'].set_visible(False);ax2.xaxis.grid(False)
ax2.set_yticks(y);ax2.set_yticklabels([]);ax2.set_ylim(-0.6,3.6)
ax2.set_title("Frases de cinco palabras repetidas",loc='left',fontsize=14.5,color=INK2,pad=12)
fig.savefig("11_repeticion.png",facecolor=BG);plt.close(fig)
print('ok')
