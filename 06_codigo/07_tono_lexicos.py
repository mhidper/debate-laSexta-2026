import json, re, collections, math, xml.etree.ElementTree as ET, csv
import simplemma

tx = json.load(open('/home/claude/hilo/textos.json'))
C = ['Carlos Cuerpo', 'Juan Bravo', 'José María Figaredo', 'Pablo Bustinduy']

# --- léxicos ---
senti = {}
root = ET.parse('senticon.es.xml').getroot()
for layer in root:
    lvl = int(layer.get('level'))
    for pol in layer:
        for lm in pol:
            w = lm.text.strip().replace('_', ' ')
            if ' ' in w: continue
            if w not in senti:  # capa más baja (más fiable) primero
                senti[w] = (float(lm.get('pol')), lvl)
emo = collections.defaultdict(set)
with open('emolex_es.txt') as f:
    r = csv.reader(f, delimiter='\t'); h = next(r)
    for row in r:
        es = row[-1].strip().lower()
        if ' ' in es or not es: continue
        for i, e in enumerate(h[1:-1], 1):
            if row[i] == '1': emo[e].add(es)
hurt = {}
for row in csv.DictReader(open('hurtlex_ES.tsv'), delimiter='\t'):
    if row['level'] == 'conservative' and ' ' not in row['lemma']:
        hurt[row['lemma'].lower()] = row['category']

NEG = {'no', 'nunca', 'ni', 'sin', 'tampoco', 'jamás', 'nada'}
STOP = set('el la los las un una de del al a en y o que se lo le les su sus es son ha han con por para como más pero muy ya este esta esto eso'.split())
# palabras con sentido técnico/neutro en debate económico que el léxico puntúa
IGNORAR = {'crecer', 'crecimiento', 'deuda', 'déficit', 'impuesto', 'paro', 'precio', 'coste', 'interés', 'mercado', 'demanda', 'oferta',
           'banco', 'fondo', 'cambio', 'bajar', 'subir', 'caer', 'gasto', 'presión', 'tipo', 'parte', 'vez', 'caso', 'señor', 'gobierno'}

def tokens(s):
    return re.findall(r"[a-záéíóúñü]+", s.lower())

def oraciones(s):
    return [o.strip() for o in re.split(r'(?<=[.!?])\s+', s) if len(o.split()) > 3]

import sys
MAXL=int(sys.argv[1]) if len(sys.argv)>1 else 8
res = {}
for c in C:
    toks = tokens(tx[c]); n = len(toks)
    lem = [simplemma.lemmatize(t, lang='es') for t in toks]
    pos = neg = 0; covered = 0
    for i, l in enumerate(lem):
        if l in IGNORAR or toks[i] in STOP: continue
        if l in senti:
            p, lvl = senti[l]
            if lvl > MAXL: continue
            if any(x in NEG for x in toks[max(0, i - 3):i]): p = -p
            covered += 1
            if p > 0: pos += p
            else: neg += -p
    e = {k: sum(1 for t, l in zip(toks, lem) if (t in v or l in v)) for k, v in emo.items()}
    hm = [(t, hurt.get(t) or hurt.get(l)) for t, l in zip(toks, lem) if (t in hurt or l in hurt)]
    res[c] = dict(n=n, cov=covered/n*100, pos=pos / n * 1000, neg=neg / n * 1000, tono=(pos - neg) / (pos + neg),
                  **{k: v / n * 1000 for k, v in e.items()}, hurt=len(hm) / n * 1000, hurtw=collections.Counter(t for t, _ in hm).most_common(15))
for c in C:
    r = res[c]
    print(f"{c:22s} cov={r['cov']:.1f}% n={r['n']} pos={r['pos']:.1f} neg={r['neg']:.1f} tono={r['tono']:+.3f} ira={r['anger']:.1f} miedo={r['fear']:.1f} asco={r['disgust']:.1f} confianza={r['trust']:.1f} alegría={r['joy']:.1f} hurt={r['hurt']:.1f}")
    print('   hurt:', r['hurtw'])
json.dump(res, open(f'res_lex_{MAXL}.json', 'w'), ensure_ascii=False, indent=1)
