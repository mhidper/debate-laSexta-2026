"""Incivilidad v2: diccionario -> exclusiones manuales -> deduplicación -> recuento por 1.000 palabras.
Regla de deduplicación (mecánica y reproducible):
  (a) varias coincidencias en la misma oración cuentan una vez;
  (b) el mismo patrón repetido dentro de la misma intervención cuenta una vez.
Las coincidencias unidas por (a) o (b) forman un único 'evento'; su categoría es la de la primera coincidencia."""
import json, csv, collections, sys
sys.path.insert(0, '/home/claude/v2')
from tokens import n_palabras
H = json.load(open('/home/claude/v2/incivilidad_hits_brutos.json'))
iv = json.load(open('/home/claude/v2/intervenciones.json'))
EXCL = {  # (candidato, intervención, coincidencia) -> motivo
 ('Pablo Bustinduy',11,'hacer negocio'):'dirigido a terceros ausentes (empresas extranjeras)',
 ('Pablo Bustinduy',52,'se están forrando'):'dirigido a terceros ausentes (fondos, grandes propietarios)',
 ('Pablo Bustinduy',60,'echar a las familias'):'dirigido a terceros ausentes (fondos buitre)',
 ('Pablo Bustinduy',101,'se están lucrando'):'dirigido a terceros ausentes (especuladores); la oración cuenta por «blindar los intereses»',
 ('Pablo Bustinduy',207,'se están forrando'):'dirigido a terceros ausentes (grandes empresas)',
 ('Pablo Bustinduy',207,'obscenas'):'dirigido a terceros ausentes (grandes fortunas)',
 ('Pablo Bustinduy',207,'forrando'):'dirigido a terceros ausentes',
 ('Pablo Bustinduy',232,'se están forrando'):'dirigido a terceros ausentes (rentistas)',
 ('Pablo Bustinduy',245,'hacer negocio'):'dirigido a terceros ausentes («buitres», gestoras privadas)',
 ('Juan Bravo',79,'mentira'):'falso positivo: «parece mentira» expresa sorpresa',
 ('Juan Bravo',142,'falsas'):'falso positivo: «sus dudas no son falsas»',
 ('Juan Bravo',142,'mentira'):'pregunta retórica sobre su propio documento, no acusa de mentir',
 ('José María Figaredo',89,'casta'):'falso positivo: «casta de inalquilables» describe a inquilinos, no a un rival',
 ('José María Figaredo',133,'privatizar'):'cita lo que dicen otros de Vox, no lo atribuye él',
 ('Moderadora',None,None):'moderadora',
}
def excl(h):
    if h['cand'] == 'Moderadora': return 'moderadora'
    return EXCL.get((h['cand'], h['interv'], h['match']))
par = list(range(len(H)))
def f(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
inc = [i for i, h in enumerate(H) if not excl(h)]
seen = {}
for i in inc:
    h = H[i]
    for key in [('o', h['interv'], h['orac']), ('p', h['interv'], h['patron'])]:
        if key in seen: par[f(i)] = f(seen[key])
        else: seen[key] = i
ev = collections.OrderedDict()
for i in inc: ev.setdefault(f(i), []).append(i)
# id de evento legible
eid = {}
for k, (r, mem) in enumerate(sorted(ev.items(), key=lambda x: (H[x[0]]['interv'], H[x[0]]['orac'])), 1):
    for m in mem: eid[m] = k
with open('/home/claude/v2/incivilidad_coincidencias_brutas.csv', 'w', newline='', encoding='utf-8-sig') as fo:
    w = csv.writer(fo); w.writerow(['candidato', 'intervencion', 'oracion', 'categoria_diccionario', 'coincidencia', 'incluida', 'motivo_exclusion_o_fusion', 'evento', 'texto_oracion'])
    for i, h in enumerate(H):
        m = excl(h)
        if m: inc_, mot, e = 'no', m, ''
        else:
            e = eid[i]; first = min(ev[f(i)], key=lambda x: (H[x]['interv'], H[x]['orac'], x))
            inc_ = 'sí' if i == first else 'duplicado'
            mot = '' if i == first else 'misma oración o mismo patrón en la misma intervención que la coincidencia principal del evento'
        w.writerow([h['cand'], h['interv'], h['orac'], h['cat'], h['match'], inc_, mot, e, h['oracion']])
C = ['Carlos Cuerpo', 'Juan Bravo', 'José María Figaredo', 'Pablo Bustinduy']
CATS = ['Acusar de mentir', 'Descalificación personal', 'Desprecio del discurso', 'Atribuir malas intenciones']
cnt = {c: collections.Counter() for c in C}; rows = []
for r, mem in ev.items():
    first = min(mem, key=lambda x: (H[x]['interv'], H[x]['orac'], x)); h = H[first]
    cnt[h['cand']][h['cat']] += 1
    rows.append([eid[first], h['cand'], h['cat'], h['interv'], ' / '.join(sorted({H[m]['match'] for m in mem})), len(mem), h['oracion']])
rows.sort()
with open('/home/claude/v2/incivilidad_eventos_depurados.csv', 'w', newline='', encoding='utf-8-sig') as fo:
    w = csv.writer(fo); w.writerow(['evento', 'candidato', 'categoria', 'intervencion', 'expresiones_detectadas', 'coincidencias_fusionadas', 'oracion'])
    w.writerows(rows)
res = {}
for c in C:
    n = n_palabras(' '.join(x for s, x in iv if s == c)); t = sum(cnt[c].values())
    res[c] = dict(cats=[cnt[c][k] for k in CATS], total=t, palabras=n, por1000=t / n * 1000)
    print(c, res[c])
json.dump(res, open('/home/claude/v2/incivilidad_resumen.json', 'w'), ensure_ascii=False, indent=1)
