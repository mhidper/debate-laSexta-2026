"""Diversidad léxica con el criterio único de tokens (tokens.py)."""
import json, collections, random, sys
sys.path.insert(0, '/home/claude/v2')
from tokens import tokens
from lexicalrichness import LexicalRichness
import simplemma
iv = json.load(open('/home/claude/v2/intervenciones.json'))
C = ['Carlos Cuerpo', 'Juan Bravo', 'José María Figaredo', 'Pablo Bustinduy']
def rep(tk, n):
    g = [' '.join(tk[i:i+n]) for i in range(len(tk)-n+1)]
    c = collections.Counter(g)
    return 100*sum(v for v in c.values() if v > 1)/len(g), c
def ci(tk, reps=2000, seed=1):
    ch = [tk[i:i+100] for i in range(0, len(tk)-99, 100)]
    t = [len(set(x))/100 for x in ch]; rnd = random.Random(seed); m = []
    for _ in range(reps):
        s = [rnd.choice(t) for _ in t]; m.append(sum(s)/len(s))
    m.sort(); return sum(t)/len(t), m[int(.025*reps)], m[int(.975*reps)]
out = {}
for c in C:
    tk = [w.lower() for w in tokens(' '.join(x for s, x in iv if s == c))]
    lm = [simplemma.lemmatize(w, lang='es') for w in tk]
    L = LexicalRichness(tk, preprocessor=None, tokenizer=None)
    Ll = LexicalRichness(lm, preprocessor=None, tokenizer=None)
    r3, _ = rep(tk, 3); r5, c5 = rep(tk, 5)
    m, lo, hi = ci(tk)
    out[c] = dict(n=len(tk), ttr=L.ttr, mattr100=L.mattr(100), mattr500=L.mattr(500), mtld=L.mtld(0.72), hdd=L.hdd(42),
                  mattr100_lem=Ll.mattr(100), mtld_lem=Ll.mtld(0.72), ttr100=m, ci_lo=lo, ci_hi=hi, rep3=r3, rep5=r5,
                  top5=[[k, v] for k, v in c5.most_common(10)])
    print(c, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out[c].items() if k != 'top5'})
json.dump(out, open('/home/claude/v2/diversidad.json', 'w'), ensure_ascii=False, indent=1)
