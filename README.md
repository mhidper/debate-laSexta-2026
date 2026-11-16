# Análisis del primer debate a cuatro de laSexta (13 de noviembre de 2026)

**Nota metodológica (PDF):** [02_informe/nota_metodologica_debate_laSexta.pdf](02_informe/nota_metodologica_debate_laSexta.pdf) · **Informe completo:** [02_informe/informe_datos_y_promesas_debate_laSexta.md](02_informe/informe_datos_y_promesas_debate_laSexta.md)

Cuerpo (PSOE), Bravo (PP), Figaredo (Vox) y Bustinduy (Frente Amplio), moderados por Ana Pastor. Material elaborado el 15 de noviembre de 2026 y revisado el 16 de noviembre (ver «Revisión metodológica» al final).

## Contenido

| Carpeta | Qué contiene |
| --- | --- |
| `01_transcripcion/` | Debate reconstruido intervención a intervención (`.md`), el texto agregado de cada participante y la lista de las 287 intervenciones en orden (`.json`). |
| `02_informe/` | Informe completo «Datos y promesas en el primer debate a cuatro de laSexta», en Markdown y Word, y la nota metodológica en PDF para adjuntar al hilo. |
| `03_hilo_X/` | Hilo de 22 tuits listo para publicar, con la imagen que acompaña a cada uno. |
| `04_graficos/` | Los 12 gráficos en PNG (1600 × 900 o similar), más `12b`, la versión del gráfico de evidencia en números absolutos. |
| `05_datos_csv/graficos/` | Un CSV con los datos de cada gráfico, más datos complementarios (palabras distintivas, contextos de incivilidad, menciones curiosas, legibilidad). |
| `05_datos_csv/tablas_del_informe/` | Todas las tablas del informe en CSV (verificaciones, concreción, evidencia, etc.), con las fuentes enlazadas. |
| `06_codigo/` | Scripts de Python usados para los recuentos y los gráficos. |

Los CSV están en UTF-8 con BOM para que Excel muestre bien los acentos.

## Correspondencia gráfico ↔ datos

| Gráfico | CSV |
| --- | --- |
| 01 Tiempo y cifras | `graficos/01_tiempo_y_cifras.csv` |
| 02 Verificaciones | `graficos/02_verificaciones.csv` (detalle en `tablas_del_informe/02` y `03`) |
| 03 Concreción | `graficos/03_concrecion_resumen.csv` (medias por naturaleza) y `03b_concrecion_medidas_con_naturaleza.csv` (las 28 medidas) |
| 04 Alusiones | `graficos/04_alusiones_matriz.csv` |
| 05 Tres medidas | `graficos/05_tres_medidas.csv` |
| 06 Preguntas sin respuesta | `graficos/06_preguntas_sin_respuesta.csv` (detalle en `tablas_del_informe/13`) |
| 07 Palabras distintivas | `graficos/07_palabras_distintivas_logodds.csv` |
| 08 Tono | `graficos/08_tono_sentimiento.csv` |
| 09 Incivilidad | `graficos/09_incivilidad.csv` (resumen), `09b_incivilidad_coincidencias_brutas.csv` (todas las coincidencias del diccionario, con motivo de exclusión o fusión) y `09c_incivilidad_eventos_depurados.csv` (los 42 eventos contados) |
| 10 Agenda de crecimiento | `graficos/10_agenda_crecimiento.csv` |
| 11 Repetición | `graficos/11_repeticion_diversidad.csv` |
| 12 Evidencia | `graficos/12_evidencia_balance.csv`, con recuentos y porcentajes (medida a medida en `tablas_del_informe/08` a `12`) |
| Viabilidad (tabla) | `tablas_del_informe/06_viabilidad_y_coherencia_interna.csv` y `graficos/15_viabilidad_datos_contexto.csv` |

## Método, en breve

- **Herramientas de inteligencia artificial.** Buena parte del análisis se ha apoyado en Claude Code (Anthropic) y Gemini (Google): transcripción y atribución de turnos, programación de recuentos, índices y gráficos, búsqueda y contraste de fuentes y borradores de los textos. Los criterios, las valoraciones y la revisión final son responsabilidad del autor.

- **Transcripción.** Seis transcripciones automáticas del cuaderno de NotebookLM, sin indicación de hablante. La atribución de turnos se reconstruyó por contenido y alusiones, cotejada con 17 clips de laSexta. Nueve réplicas breves tienen atribución solo probable.
- **Verificación.** Newtral (directo del 13-11-2026) más diez cifras comprobadas con fuentes públicas.
- **Tono.** Léxico ML-SentiCon (Cruz, Troyano, Pontes y Ortega, 2014), lematización con simplemma y negación simple; dos versiones (capas revisadas 1-4 y léxico completo).
- **Palabras.** Criterio único para todas las tasas (`06_codigo/00_tokens_criterio_unico.py`): palabras y números pronunciados, sin puntuación aislada ni marcas de transcripción entre corchetes. Cuerpo 4.302, Bravo 4.546, Figaredo 3.579, Bustinduy 4.217.
- **Incivilidad.** Categorías de Coe, Kenski y Rains (2014). Diccionario, revisión manual de cada caso en contexto y deduplicación: varias coincidencias en una misma oración cuentan una vez, y la misma expresión repetida en una misma intervención también.
- **Palabras distintivas.** Log-odds con prior informativo (Monroe, Colaresi y Quinn, 2008).
- **Diversidad léxica.** MATTR, MTLD y HD-D con el paquete `lexicalrichness`; intervalo de confianza por bootstrap sobre tramos de 100 palabras.
- **Legibilidad.** Índice INFLESZ (Szigriszt-Pazos).
- **Concreción.** Cada medida lleva además su naturaleza: en vigor (BOE), instrumento nuevo o meta de resultado.
- **Evidencia económica.** 20 propuestas y diagnósticos (26 valoraciones, porque las compartidas cuentan para cada partido) valorados con la literatura empírica. El gráfico 12 está normalizado al 100 % de las medidas de cada partido.

## Para reproducir

Python 3 con `matplotlib`, `numpy`, `wordcloud`, `simplemma`, `lexicalrichness` y la fuente Inter. Los scripts usan rutas absolutas del entorno de trabajo original: ajústalas a tu carpeta. Los léxicos no se incluyen por sus licencias; se descargan de sus fuentes originales:

- ML-SentiCon: https://core.ac.uk/download/333939468.pdf (artículo de referencia)
- NRC EmoLex en español (probado y descartado por su ruido): Mohammad y Turney, NRC Canada
- Hurtlex ES (probado y descartado): https://github.com/valeriobasile/hurtlex

## Limitaciones

Un único debate de unas 17.000 palabras de los candidatos. Las valoraciones de concreción, incivilidad y evidencia son de elaboración propia y otro analista podría clasificar algún caso de forma distinta. Newtral elige qué verifica, así que sus recuentos no son una muestra aleatoria.

## Revisión metodológica (16 de noviembre de 2026)

| Cambio | Antes | Después |
| --- | --- | --- |
| Denominador de palabras | Dos criterios (división por espacios en participación e incivilidad, tokenizador de `lexicalrichness` en diversidad) | Un solo criterio en todo el material |
| Cifras por 1.000 palabras | Cuerpo 6,7, Bravo 9,8, Figaredo 6,1, Bustinduy 9,4 | 6,7, 9,9, 6,1, 9,5 |
| Incivilidad (total y por 1.000 palabras) | Cuerpo 5 (1,2), Bravo 14 (3,1), Figaredo 11 (3,1), Bustinduy 17 (4,0) | 5 (1,2), 12 (2,6), 10 (2,8), 15 (3,6) |
| Diversidad léxica (MATTR 100) | 0,651 / 0,672 / 0,641 / 0,648 | 0,658 / 0,679 / 0,645 / 0,653 (mismo orden en las conclusiones) |
| Concreción | Medias por partido | Medias por partido y por naturaleza de la medida. El PSOE puntúa 2,6 en lo que está en vigor y 2,5 en lo nuevo, de modo que su ventaja no se explica por el BOE |
| Evidencia | Gráfico en números absolutos | Gráfico al 100 % con n por partido (el absoluto se conserva como `12b`) |
| Viabilidad | No existía | Nueva tabla tras el cuadre fiscal: cuellos de botella físicos, paradoja del impuesto pigouviano y fricción competencial |
| Dato del CIS de Bravo (clase baja/pobre) | «No comparable», siguiendo a Newtral | «Correcta, con matices». La pregunta y la agrupación son las mismas en diciembre de 2019 (3,0 %) y octubre de 2026 (20,6 %). Newtral queda en 11 correctas, 11 con contexto, 2 sin corroborar y 1 falsa. Corrección por aviso de Fernando Sols |

Sobre la deduplicación de incivilidad: el recuento anterior ya había pasado por una revisión manual, así que no arrastraba todas las filas repetidas del fichero de contextos (que se deben al solapamiento de la ventana de texto alrededor de cada coincidencia). La lista manual anterior no se guardó, de modo que la comparación se ha reconstruido: con la regla nueva, Bravo baja dos (la repetición de «para generar miedo» y la de «Sánchez es reincidente» en la misma intervención), Figaredo uno («una casta corrupta que ha saqueado lo público» contaba en dos categorías) y Bustinduy dos («su amigo» y «su jefe, su amigo» en la misma réplica, y «privatizar» repetido en la réplica sobre pensiones). «Casta de inalquilables» (Figaredo) y «¿Es mentira esto?» (Bravo) no cuentan, porque no son ataques a un rival. Bustinduy sigue en cabeza y Cuerpo a la cola, pero el empate anterior entre Bravo y Figaredo se deshace: Figaredo queda segundo.

## Licencia

Los datos, las tablas, los gráficos y los textos se publican bajo licencia [Creative Commons Atribución 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) (CC BY 4.0): se pueden reutilizar citando la fuente. El código de `06_codigo/` se publica bajo licencia MIT. La transcripción reproduce intervenciones públicas de un debate electoral con fines informativos y de análisis.

## Cómo citar

Hidalgo, M. (2026). *Datos y promesas en el primer debate a cuatro de laSexta (13 de noviembre de 2026)*. Datos, código y nota metodológica. https://github.com/mhidper/debate-laSexta-2026.

## Errores y sugerencias

Si detecta un error en una cifra, una atribución o una clasificación, puede abrir una *issue* en este repositorio indicando el fichero y la fila.
