exec(open('figuras.py').read().split('# 1. Reparto')[0])
y=np.arange(4)[::-1]
cats=["Respaldada","Mixta","Débil o contraria","Sin evidencia suficiente"]
cols=[GOOD,WARN,CRIT,NEUTRAL]
d={"PSOE":[1,2,1,0],"PP":[2,3,2,2],"Vox":[0,2,2,1],"Frente Amplio":[1,5,0,2]}
fig=lienzo("Pocas propuestas con respaldo claro en la literatura económica",
           "Propuestas y diagnósticos de cada partido según lo que dice la evidencia empírica sobre su objetivo (número de medidas)",
           "Fuente: elaboración propia a partir de la literatura citada en el hilo (Banco de España, AIReF, Saiz, González y Ortega, Diamond et al., Carozzi et al., Zwick y Mahon, entre otros).\n"
           "20 medidas evaluadas; las compartidas cuentan para cada partido que las defendió. «Mixta» no significa mala: el resultado depende del diseño.",h=9.6)
ax=fig.add_axes([0.17,0.2,0.77,0.52]);limpio(ax)
for yi,k in zip(y,d):
    left=0
    for j,v in enumerate(d[k]):
        if v:
            ax.barh(yi,v-0.06,left=left+0.03,color=cols[j],height=0.56,alpha=0.85)
            ax.text(left+v/2,yi,str(v),ha='center',va='center',fontsize=15,fontweight='bold',color='white' if j in (0,2) else INK)
        left+=v
    ax.text(left+0.12,yi,f"{left} medidas",va='center',fontsize=13,color=INK2)
ax.set_yticks(y);ax.set_yticklabels(list(d),fontsize=15);ax.set_xlim(0,10.5);ax.set_xticks([])
ax.spines['bottom'].set_visible(False);ax.xaxis.grid(False)
hs=[plt.Rectangle((0,0),1,1,color=c,alpha=0.85) for c in cols]
fig.legend(hs,cats,loc='upper left',bbox_to_anchor=(0.165,0.80),ncol=4,frameon=False,fontsize=13.5)
fig.savefig("12b_evidencia_absoluta.png",facecolor=BG);plt.close(fig);print('ok')

# 12. Versión normalizada al 100 %
fig=lienzo("Pocas propuestas con respaldo claro en la literatura económica",
           "Reparto de las propuestas y diagnósticos de cada partido según lo que dice la evidencia empírica (% del total de cada partido)",
           "Fuente: elaboración propia a partir de la literatura citada en el hilo (Banco de España, AIReF, Saiz, González y Ortega, Diamond et al., Carozzi et al., Zwick y Mahon, entre otros).\n"
           "20 medidas únicas y 26 valoraciones: las compartidas cuentan para cada partido que las defendió. «Mixta» no significa mala: el resultado depende del diseño.",h=9.6)
ax=fig.add_axes([0.2,0.2,0.74,0.52]);limpio(ax)
for yi,k in zip(y,d):
    n=sum(d[k]);left=0
    for j,v in enumerate(d[k]):
        p=v/n*100
        if v:
            ax.barh(yi,p-0.6,left=left+0.3,color=cols[j],height=0.56,alpha=0.85)
            if p>=9: ax.text(left+p/2,yi,f"{int(p+0.5)} %\n({v})",ha='center',va='center',fontsize=13.5,fontweight='bold',color='white' if j in (0,2) else INK,linespacing=1.1)
        left+=p
ax.set_yticks(y);ax.set_yticklabels([f"{k} (n = {sum(d[k])})" for k in d],fontsize=15);ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_xticklabels(['0 %','25 %','50 %','75 %','100 %'])
ax.xaxis.grid(False);ax.spines['bottom'].set_visible(False);ax.tick_params(axis='x',labelsize=12.5,colors=INK2)
fig.legend(hs,cats,loc='upper left',bbox_to_anchor=(0.195,0.80),ncol=4,frameon=False,fontsize=13.5)
fig.savefig("12_evidencia.png",facecolor=BG);plt.close(fig);print('ok100')
