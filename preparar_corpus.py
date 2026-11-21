"""Descarga La metamorfosis (Kafka) desde Wikisource en español, la limpia,
la pagina en páginas de tamaño fijo y selecciona al azar 2 páginas consecutivas."""
import random
import re
import urllib.request
from pathlib import Path

CAPITULOS = ["Uno", "Dos", "Tres"]
URL = "https://es.wikisource.org/w/index.php?title=La_metamorfosis_(Kafka)/Cap%C3%ADtulo_{}&action=raw"
PALABRAS_POR_PAGINA = 300  # aproximación a una página de edición de bolsillo
SEMILLA = 2026
SALIDA = Path(__file__).parent / "corpus"


def limpiar(wikitexto: str) -> str:
    texto = re.sub(r"\{\{.*?\}\}", "", wikitexto, flags=re.S)   # plantillas
    texto = re.sub(r"\[\[(Imagen|File|Archivo):[^\]]*\]\]", "", texto)
    texto = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", texto)  # enlaces
    texto = re.sub(r"<[^>]+>", "", texto)                          # html
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    capitulos = []
    for i, nombre in enumerate(CAPITULOS, start=1):
        req = urllib.request.Request(URL.format(nombre), headers={"User-Agent": "Lab3-NLP-corpus/1.0"})
        with urllib.request.urlopen(req) as r:
            capitulos.append(f"CAPÍTULO {i}\n\n" + limpiar(r.read().decode("utf-8")))
    completo = "\n\n".join(capitulos)
    (SALIDA / "metamorfosis_completa.txt").write_text(completo, encoding="utf-8")

    palabras = completo.split()
    paginas = [" ".join(palabras[i:i + PALABRAS_POR_PAGINA])
               for i in range(0, len(palabras), PALABRAS_POR_PAGINA)]
    random.seed(SEMILLA)
    p = random.randrange(0, len(paginas) - 1)  # índice de la primera página
    seleccion = (
        f"Fuente: Franz Kafka, *La metamorfosis*, traducción al español disponible en Wikisource\n"
        f"(https://es.wikisource.org/wiki/La_metamorfosis_(Kafka)).\n"
        f"Paginación: {PALABRAS_POR_PAGINA} palabras por página -> {len(paginas)} páginas en total.\n"
        f"Semilla aleatoria: {SEMILLA}. Páginas seleccionadas: {p + 1} y {p + 2}.\n\n"
        f"--- Página {p + 1} ---\n{paginas[p]}\n\n--- Página {p + 2} ---\n{paginas[p + 1]}\n"
    )
    (SALIDA / "paginas_seleccionadas.txt").write_text(seleccion, encoding="utf-8")
    print(seleccion)


if __name__ == "__main__":
    main()
