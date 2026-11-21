# Laboratorio 3 — Análisis de atención en BERT

Análisis de las matrices de atención de `bert-base-multilingual-cased` sobre oraciones complejas extraídas de *La metamorfosis* de Franz Kafka. Se inspecciona cómo distintas capas y cabezas distribuyen la atención entre tokens, y se discuten los límites de interpretar la atención como explicación.

## Estructura

| Ruta | Contenido |
|---|---|
| `Lab3_Atencion_BERT.ipynb` | Notebook ejecutado: tokenización, ejecución del modelo, análisis de atención, comparación y respuestas a las preguntas de análisis. |
| `preparar_corpus.py` | Descarga el texto (Wikisource, español), lo limpia, lo pagina (300 palabras/página) y elige al azar 2 páginas consecutivas (semilla 2026). |
| `corpus/paginas_seleccionadas.txt` | Corpus del laboratorio: páginas 16 y 17 (de 69). |
| `corpus/metamorfosis_completa.txt` | Texto completo limpio usado para la paginación. |
| `resultados/*.csv` | Tablas de tokens, formas de las matrices, perfil de cabezas, top-5 de atención, contrastes de contexto, simples vs. complejas y subpalabras. |
| `resultados/figuras/*.png` | Heatmaps de atención, perfil de las 144 cabezas, atención a referentes, contrastes *hoja*/*banco*, similitud de representaciones y subpalabras. |

## Oraciones analizadas

* **Complejas (corpus):** C1–C4, con coordinación larga, relativas y pronombres con antecedente.
* **Simples (corpus):** S1 “Entre tanto el día había aclarado.”, S2 “Todavía caía la lluvia.”
* **Contraste de contexto:** *hoja* (de la puerta / de un árbol) y *banco* (entidad financiera / asiento).

## Selección de capas y cabezas

Capas 3, 7 y 11; en cada una, una cabeza **posicional** (mayor atención al token vecino) y una **contextual** (mayor entropía con poca atención a tokens especiales). Como complemento, la capa 9, cabeza 3, que concentra la atención hacia los referentes de pronombres.

## Reproducción

```bash
pip install transformers torch pandas matplotlib seaborn
python preparar_corpus.py          # opcional: regenera el corpus
jupyter nbconvert --to notebook --execute --inplace Lab3_Atencion_BERT.ipynb
```

El notebook se ejecuta en CPU en pocos minutos (descarga ~700 MB del modelo la primera vez).
