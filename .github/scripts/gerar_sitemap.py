#!/usr/bin/env python3
"""
Gera sitemap.xml varrendo os arquivos .html publicados do site.

Regras de URL:
    index.html                 ->  /
    projeto-cvm/index.html     ->  /projeto-cvm/
    sobre.html                 ->  /sobre.html

O lastmod de cada URL vem da data do ultimo commit que tocou o arquivo,
entao nao precisa ser mantido a mao.
"""

import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

BASE = "https://1pedroosilva.github.io"
RAIZ = Path(".")

# Pastas que nunca entram no sitemap
PASTAS_IGNORADAS = {".git", ".github", "node_modules", "_site", "assets"}

# Arquivos especificos que nao sao paginas de verdade
ARQUIVOS_IGNORADOS = {"404.html"}

# Prefixos de arquivo que sao verificacao de propriedade (Google, Bing, etc.)
PREFIXOS_IGNORADOS = ("google", "BingSiteAuth")


def eh_pagina(caminho: Path) -> bool:
    if any(parte in PASTAS_IGNORADAS for parte in caminho.parts):
        return False
    if caminho.name in ARQUIVOS_IGNORADOS:
        return False
    if caminho.name.startswith(PREFIXOS_IGNORADOS):
        return False
    return True


def para_url(caminho: Path) -> str:
    if caminho.name == "index.html":
        pasta = caminho.parent.as_posix()
        return f"{BASE}/" if pasta == "." else f"{BASE}/{pasta}/"
    return f"{BASE}/{caminho.as_posix()}"


def ultima_modificacao(caminho: Path) -> str:
    """Data (YYYY-MM-DD) do ultimo commit que tocou o arquivo."""
    resultado = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(caminho)],
        capture_output=True,
        text=True,
        check=False,
    )
    return resultado.stdout.strip() or ""


def prioridade(url: str) -> str:
    return "1.0" if url == f"{BASE}/" else "0.8"


def main() -> None:
    paginas = sorted(p for p in RAIZ.rglob("*.html") if eh_pagina(p))

    linhas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    # A home primeiro, o resto em ordem alfabetica
    paginas.sort(key=lambda p: (para_url(p) != f"{BASE}/", para_url(p)))

    for pagina in paginas:
        url = para_url(pagina)
        linhas.append("  <url>")
        linhas.append(f"    <loc>{escape(url)}</loc>")

        data = ultima_modificacao(pagina)
        if data:
            linhas.append(f"    <lastmod>{data}</lastmod>")

        linhas.append("    <changefreq>monthly</changefreq>")
        linhas.append(f"    <priority>{prioridade(url)}</priority>")
        linhas.append("  </url>")

    linhas.append("</urlset>")

    Path("sitemap.xml").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    print(f"{len(paginas)} pagina(s) no sitemap:")
    for pagina in paginas:
        print(f"  - {para_url(pagina)}")


if __name__ == "__main__":
    main()
