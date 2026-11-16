import json,re,sys
sys.path.insert(0,'/home/claude/v2'); sys.path.insert(0,'/home/claude/lex')
src=open('/home/claude/lex/incivilidad.py').read().split('out={c')[0].split('tx=json.load')[0]
exec(src)  # imports
exec('D='+open('/home/claude/lex/incivilidad.py').read().split('D=',1)[1].split('\nout=')[0])
iv=json.load(open('/home/claude/v2/intervenciones.json'))
def oraciones(t): return [o for o in re.split(r'(?<=[.!?…])\s+',t) if o.strip()]
hits=[]
for i,(s,t) in enumerate(iv):
    for j,o in enumerate(oraciones(t)):
        for cat,pats in D.items():
            for p in pats:
                for m in re.finditer(p,o,re.I):
                    hits.append(dict(cand=s,interv=i,orac=j,cat=cat,patron=p,match=m.group(),oracion=o))
json.dump(hits,open('/home/claude/v2/incivilidad_hits_brutos.json','w'),ensure_ascii=False,indent=0)
