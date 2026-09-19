#!/usr/bin/env python3
"""
Gera sitemap.xml descobrindo sozinho todas as paginas publicadas no dominio
{usuario}.github.io, varrendo TODOS os repositorios do usuario que tenham
GitHub Pages habilitado.

Nada aqui e fixo: o usuario sai do ambiente do Actions, a lista de repos sai
da API do GitHub e cada URL so entra no sitemap depois de responder 200 de
verdade. Repositorio novo, pagina nova ou pagina removida sao refletidos na
proxima execucao, sem ninguem editar arquivo nenhum.

Como funciona:
  1. lista os repositorios publicos do usuario com has_pages = true
  2. em cada um, procura os .html no branch de publicacao provavel
  3. converte cada caminho em URL candidata
  4. testa a URL por HTTP; so entra quem devolver 200
  5. pega o lastmod do ultimo commit que tocou o arquivo
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

# ---------------------------------------------------------------------------
# Ajustes (mudar so se quiser alterar o comportamento; nada aqui e obrigatorio)
# ---------------------------------------------------------------------------

# Quando uma pasta tem index.html, publica so a URL da pasta e omite os
# outros .html irmaos. Evita que uma pasta com dezenas de transcricoes
# despeje dezenas de URLs soltas no sitemap.
SOMENTE_INDICE_POR_PASTA = True

IGNORAR_FORKS = True
IGNORAR_ARQUIVADOS = True

# Pastas que nunca contem pagina publicavel
PASTAS_IGNORADAS = {".git", ".github", "node_modules", "_site", "vendor"}

# Arquivos que existem mas nao sao pagina de verdade
ARQUIVOS_IGNORADOS = {"404.html"}
PREFIXOS_IGNORADOS = ("google", "BingSiteAuth", "yandex")

# Branches onde o Pages costuma publicar, alem do branch padrao do repo
BRANCHES_EXTRAS = ("gh-pages",)

# Pastas que o Pages pode usar como raiz do site
RAIZES_POSSIVEIS = ("", "docs/")

TIMEOUT = 20
THREADS = 8

# ---------------------------------------------------------------------------

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

repo_atual = os.environ.get("GITHUB_REPOSITORY", "")
if not repo_atual:
    sys.exit("GITHUB_REPOSITORY nao definido. Este script roda dentro do Actions.")

USUARIO = repo_atual.split("/")[0]
REPO_DO_SITE = f"{USUARIO.lower()}.github.io"
DOMINIO = f"https://{REPO_DO_SITE}"


@dataclass
class Pagina:
    url: str
    repo: str
    caminho: str
    branch: str
    lastmod: str = ""


def api(rota: str, autenticado: bool = True):
    """GET na API do GitHub. Devolve None em 404/403 em vez de explodir."""
    pedido = urllib.request.Request(f"{API}{rota}")
    pedido.add_header("Accept", "application/vnd.github+json")
    pedido.add_header("User-Agent", "gerador-de-sitemap")
    if autenticado and TOKEN:
        pedido.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(pedido, timeout=TIMEOUT) as resposta:
            return json.loads(resposta.read())
    except urllib.error.HTTPError as erro:
        # Token do Actions as vezes nao alcanca repo de fora; tenta anonimo
        if erro.code in (401, 403) and autenticado:
            return api(rota, autenticado=False)
        return None
    except Exception:
        return None


def listar_repositorios() -> list[dict]:
    repos, pagina = [], 1
    while True:
        lote = api(f"/users/{USUARIO}/repos?per_page=100&page={pagina}&type=owner")
        if not lote:
            break
        repos.extend(lote)
        if len(lote) < 100:
            break
        pagina += 1

    selecionados = []
    for repo in repos:
        if not repo.get("has_pages"):
            continue
        if IGNORAR_FORKS and repo.get("fork"):
            continue
        if IGNORAR_ARQUIVADOS and repo.get("archived"):
            continue
        selecionados.append(repo)
    return selecionados


def listar_htmls(repo: str, branch: str) -> list[str]:
    arvore = api(f"/repos/{USUARIO}/{repo}/git/trees/{branch}?recursive=1")
    if not arvore or "tree" not in arvore:
        return []

    encontrados = []
    for item in arvore["tree"]:
        if item.get("type") != "blob":
            continue
        caminho = item["path"]
        if not caminho.endswith(".html"):
            continue
        partes = Path(caminho).parts
        if any(parte in PASTAS_IGNORADAS for parte in partes):
            continue
        nome = partes[-1]
        if nome in ARQUIVOS_IGNORADOS or nome.startswith(PREFIXOS_IGNORADOS):
            continue
        encontrados.append(caminho)
    return encontrados


def montar_url(repo: str, caminho: str) -> list[str]:
    """Todas as URLs plausiveis para um arquivo. A validacao HTTP decide."""
    if repo.lower() == REPO_DO_SITE:
        base = DOMINIO
    else:
        base = f"{DOMINIO}/{repo}"

    candidatas = []
    for raiz in RAIZES_POSSIVEIS:
        if raiz and not caminho.startswith(raiz):
            continue
        relativo = caminho[len(raiz):]
        if not relativo:
            continue
        if relativo.endswith("/index.html"):
            candidatas.append(f"{base}/{relativo[: -len('index.html')]}")
        elif relativo == "index.html":
            candidatas.append(f"{base}/")
        else:
            candidatas.append(f"{base}/{relativo}")
    return candidatas


def esta_no_ar(url: str) -> bool:
    pedido = urllib.request.Request(url, method="HEAD")
    pedido.add_header("User-Agent", "gerador-de-sitemap")
    try:
        with urllib.request.urlopen(pedido, timeout=TIMEOUT) as resposta:
            return resposta.status == 200
    except Exception:
        return False


def buscar_lastmod(pagina: Pagina) -> str:
    rota = (
        f"/repos/{USUARIO}/{pagina.repo}/commits"
        f"?path={urllib.parse.quote(pagina.caminho)}&sha={pagina.branch}&per_page=1"
    )
    dados = api(rota)
    if isinstance(dados, list) and dados:
        return dados[0]["commit"]["committer"]["date"][:10]
    return ""


def filtrar_por_indice(paginas: list[Pagina]) -> list[Pagina]:
    """Se a pasta tem index.html, mantem so ela."""
    pastas_com_indice = {
        pagina.url for pagina in paginas if pagina.url.endswith("/")
    }
    resultado = []
    for pagina in paginas:
        if pagina.url.endswith("/"):
            resultado.append(pagina)
            continue
        pasta = pagina.url.rsplit("/", 1)[0] + "/"
        if pasta in pastas_com_indice:
            continue
        resultado.append(pagina)
    return resultado


def prioridade(url: str) -> str:
    if url == f"{DOMINIO}/":
        return "1.0"
    profundidade = url[len(DOMINIO) + 1:].strip("/").count("/")
    return "0.8" if profundidade == 0 else "0.6"


def main() -> None:
    repositorios = listar_repositorios()
    print(f"Repositorios com Pages: {len(repositorios)}")

    candidatas: dict[str, Pagina] = {}

    for repo in repositorios:
        nome = repo["name"]
        branches = [repo.get("default_branch", "main"), *BRANCHES_EXTRAS]
        vistos = set()
        for branch in branches:
            if branch in vistos:
                continue
            vistos.add(branch)
            for caminho in listar_htmls(nome, branch):
                for url in montar_url(nome, caminho):
                    candidatas.setdefault(
                        url, Pagina(url=url, repo=nome, caminho=caminho, branch=branch)
                    )
        print(f"  {nome}: {len(candidatas)} candidata(s) acumulada(s)")

    print(f"\nValidando {len(candidatas)} URL(s) por HTTP...")
    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        vivas = list(pool.map(esta_no_ar, candidatas))

    paginas = [p for p, viva in zip(candidatas.values(), vivas) if viva]
    print(f"{len(paginas)} URL(s) responderam 200.")

    if SOMENTE_INDICE_POR_PASTA:
        antes = len(paginas)
        paginas = filtrar_por_indice(paginas)
        if antes != len(paginas):
            print(f"{antes - len(paginas)} pagina(s) omitida(s): a pasta tem indice.")

    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        for pagina, data in zip(paginas, pool.map(buscar_lastmod, paginas)):
            pagina.lastmod = data

    paginas.sort(key=lambda p: (p.url != f"{DOMINIO}/", p.url))

    linhas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for pagina in paginas:
        linhas.append("  <url>")
        linhas.append(f"    <loc>{escape(pagina.url)}</loc>")
        if pagina.lastmod:
            linhas.append(f"    <lastmod>{pagina.lastmod}</lastmod>")
        linhas.append("    <changefreq>monthly</changefreq>")
        linhas.append(f"    <priority>{prioridade(pagina.url)}</priority>")
        linhas.append("  </url>")
    linhas.append("</urlset>")

    if not paginas:
        sys.exit("Nenhuma pagina encontrada. Sitemap nao foi sobrescrito.")

    Path("sitemap.xml").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    print(f"\nSitemap com {len(paginas)} URL(s):")
    for pagina in paginas:
        print(f"  {pagina.url}  ({pagina.repo})")


if __name__ == "__main__":
    main()
