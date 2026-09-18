#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditor_wcag.py - Auditor automático de acessibilidade web (WCAG 2.1 / eMAG 3.1).

Verifica, no código-fonte HTML das páginas informadas, os itens do checklist de
15 pontos que podem ser conferidos de forma automatizada, e grava as ocorrencias
em dados/resultados_automaticos.json.

Uso:
    python3 ferramenta/auditor_wcag.py https://exemplo.gov.br
    python3 ferramenta/auditor_wcag.py https://exemplo.gov.br/a https://exemplo.gov.br/b
    python3 ferramenta/auditor_wcag.py --arquivo pagina_salva.html --url https://exemplo.gov.br

Não requer bibliotecas externas (apenas a biblioteca padrão do Python 3.8+).
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
from collections import Counter
from html.parser import HTMLParser

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "dados", "resultados_automaticos.json")

TEXTO_GENERICO = {
    "clique aqui", "clique", "aqui", "saiba mais", "leia mais", "veja mais",
    "mais", "link", "acesse", "acesse aqui", "continuar", "continue lendo",
    "detalhes", "ver", "ver mais", "baixar", "download", "click here",
    "read more", "more", "learn more",
}
ALT_SUSPEITO = re.compile(
    r"^(imagem|image|img|foto|photo|picture|figura|logo|logotipo|banner|ícone|icon|spacer|"
    r"[\w\-\s]+\.(jpg|jpeg|png|gif|svg|webp))$", re.I
)
TEXTO_SALTO = re.compile(r"(pular|saltar|ir para|ir ao|skip)\s*(para|ao|to)?\s*"
                         r"(o\s+|the\s+)?(conteúdo|conte[uú]do|content|main|principal|menu|busca)", re.I)
CONTROLES = {"input", "select", "textarea"}
INPUT_SEM_ROTULO = {"hidden", "submit", "reset", "button", "image"}
LANDMARKS = {"header", "nav", "main", "footer", "aside"}


class Analisador(HTMLParser):
    """Percorre o HTML coletando os elementos relevantes para a auditoria."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titulo = None
        self._em_titulo = False
        self.viewport = None
        self.imagens = []
        self.cabecalhos = []
        self._cab_atual = None
        self.links = []
        self._link_atual = None
        self.botoes = []
        self._botao_atual = None
        self.controles = []
        self.rotulos_for = set()
        self.ids = []
        self.landmarks = Counter()
        self.papeis = Counter()
        self.divs_clicaveis = []
        self.iframes_sem_titulo = 0
        self.iframes = 0
        self.tabelas = 0
        self.tabelas_sem_th = 0
        self._tabela_tem_th = None
        self._pilha_tabela = []
        self.eventos_inline = 0
        self._label_aberto = None

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _d(attrs):
        return {k.lower(): (v if v is not None else "") for k, v in attrs}

    def _acumula_texto(self, dado):
        if self._em_titulo:
            self.titulo = (self.titulo or "") + dado
        if self._cab_atual is not None:
            self._cab_atual["texto"] += dado
        if self._link_atual is not None:
            self._link_atual["texto"] += dado
        if self._botao_atual is not None:
            self._botao_atual["texto"] += dado
        if self._label_aberto is not None:
            self._label_aberto["texto"] += dado

    # ------------------------------------------------------------------ tags
    def handle_starttag(self, tag, attrs):
        a = self._d(attrs)
        tag = tag.lower()

        if any(k.startswith("on") for k in a):
            self.eventos_inline += 1
        if a.get("id"):
            self.ids.append(a["id"])
        if a.get("role"):
            self.papeis[a["role"].strip().lower()] += 1
        if tag in LANDMARKS:
            self.landmarks[tag] += 1

        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title" and self.titulo is None:
            self._em_titulo = True
            self.titulo = ""
        elif tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = a.get("content", "")
        elif tag == "img":
            self.imagens.append({
                "src": a.get("src", "")[:120],
                "tem_alt": "alt" in a,
                "alt": a.get("alt", ""),
                "role": a.get("role", ""),
                "aria_hidden": a.get("aria-hidden", ""),
            })
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._cab_atual = {"nivel": int(tag[1]), "texto": ""}
        elif tag == "a":
            self._link_atual = {
                "href": a.get("href", ""),
                "texto": "",
                "aria_label": a.get("aria-label", "") or a.get("title", ""),
                "tem_img_com_alt": False,
                "posicao": len(self.links),
            }
        elif tag == "button":
            self._botao_atual = {"texto": "", "aria_label": a.get("aria-label", "") or a.get("title", "")}
        elif tag == "label":
            self._label_aberto = {"texto": "", "for": a.get("for", "")}
            if a.get("for"):
                self.rotulos_for.add(a["for"])
        elif tag in CONTROLES:
            tipo = a.get("type", "text").lower() if tag == "input" else tag
            if not (tag == "input" and tipo in INPUT_SEM_ROTULO):
                self.controles.append({
                    "tag": tag,
                    "tipo": tipo,
                    "id": a.get("id", ""),
                    "name": a.get("name", ""),
                    "aria_label": a.get("aria-label", ""),
                    "aria_labelledby": a.get("aria-labelledby", ""),
                    "title": a.get("title", ""),
                    "placeholder": a.get("placeholder", ""),
                    "dentro_de_label": self._label_aberto is not None,
                })
        elif tag == "iframe":
            self.iframes += 1
            if not a.get("title"):
                self.iframes_sem_titulo += 1
        elif tag == "table":
            self.tabelas += 1
            self._pilha_tabela.append(False)
        elif tag == "th" and self._pilha_tabela:
            self._pilha_tabela[-1] = True
        elif tag in ("div", "span") and any(k in a for k in ("onclick", "onkeydown", "onkeypress")):
            if not a.get("role") and "tabindex" not in a:
                self.divs_clicaveis.append(a.get("class", "")[:80])

        # imagem dentro de link
        if tag == "img" and self._link_atual is not None:
            if a.get("alt", "").strip():
                self._link_atual["tem_img_com_alt"] = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._em_titulo = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._cab_atual:
            self._cab_atual["texto"] = " ".join(self._cab_atual["texto"].split())
            self.cabecalhos.append(self._cab_atual)
            self._cab_atual = None
        elif tag == "a" and self._link_atual:
            self._link_atual["texto"] = " ".join(self._link_atual["texto"].split())
            self.links.append(self._link_atual)
            self._link_atual = None
        elif tag == "button" and self._botao_atual:
            self._botao_atual["texto"] = " ".join(self._botao_atual["texto"].split())
            self.botoes.append(self._botao_atual)
            self._botao_atual = None
        elif tag == "label":
            self._label_aberto = None
        elif tag == "table" and self._pilha_tabela:
            if not self._pilha_tabela.pop():
                self.tabelas_sem_th += 1

    def handle_data(self, dado):
        self._acumula_texto(dado)


# ---------------------------------------------------------------------- regras
def _res(item, nome, status, detalhe, ocorrencias=0, exemplos=None):
    return {
        "item": item, "nome": nome, "status": status, "detalhe": detalhe,
        "ocorrencias": ocorrencias, "exemplos": (exemplos or [])[:5],
    }


def avaliar(p: Analisador, html: str):
    r = []

    # 1 - texto alternativo
    sem_alt = [i for i in p.imagens if not i["tem_alt"] and i["aria_hidden"] != "true"]
    suspeitas = [i for i in p.imagens if i["tem_alt"] and i["alt"].strip()
                 and ALT_SUSPEITO.match(i["alt"].strip())]
    total_prob = len(sem_alt) + len(suspeitas)
    r.append(_res(1, "Texto alternativo em imagens",
                  "nao_conforme" if total_prob else ("conforme" if p.imagens else "nao_aplicavel"),
                  f"{len(p.imagens)} imagens; {len(sem_alt)} sem atributo alt; "
                  f"{len(suspeitas)} com alt genérico/nome de arquivo.",
                  total_prob, [i["src"] for i in sem_alt] + [i["alt"] for i in suspeitas]))

    # 2 - hierarquia de cabecalhos
    niveis = [c["nivel"] for c in p.cabecalhos]
    h1 = niveis.count(1)
    saltos, ant = [], 0
    for n in niveis:
        if ant and n > ant + 1:
            saltos.append(f"h{ant} -> h{n}")
        ant = n
    vazios = [c for c in p.cabecalhos if not c["texto"]]
    prob2 = (h1 != 1) or bool(saltos) or bool(vazios)
    r.append(_res(2, "Hierarquia de cabeçalhos",
                  "nao_conforme" if prob2 else "conforme",
                  f"{len(p.cabecalhos)} cabeçalhos; {h1} elemento(s) h1; "
                  f"{len(saltos)} salto(s) de nível; {len(vazios)} cabeçalho(s) vazio(s).",
                  (0 if h1 == 1 else 1) + len(saltos) + len(vazios), saltos))

    # 3 - idioma
    ok3 = bool(p.lang and p.lang.strip())
    r.append(_res(3, "Idioma da página declarado",
                  "conforme" if ok3 else "nao_conforme",
                  f"Atributo lang da tag <html>: {p.lang!r}." if ok3
                  else "A tag <html> não declara o atributo lang.",
                  0 if ok3 else 1, [str(p.lang)]))

    # 4 - titulo
    t = (p.titulo or "").strip()
    ok4 = len(t) >= 5
    r.append(_res(4, "Título de página descritivo",
                  "conforme" if ok4 else "nao_conforme",
                  f"<title> = {t[:90]!r} ({len(t)} caracteres)." if t else "Página sem <title>.",
                  0 if ok4 else 1, [t[:90]]))

    # 7 - redimensionamento
    vp = (p.viewport or "").lower()
    bloqueia = "user-scalable=no" in vp.replace(" ", "") or\
               bool(re.search(r"maximum-scale\s*=\s*(1(\.0+)?|0?\.\d+)\b", vp))
    r.append(_res(7, "Redimensionamento de texto até 200%",
                  "nao_conforme" if bloqueia else "verificar_manualmente",
                  f"meta viewport = {vp[:90]!r}. " +
                  ("A página bloqueia o zoom do usuário."
                   if bloqueia else "Zoom não bloqueado no viewport; confirmar visualmente em 200%."),
                  1 if bloqueia else 0, [vp[:90]]))

    # 10 - link de salto
    salto = [l for l in p.links[:6]
             if l["href"].startswith("#") and TEXTO_SALTO.search(l["texto"] or l["aria_label"] or "")]
    r.append(_res(10, "Link para pular ao conteúdo principal",
                  "conforme" if salto else "nao_conforme",
                  f"{len(salto)} link(s) de salto entre os 6 primeiros links."
                  if salto else "Nenhum link de salto para o conteúdo foi encontrado no início da página.",
                  0 if salto else 1, [l["texto"] for l in salto]))

    # 11 - rotulos de formulario
    sem_rotulo = []
    for c in p.controles:
        tem = bool(c["aria_label"] or c["aria_labelledby"] or c["title"] or c["dentro_de_label"]
                   or (c["id"] and c["id"] in p.rotulos_for))
        if not tem:
            sem_rotulo.append(c)
    so_placeholder = [c for c in sem_rotulo if c["placeholder"]]
    r.append(_res(11, "Rótulos associados aos campos de formulário",
                  "nao_conforme" if sem_rotulo else ("conforme" if p.controles else "nao_aplicavel"),
                  f"{len(p.controles)} campos analisados; {len(sem_rotulo)} sem rótulo associado "
                  f"({len(so_placeholder)} contando apenas com placeholder).",
                  len(sem_rotulo), [f"{c['tag']}[{c['tipo']}] name={c['name']!r}" for c in sem_rotulo]))

    # 13 - links descritivos
    genericos, vazios_l = [], []
    for l in p.links:
        rot = (l["texto"] or l["aria_label"] or "").strip()
        if not rot and not l["tem_img_com_alt"]:
            vazios_l.append(l["href"][:80])
        elif rot.lower().strip(" .:!?»>") in TEXTO_GENERICO:
            genericos.append(rot)
        elif re.match(r"^https?://", rot):
            genericos.append(rot[:60])
    prob13 = len(genericos) + len(vazios_l)
    r.append(_res(13, "Links com texto descritivo",
                  "nao_conforme" if prob13 else "conforme",
                  f"{len(p.links)} links; {len(vazios_l)} sem texto acessível; "
                  f"{len(genericos)} com texto genérico ou URL crua.",
                  prob13, vazios_l + genericos))

    # 15 - estrutura semantica
    dup = [i for i, n in Counter(p.ids).items() if n > 1]
    falt = sorted(LANDMARKS - set(p.landmarks) - set(p.papeis))
    bt_sem_nome = [b for b in p.botoes if not (b["texto"] or b["aria_label"])]
    prob15 = (len(dup) + len(p.divs_clicaveis) + p.iframes_sem_titulo
              + p.tabelas_sem_th + len(bt_sem_nome) + (1 if "main" in falt else 0))
    r.append(_res(15, "Estrutura semântica e marcação válida",
                  "nao_conforme" if prob15 else "conforme",
                  f"{len(dup)} id(s) duplicado(s); landmarks ausentes: {', '.join(falt) or 'nenhum'}; "
                  f"{len(p.divs_clicaveis)} div/span clicavel sem role/tabindex; "
                  f"{p.iframes_sem_titulo}/{p.iframes} iframe(s) sem title; "
                  f"{p.tabelas_sem_th}/{p.tabelas} tabela(s) sem <th>; "
                  f"{len(bt_sem_nome)} botao(oes) sem nome acessível; "
                  f"{p.eventos_inline} manipulador(es) de evento inline.",
                  prob15, dup[:3] + falt[:2]))

    # itens que exigem inspecao humana
    for n, nome in ((5, "Contraste mínimo de cores"),
                    (6, "Cor não e o único meio de transmitir informação"),
                    (8, "Navegação completa por teclado"),
                    (9, "Indicador de foco visível"),
                    (12, "Identificacao e sugestao de correção de erros"),
                    (14, "Controle de conteúdo em movimento")):
        dica = ""
        if n == 9 and re.search(r"outline\s*:\s*(none|0)", html, re.I):
            dica = " ATENÇÃO: o CSS da página contém 'outline: none' - conferir se há foco substituto."
        if n == 14:
            c = len(re.findall(r"(carousel|carrossel|slider|swiper|owl-|slick-)", html, re.I))
            dica = f" Indicios de carrossel/slider no código: {c} ocorrência(s)."
        r.append(_res(n, nome, "verificar_manualmente",
                      "Critério subjetivo: exige inspeção humana com o site aberto." + dica))

    return sorted(r, key=lambda x: x["item"])


# ------------------------------------------------------------------ execucao
def baixar(url, timeout=30):
    ctx = ssl.create_default_context()
    ca = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
    if ca and os.path.exists(ca):
        ctx.load_verify_locations(ca)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; AuditorWCAG-IFAL/1.0)",
        "Accept-Language": "pt-BR,pt;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        bruto = resp.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", "replace")


def analisar_pagina(html, rotulo):
    p = Analisador()
    p.feed(html)
    itens = avaliar(p, html)
    return {
        "pagina": rotulo,
        "tamanho_html_kb": round(len(html) / 1024, 1),
        "total_nao_conforme": sum(1 for i in itens if i["status"] == "nao_conforme"),
        "total_conforme": sum(1 for i in itens if i["status"] == "conforme"),
        "total_manual": sum(1 for i in itens if i["status"] == "verificar_manualmente"),
        "total_ocorrencias": sum(i["ocorrencias"] for i in itens),
        "itens": itens,
    }


SIMBOLO = {"conforme": "[OK ]", "nao_conforme": "[ERRO]",
           "verificar_manualmente": "[MAN]", "nao_aplicavel": "[N/A]"}


def imprimir(rel):
    print("\n" + "=" * 78)
    print(f"PÁGINA: {rel['pagina']}   ({rel['tamanho_html_kb']} KB de HTML)")
    print("=" * 78)
    for i in rel["itens"]:
        print(f"{SIMBOLO[i['status']]} {i['item']:>2}. {i['nome']}")
        print(f"        {i['detalhe']}")
        if i["exemplos"]:
            print(f"        ex.: {'; '.join(str(e)[:60] for e in i['exemplos'][:3])}")
    print(f"\n  RESUMO: {rel['total_nao_conforme']} não conforme(s) | "
          f"{rel['total_conforme']} conforme(s) | {rel['total_manual']} para inspeção manual | "
          f"{rel['total_ocorrencias']} ocorrência(s) somadas")


def main():
    ap = argparse.ArgumentParser(description="Auditor automático WCAG 2.1 / eMAG 3.1")
    ap.add_argument("urls", nargs="*", help="URLs das páginas a auditar")
    ap.add_argument("--arquivo", action="append", default=[],
                    help="HTML salvo localmente (use quando não houver rede)")
    ap.add_argument("--url", default=None, help="URL de referência para o --arquivo")
    ap.add_argument("--saida", default=SAIDA)
    args = ap.parse_args()

    if not args.urls and not args.arquivo:
        ap.error("informe ao menos uma URL ou --arquivo")

    relatorios = []
    for caminho in args.arquivo:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            relatorios.append(analisar_pagina(f.read(), args.url or caminho))
    for url in args.urls:
        try:
            relatorios.append(analisar_pagina(baixar(url), url))
        except Exception as e:                                   # noqa: BLE001
            print(f"[FALHA] {url}: {e}", file=sys.stderr)

    if not relatorios:
        print("Nenhuma página pôde ser analisada.", file=sys.stderr)
        return 1

    for rel in relatorios:
        imprimir(rel)

    os.makedirs(os.path.dirname(args.saida), exist_ok=True)
    with open(args.saida, "w", encoding="utf-8") as f:
        json.dump({"paginas": relatorios}, f, ensure_ascii=False, indent=2)
    print(f"\nResultados gravados em: {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
