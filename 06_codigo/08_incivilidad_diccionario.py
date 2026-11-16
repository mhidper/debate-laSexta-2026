import json,re,collections
tx=json.load(open('/home/claude/hilo/textos.json'))
C=['Carlos Cuerpo','Juan Bravo','José María Figaredo','Pablo Bustinduy']
D={
 'Acusar de mentir':[r'\bment\w*', r'\bmiente\w*', r'\bfals[oa]s?\b', r'\bengañ\w+', r'falt\w+ a la verdad', r'torticer\w+', r'manipul\w+'],
 'Descalificación personal':[r'\bcasta\b', r'\bcorrupt[oa]s?\b', r'\bamigotes\b', r'\bchiringuito', r'\bvasallo', r'\bobscen\w+', r'\brob(ar|arlo|ado|aron)\b', r'\bladr[oó]n\w*', r'\breincidente', r'\bsanchismo', r'\bbrazo político', r'cazatalentos', r'colocad[ao]', r'\bnervios\w*', r'su jefe', r'su amigo'],
 'Desprecio del discurso':[r'dibujos animados', r'popurr[ií]', r'cartelitos', r'cantado bingo', r'larguísimo discurso', r'política ficción', r'\bcuento\b', r'son deseos', r'falta calle', r'le falta calle'],
 'Atribuir malas intenciones':[r'hacer negocio', r'vienen a por', r'sembrar el miedo', r'culpan a', r'\bmata\b', r'saqueado', r'se están forrando|se están lucrando|forrando', r'privatiz\w+', r'echar a las familias', r'para que no miremos', r'mensaje del miedo|generar miedo|alarma[nr]?\b', r'quieren enfrentar', r'blindar los intereses'],
}
out={c:collections.Counter() for c in C}; ej=collections.defaultdict(list)
for c in C:
    t=tx[c]; n=len(t.split())
    for cat,pats in D.items():
        for p in pats:
            for m in re.finditer(p,t,re.I):
                out[c][cat]+=1
                ej[(c,cat)].append(t[max(0,m.start()-70):m.end()+50].replace('\n',' '))
for c in C:
    n=len(tx[c].split()); tot=sum(out[c].values())
    print(c,dict(out[c]),'total',tot,'por1000',round(tot/n*1000,2))
json.dump({f'{k[0]}|{k[1]}':v for k,v in ej.items()},open('kwic.json','w'),ensure_ascii=False,indent=0)
