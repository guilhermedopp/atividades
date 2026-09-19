#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulador_mobile.py - Ambiente automatizado que simula o acesso a um site por
smartphone com recursos de acessibilidade ativados.

Emula um aparelho real (viewport, densidade de pixels, eventos de toque e
user-agent móvel) em Chromium e executa seis baterias de teste:

  A) Leitor de tela  - percorre a árvore de acessibilidade (a mesma estrutura
                       que TalkBack e VoiceOver consomem via CDP) e gera a
                       transcricao do que seria anunciado a cada deslize.
  B) Foco por teclado - simula Tab/Shift+Tab, registra a ordem de foco, detecta
                       foco invisível e armadilhas de foco.
  C) Alvos de toque  - mede os elementos interativos (WCAG 2.5.5 e 2.5.8).
  D) Reflow          - renderiza em 320 CSS px e detecta rolagem horizontal
                       (WCAG 1.4.10).
  E) Zoom            - verifica bloqueio de ampliacao e espacamento de texto
                       (WCAG 1.4.4 e 1.4.12).
  F) Contraste       - calcula a razão de contraste sobre a página renderizada
                       (WCAG 1.4.3), usando as cores efetivamente aplicadas.

Capturas de tela são gravadas em evidencias/mobile/ e os resultados em
dados/resultados_mobile.json.

Requisitos:
    pip install playwright && playwright install chromium

Uso:
    python3 ferramenta/simulador_mobile.py https://exemplo.gov.br
    python3 ferramenta/simulador_mobile.py https://exemplo.gov.br --aparelho pixel7
    python3 ferramenta/simulador_mobile.py http://localhost:8000 --swipes 60
"""

import argparse
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_EVID = os.path.join(RAIZ, "evidencias", "mobile")
SAIDA = os.path.join(RAIZ, "dados", "resultados_mobile.json")

APARELHOS = {
    "iphone13": {
        "nome": "Apple iPhone 13 (VoiceOver)", "leitor": "VoiceOver",
        "viewport": {"width": 390, "height": 844}, "dpr": 3, "mobile": True,
        "ua": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
               "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"),
    },
    "pixel7": {
        "nome": "Google Pixel 7 (TalkBack)", "leitor": "TalkBack",
        "viewport": {"width": 412, "height": 915}, "dpr": 2.625, "mobile": True,
        "ua": ("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"),
    },
    "galaxya54": {
        "nome": "Samsung Galaxy A54 (TalkBack)", "leitor": "TalkBack",
        "viewport": {"width": 360, "height": 800}, "dpr": 3, "mobile": True,
        "ua": ("Mozilla/5.0 (Linux; Android 13; SM-A546E) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"),
    },
}

# Papeis que o leitor de tela anuncia e que exigem nome acessivel
EXIGEM_NOME = {"button", "link", "textbox", "checkbox", "radio", "combobox", "slider",
               "searchbox", "switch", "image", "img", "menuitem", "tab", "listbox",
               "spinbutton", "progressbar"}
# Papeis puramente estruturais, ignorados na transcricao
RUIDO = {"generic", "none", "presentation", "InlineTextBox", "LineBreak", "GenericContainer",
         "paragraph", "LayoutTable", "LayoutTableRow", "LayoutTableCell", "Abbr", "SvgRoot",
         "EmphasizedText", "StrongText", "Canvas", "Legend"}

TRADUCAO = {
    "heading": "título", "link": "link", "button": "botão", "image": "imagem",
    "img": "imagem", "textbox": "caixa de edição", "searchbox": "campo de busca",
    "checkbox": "caixa de seleção", "radio": "botao de opção", "combobox": "lista suspensa",
    "list": "lista", "listitem": "item de lista", "navigation": "região de navegação",
    "main": "região principal", "banner": "cabeçalho da página",
    "contentinfo": "rodapé da página", "search": "região de busca", "form": "formulário",
    "table": "tabela", "article": "artigo", "region": "região", "dialog": "caixa de diálogo",
    "StaticText": "texto", "menuitem": "item de menu", "tab": "aba", "switch": "interruptor",
    "Iframe": "quadro embutido", "iframe": "quadro embutido", "separator": "separador",
    "figure": "figura", "complementary": "região complementar", "menu": "menu",
    "menubar": "barra de menus", "status": "mensagem de status", "alert": "alerta",
    "textarea": "área de texto", "option": "opção", "graphics-document": "gráfico",
}

# ---------------------------------------------------------------- JS auxiliar
JS_CONTRASTE = r"""
() => {
  const lum = (c) => {
    const s = c.map(v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2];
  };
  const rgb = (str) => {
    const m = String(str).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x.trim()));
    return { c: [p[0],p[1],p[2]], a: p.length > 3 ? p[3] : 1 };
  };
  const fundo = (el) => {
    let n = el;
    while (n && n.nodeType === 1) {
      const b = rgb(getComputedStyle(n).backgroundColor);
      if (b && b.a > 0.1) return b.c;
      n = n.parentElement;
    }
    return [255,255,255];
  };
  const visível = (el) => {
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) < 0.1) return false;
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const txt = Array.from(el.childNodes)
      .filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
    if (!txt || txt.length < 2 || !visível(el)) return;
    const st = getComputedStyle(el);
    const f = rgb(st.color); if (!f) return;
    const b = fundo(el);
    const l1 = lum(f.c), l2 = lum(b);
    const razao = (Math.max(l1,l2) + 0.05) / (Math.min(l1,l2) + 0.05);
    const px = parseFloat(st.fontSize);
    const peso = parseInt(st.fontWeight) || 400;
    const grande = px >= 24 || (px >= 18.66 && peso >= 700);
    const exigido = grande ? 3.0 : 4.5;
    out.push({
      texto: txt.slice(0, 60), razao: Math.round(razao * 100) / 100, exigido,
      aprovado: razao >= exigido, px: Math.round(px * 10) / 10, peso,
      cor: st.color, fundo: 'rgb(' + b.join(',') + ')',
      seletor: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
               ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '')
    });
  });
  return out;
}
"""

JS_ALVOS = r"""
() => {
  const sel = 'a[href], button, input:not([type=hidden]), select, textarea, ' +
              '[role=button], [role=link], [onclick], [tabindex]:not([tabindex="-1"])';
  const out = [];
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    if (r.width < 1 || r.height < 1 || s.display === 'none' || s.visibility === 'hidden') return;
    const nome = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title')
                  || el.value || '').trim().replace(/\s+/g, ' ');
    out.push({
      tag: el.tagName.toLowerCase(), nome: nome.slice(0, 50),
      largura: Math.round(r.width), altura: Math.round(r.height),
      menor: Math.round(Math.min(r.width, r.height))
    });
  });
  return out;
}
"""

JS_ESPACAMENTO = r"""
() => {
  const st = document.createElement('style');
  st.id = '__teste_espacamento__';
  st.textContent = '*{line-height:1.5 !important;letter-spacing:0.12em !important;' +
                   'word-spacing:0.16em !important;} p{margin-bottom:2em !important;}';
  document.head.appendChild(st);
  const h = document.documentElement.scrollWidth > document.documentElement.clientWidth + 2;
  let cortado = 0;
  document.querySelectorAll('p, h1, h2, h3, li, a, button, span').forEach(el => {
    if (el.scrollHeight > el.clientHeight + 4 &&
        getComputedStyle(el).overflow === 'hidden') cortado++;
  });
  st.remove();
  return { rolagem_horizontal: h, elementos_cortados: cortado };
}
"""

JS_FOCO = r"""
() => {
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  const s = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  const semContorno = (s.outlineStyle === 'none' || parseFloat(s.outlineWidth) === 0);
  const temAlternativa = s.boxShadow !== 'none' || parseFloat(s.borderWidth) > 2;
  return {
    tag: el.tagName.toLowerCase(),
    nome: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title')
           || el.value || el.alt || '').trim().replace(/\s+/g,' ').slice(0, 60),
    href: (el.getAttribute('href') || '').slice(0, 60),
    foco_visivel: !semContorno || temAlternativa,
    dentro_da_tela: r.top >= -2 && r.bottom <= window.innerHeight + 2,
    x: Math.round(r.x), y: Math.round(r.y)
  };
}
"""


# ------------------------------------------------------------------- funcoes
def anuncio(role, nome, nivel=None):
    """Monta a frase que o leitor de tela verbalizaria."""
    papel = TRADUCAO.get(role, role)
    if role == "heading" and nivel:
        papel = f"título nível {nivel}"
    if not nome:
        if role in EXIGEM_NOME:
            return f"<<{papel} SEM RÓTULO>>", True
        return papel, False
    return f"{nome}, {papel}", False


def coletar_arvore(sessao):
    sessao.send("Accessibility.enable")
    return sessao.send("Accessibility.getFullAXTree").get("nodes", [])


def transcricao(nos, limite):
    """Converte a árvore de acessibilidade na sequencia de anúncios."""
    linhas, mudos, vistos = [], [], set()
    for n in nos:
        if n.get("ignored"):
            continue
        role = (n.get("role") or {}).get("value") or ""
        if role in RUIDO or role == "RootWebArea":
            continue
        nome = ((n.get("name") or {}).get("value") or "").strip()
        nome = re.sub(r"\s+", " ", nome)
        nivel = None
        for prop in n.get("properties", []):
            if prop.get("name") == "level":
                nivel = prop.get("value", {}).get("value")
        if role == "StaticText":
            if not nome or nome in vistos:
                continue
            vistos.add(nome)
        frase, mudo = anuncio(role, nome, nivel)
        if mudo:
            mudos.append({"papel": role, "posicao": len(linhas) + 1})
        linhas.append(frase)
        if len(linhas) >= limite:
            break
    return linhas, mudos


def achar_conteudo(linhas):
    """Quantos deslizes até o conteúdo principal ser anunciado."""
    alvos = ("região principal", "título nível 1")
    for i, l in enumerate(linhas, 1):
        if any(a in l.lower() for a in alvos):
            return i
    return None


def testar(url, ap, swipes, tabs, headless=True):
    from playwright.sync_api import sync_playwright

    exe = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
    os.makedirs(DIR_EVID, exist_ok=True)
    r = {"url": url, "aparelho": ap["nome"], "leitor_tela_simulado": ap["leitor"],
         "viewport": ap["viewport"], "dpr": ap["dpr"]}

    with sync_playwright() as p:
        lanc = {"headless": headless}
        if os.path.exists(exe):
            lanc["executable_path"] = exe
        nav = p.chromium.launch(**lanc)
        ctx = nav.new_context(
            viewport=ap["viewport"], device_scale_factor=ap["dpr"],
            is_mobile=ap["mobile"], has_touch=True, user_agent=ap["ua"],
            locale="pt-BR",
        )
        pg = ctx.new_page()

        # Recursos que não carregam (CDN bloqueado, domínio fora do allowlist)
        # distorcem silenciosamente o contraste e o reflow: a página é medida
        # sem o CSS que ela deveria ter. Por isso são contados e reportados.
        falhas_rede = []
        pg.on("requestfailed", lambda r: falhas_rede.append({
            "url": r.url[:120], "tipo": r.resource_type,
            "motivo": (r.failure or "")[:60]}))

        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        try:
            pg.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass

        base = re.sub(r"[^a-z0-9]+", "-", url.lower())[:60].strip("-")
        cap = os.path.join(DIR_EVID, f"{base}-{ap['viewport']['width']}px.png")
        pg.screenshot(path=cap, full_page=True)
        r["captura_tela"] = os.path.relpath(cap, RAIZ)
        r["titulo_pagina"] = pg.title()

        criticos = [f for f in falhas_rede
                    if f["tipo"] in ("stylesheet", "script", "font", "image")]
        dominios = sorted({re.sub(r"^https?://([^/]+).*", r"\1", f["url"])
                           for f in criticos})
        r["recursos_nao_carregados"] = {
            "total": len(falhas_rede),
            "criticos_para_a_medicao": len(criticos),
            "dominios": dominios[:10],
            "medicao_confiavel": not criticos,
            "detalhe": criticos[:10],
        }

        # A) leitor de tela
        sess = ctx.new_cdp_session(pg)
        linhas, mudos = transcricao(coletar_arvore(sess), swipes)
        r["leitor_tela"] = {
            "anuncios_analisados": len(linhas),
            "elementos_sem_rotulo": len(mudos),
            "detalhe_sem_rotulo": mudos[:15],
            "deslizes_ate_conteudo": achar_conteudo(linhas),
            "transcricao": linhas,
        }

        # B) foco por teclado
        ordem, sem_foco, repetidos = [], 0, 0
        anterior = None
        for _ in range(tabs):
            pg.keyboard.press("Tab")
            f = pg.evaluate(JS_FOCO)
            if not f:
                break
            if anterior and f["tag"] == anterior["tag"] and f["nome"] == anterior["nome"]\
                    and f["x"] == anterior["x"] and f["y"] == anterior["y"]:
                repetidos += 1
                if repetidos >= 3:
                    break
            else:
                repetidos = 0
            if not f["foco_visivel"]:
                sem_foco += 1
            ordem.append(f)
            anterior = f
        r["foco_teclado"] = {
            "elementos_focaveis": len(ordem),
            "sem_indicador_visivel": sem_foco,
            "fora_da_tela_ao_focar": sum(1 for f in ordem if not f["dentro_da_tela"]),
            "sem_nome_acessivel": sum(1 for f in ordem if not f["nome"]),
            "possivel_armadilha_foco": repetidos >= 3,
            "ordem": ordem[:30],
        }

        # C) alvos de toque
        alvos = pg.evaluate(JS_ALVOS)
        peq_aa = [a for a in alvos if a["menor"] < 24]
        peq_aaa = [a for a in alvos if a["menor"] < 44]
        r["alvos_toque"] = {
            "total": len(alvos),
            "menores_que_24px_AA": len(peq_aa),
            "menores_que_44px_AAA": len(peq_aaa),
            "exemplos": sorted(peq_aaa, key=lambda a: a["menor"])[:10],
        }

        # D) reflow em 320 px
        pg.set_viewport_size({"width": 320, "height": 800})
        pg.wait_for_timeout(600)
        reflow = pg.evaluate(
            "() => ({larg: document.documentElement.scrollWidth,"
            " tela: document.documentElement.clientWidth})")
        cap2 = os.path.join(DIR_EVID, f"{base}-320px-reflow.png")
        pg.screenshot(path=cap2, full_page=True)
        r["reflow_320px"] = {
            "largura_conteudo": reflow["larg"], "largura_tela": reflow["tela"],
            "rolagem_horizontal": reflow["larg"] > reflow["tela"] + 2,
            "captura": os.path.relpath(cap2, RAIZ),
        }
        pg.set_viewport_size(ap["viewport"])
        pg.wait_for_timeout(400)

        # E) zoom e espacamento de texto
        vp = pg.evaluate(
            "() => { const m = document.querySelector('meta[name=viewport]');"
            " return m ? m.getAttribute('content') : ''; }") or ""
        limpo = vp.replace(" ", "").lower()
        bloqueia = ("user-scalable=no" in limpo
                    or bool(re.search(r"maximum-scale=(1(\.0+)?|0?\.\d+)\b", limpo)))
        r["zoom"] = {"meta_viewport": vp, "zoom_bloqueado": bloqueia,
                     "espacamento_texto": pg.evaluate(JS_ESPACAMENTO)}

        # F) contraste
        c = pg.evaluate(JS_CONTRASTE)
        reprov = [x for x in c if not x["aprovado"]]
        r["contraste"] = {
            "trechos_analisados": len(c), "reprovados": len(reprov),
            "pior_razao": min([x["razao"] for x in c], default=None),
            "exemplos": sorted(reprov, key=lambda x: x["razao"])[:10],
        }

        nav.close()
    return r


# -------------------------------------------------------------------- saida
def imprimir(r):
    lt, fk, at, rf, zm, ct = (r["leitor_tela"], r["foco_teclado"], r["alvos_toque"],
                              r["reflow_320px"], r["zoom"], r["contraste"])
    p = print
    rec = r.get("recursos_nao_carregados") or {}
    if rec and not rec.get("medicao_confiavel", True):
        p("\n" + "!" * 78)
        p(f"ATENÇÃO: {rec['criticos_para_a_medicao']} recurso(s) de CSS/fonte/script/imagem")
        p("não carregaram. A página foi medida sem parte da sua aparência real, portanto")
        p("o CONTRASTE e o REFLOW abaixo NÃO são confiáveis.")
        p(f"Domínios envolvidos: {', '.join(rec['dominios']) or '(desconhecido)'}")
        p("Libere esses domínios no ambiente e rode de novo.")
        p("!" * 78)
    p("\n" + "=" * 78)
    p(f"SIMULAÇÃO MOBILE COM ACESSIBILIDADE - {r['aparelho']}")
    p(f"URL: {r['url']}")
    p(f"Viewport: {r['viewport']['width']}x{r['viewport']['height']} @ {r['dpr']}x  |  "
      f"Leitor simulado: {r['leitor_tela_simulado']}")
    p("=" * 78)

    p("\n[A] LEITOR DE TELA - árvore de acessibilidade")
    p(f"    Anúncios analisados ............. {lt['anuncios_analisados']}")
    p(f"    Elementos anunciados SEM RÓTULO . {lt['elementos_sem_rotulo']}   <- WCAG 1.1.1 / 4.1.2 (A)")
    d = lt["deslizes_ate_conteudo"]
    p(f"    Deslizes até o conteúdo principal {d if d else 'NÃO ENCONTRADO (sem <main> nem h1)'}"
      + ("   <- WCAG 2.4.1 (A)" if (d is None or d > 15) else ""))
    p("    Transcrição (primeiros 12 anúncios):")
    for i, l in enumerate(lt["transcricao"][:12], 1):
        p(f"      {i:>2}. {l[:68]}")

    p("\n[B] NAVEGAÇÃO POR FOCO (teclado / switch access)")
    p(f"    Elementos focáveis .............. {fk['elementos_focaveis']}")
    p(f"    Sem indicador de foco visível ... {fk['sem_indicador_visivel']}   <- WCAG 2.4.7 (AA)")
    p(f"    Sem nome acessível .............. {fk['sem_nome_acessivel']}   <- WCAG 4.1.2 (A)")
    p(f"    Armadilha de foco detectada ..... {'SIM' if fk['possivel_armadilha_foco'] else 'não'}"
      "   <- WCAG 2.1.2 (A)")

    p("\n[C] ALVOS DE TOQUE")
    p(f"    Elementos interativos ........... {at['total']}")
    p(f"    Menores que 24x24 px ............ {at['menores_que_24px_AA']}   <- WCAG 2.5.8 (AA)")
    p(f"    Menores que 44x44 px ............ {at['menores_que_44px_AAA']}   <- WCAG 2.5.5 (AAA)")
    for a in at["exemplos"][:5]:
        p(f"      - {a['tag']:<8} {a['largura']}x{a['altura']} px  \"{a['nome'][:34]}\"")

    p("\n[D] REFLOW EM 320 CSS PX")
    p(f"    Conteúdo: {rf['largura_conteudo']} px / tela: {rf['largura_tela']} px -> "
      f"rolagem horizontal: {'SIM' if rf['rolagem_horizontal'] else 'não'}   <- WCAG 1.4.10 (AA)")

    p("\n[E] ZOOM E ESPAÇAMENTO DE TEXTO")
    p(f"    meta viewport: {zm['meta_viewport'][:62]!r}")
    p(f"    Zoom bloqueado .................. {'SIM' if zm['zoom_bloqueado'] else 'não'}"
      "   <- WCAG 1.4.4 (AA)")
    e = zm["espacamento_texto"]
    p(f"    Espaçamento ampliado: rolagem horizontal={'SIM' if e['rolagem_horizontal'] else 'não'}, "
      f"{e['elementos_cortados']} elemento(s) cortado(s)   <- WCAG 1.4.12 (AA)")

    p("\n[F] CONTRASTE DE CORES (página renderizada)")
    p(f"    Trechos de texto analisados ..... {ct['trechos_analisados']}")
    p(f"    Reprovados ...................... {ct['reprovados']}   <- WCAG 1.4.3 (AA)")
    p(f"    Pior razão encontrada ........... {ct['pior_razao']}:1")
    for x in ct["exemplos"][:5]:
        p(f"      - {x['razao']}:1 (exige {x['exigido']}:1)  {x['seletor'][:22]:<22} \"{x['texto'][:26]}\"")

    if rec.get("medicao_confiavel", True):
        p(f"\n[G] INTEGRIDADE DA MEDIÇÃO")
        p(f"    Todos os recursos da página carregaram — contraste e reflow confiáveis.")
    p(f"\n    Capturas: {r['captura_tela']} | {rf['captura']}")


def main():
    ap = argparse.ArgumentParser(description="Simulador de acesso mobile com acessibilidade")
    ap.add_argument("url", help="URL a testar")
    ap.add_argument("--aparelho", default="pixel7", choices=sorted(APARELHOS),
                    help="aparelho a emular (padrão: pixel7)")
    ap.add_argument("--swipes", type=int, default=80,
                    help="máximo de anúncios do leitor de tela a transcrever")
    ap.add_argument("--tabs", type=int, default=60, help="máximo de Tabs a simular")
    ap.add_argument("--mostrar-navegador", action="store_true", help="desliga o modo headless")
    ap.add_argument("--saida", default=SAIDA)
    args = ap.parse_args()

    try:
        r = testar(args.url, APARELHOS[args.aparelho], args.swipes, args.tabs,
                   headless=not args.mostrar_navegador)
    except Exception as e:                                          # noqa: BLE001
        print(f"[FALHA] {args.url}: {e}", file=sys.stderr)
        return 1

    imprimir(r)
    os.makedirs(os.path.dirname(args.saida), exist_ok=True)
    anteriores = []
    if os.path.exists(args.saida):
        try:
            anteriores = json.load(open(args.saida, encoding="utf-8")).get("execucoes", [])
        except Exception:                                           # noqa: BLE001
            anteriores = []
    anteriores = [x for x in anteriores
                  if not (x.get("url") == r["url"] and x.get("aparelho") == r["aparelho"])]
    anteriores.append(r)
    with open(args.saida, "w", encoding="utf-8") as f:
        json.dump({"execucoes": anteriores}, f, ensure_ascii=False, indent=2)
    print(f"\nResultados gravados em: {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
