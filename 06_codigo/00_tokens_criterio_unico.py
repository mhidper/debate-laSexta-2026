"""Criterio único de tokenización para todo el análisis (versión 2, 16-11-2026).
- Se eliminan las marcas de transcripción entre corchetes ([…], [de personas], [atribución probable]...)
  y las acotaciones en cursiva entre paréntesis.
- Una palabra es una secuencia de letras (con tildes, ñ, ü) o un número; los números con separadores
  de miles o decimales (50.000, 3,2) cuentan como una sola palabra y el símbolo % no cuenta.
- Los signos de puntuación aislados, guiones, comillas y puntos suspensivos no cuentan.
"""
import re, json
TOK = re.compile(r"\d+(?:[.,]\d+)*|[a-záéíóúñüà-ÿ]+(?:[-'][a-záéíóúñü]+)*", re.I)
def limpiar(t):
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = re.sub(r"\*\(.*?\)\*", " ", t)
    return t
def tokens(t):
    return TOK.findall(limpiar(t))
def n_palabras(t):
    return len(tokens(t))
