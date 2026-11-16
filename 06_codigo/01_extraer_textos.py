import re,json
t=open('/home/claude/debate_laSexta_intervenciones.md').read().split('## Parte I ·',1)[1]
pat=re.compile(r'^\*\*(Moderadora|Carlos Cuerpo|Juan Bravo|José María Figaredo|Pablo Bustinduy)(?::\*\*|\*\*)(?:\s*\*\[[^\]]*\]\*)?:?\s*(.*)$',re.S)
cur=None;tx={}
for p in t.split('\n\n'):
    p=p.strip()
    if not p or p.startswith('#') or p.startswith('*['):continue
    m=pat.match(p)
    if m: cur=m.group(1);x=m.group(2)
    else: x=p
    x=re.sub(r'\*\(.*?\)\*','',x)
    tx[cur]=tx.get(cur,'')+' '+x
json.dump(tx,open('/home/claude/hilo/textos.json','w'),ensure_ascii=False)
print({k:len(v.split()) for k,v in tx.items()})
