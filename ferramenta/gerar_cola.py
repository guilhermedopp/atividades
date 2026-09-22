#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a cola de uma página para levar na mão durante a apresentação.

Os números saem de dados/dados_trabalho.json, o mesmo arquivo que alimenta o
relatório, então a cola não pode divergir dele.

Uso:  python3 ferramenta/gerar_cola.py [saida.docx]
"""
import json
import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "COLA_APRESENTACAO.docx")
FONTE = "Arial"
ESCURO = RGBColor(0x1A, 0x1A, 0x1A)
VERM = RGBColor(0xB7, 0x1C, 0x1C)
CINZA = RGBColor(0x55, 0x55, 0x55)

d = json.load(open(os.path.join(RAIZ, "dados", "dados_trabalho.json"), encoding="utf-8"))
w, a, cp, m = d["wave"], d["ases"], d["contraste_pixel"], d["mobile"]
cf, axe = d["conformidade"], d["axe"]["paginas"]
from collections import Counter                                      # noqa: E402
sit = Counter(v["situacao"] for v in d["checklist_manual"].values())


def vg(x):
    """Vírgula decimal."""
    return str(x).replace(".", ",")


doc = Document()
n = doc.styles["Normal"]
n.font.name = FONTE
n.font.size = Pt(11.5)
n._element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
n.paragraph_format.line_spacing = 1.12
n.paragraph_format.space_after = Pt(0)
s = doc.sections[0]
s.page_width, s.page_height = Cm(21.0), Cm(29.7)
s.left_margin = s.right_margin = Cm(1.2)
s.top_margin = s.bottom_margin = Cm(1.1)
LARG = 18.6


def par(trechos, tam=11.5, antes=0, depois=2, esp=1.08, alin=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(antes), Pt(depois)
    pf.line_spacing = esp
    if alin is not None:
        pf.alignment = alin
    for texto, negrito, cor in trechos:
        r = p.add_run(texto)
        r.font.name, r.font.size = FONTE, Pt(tam)
        r.bold = negrito
        r.font.color.rgb = cor
    return p


def faixa(texto):
    """Cabeçalho de bloco, em caixa alta e com regra embaixo."""
    p = par([(texto, True, ESCURO)], tam=12.5, antes=9, depois=3)
    pb = OxmlElement("w:pBdr")
    bt = OxmlElement("w:bottom")
    bt.set(qn("w:val"), "single")
    bt.set(qn("w:sz"), "8")
    bt.set(qn("w:color"), "999999")
    pb.append(bt)
    p._p.get_or_add_pPr().append(pb)


def celula(cel, trechos, tam=11.5, alin=None):
    cel.text = ""
    p = cel.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    if alin is not None:
        p.alignment = alin
    for texto, negrito, cor in trechos:
        r = p.add_run(texto)
        r.font.name, r.font.size = FONTE, Pt(tam)
        r.bold = negrito
        r.font.color.rgb = cor


def tabela(linhas, larguras, tam=11.5):
    t = doc.add_table(rows=0, cols=len(larguras))
    t.style = "Table Grid"
    t.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(layout)
    grid = OxmlElement("w:tblGrid")
    for l in larguras:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(Cm(l).twips)))
        grid.append(col)
    antigo = t._tbl.find(qn("w:tblGrid"))
    t._tbl.replace(antigo, grid) if antigo is not None else t._tbl.insert(1, grid)
    for dados in linhas:
        cels = t.add_row().cells
        for i, (conteudo, l) in enumerate(zip(dados, larguras)):
            celula(cels[i], conteudo, tam=tam)
            cels[i].width = Cm(l)
    return t


# ─────────────────────────────────────────────────────────────── cabeçalho
par([("COLA — Avaliação de Acessibilidade WCAG 2.1 · Portal do IFAL Campus Maceió",
      True, ESCURO)], tam=14.5, depois=2)
par([("Veredito: ", True, ESCURO), (cf["nivel_atingido"].upper(), True, VERM),
     ("  — por 1.4.1 (slide ativo só pela cor) e 2.2.2 (banner sem pausa). "
      "Uma falha de Nível A derruba a conformidade em qualquer nível.", False, CINZA)],
    tam=11.5, depois=3)

# ─────────────────────────────────────────────────────────────── números
faixa("NÚMEROS")
pior = vg(min(r["razao"] for r in cp["reprovacoes_confirmadas"]))
foco = cp["indicador_de_foco"]
tabela([
    [[("ASES", True, ESCURO)],
     [(f"nota {a['nota_geral']}%", True, ESCURO),
      (f" · {a['total_erros']} erros · {a['total_avisos']} avisos · "
       f"Marcação {a['marcacao_erros']} · Conteúdo {a['conteudo_erros']}", False, ESCURO)]],
    [[("WAVE", True, ESCURO)],
     [(f"{w['errors']} erros · {w['contrast_errors']} contraste · {w['alerts']} alertas · "
       f"{w['features']} recursos · {w['structural_elements']} estruturais · "
       f"{w['aria']} ARIA", False, ESCURO)]],
    [[("axe-core", True, ESCURO)],
     [(f"{sum(r['violacoes_wcag'] for r in axe.values())} violações WCAG A/AA", True, ESCURO),
      ("  nas 3 páginas — só no relatório, seção 4.4", False, CINZA)]],
    [[("Contraste", True, ESCURO)],
     [(f"{len(cp['reprovacoes_confirmadas'])} reprovações confirmadas · pior {pior}:1",
       True, ESCURO),
      (f" (exige 4,5:1) · foco {vg(foco['sobre_branco'])}:1 no branco "
       f"(exige {vg(foco['exigido_1411'])}:1)", False, ESCURO)]],
    [[("Mobile", True, ESCURO)],
     [("23 de 58 alvos < 24×24 px · 3 elementos cortados com espaçamento ampliado · "
       "reflow em 320 px OK · viewport 412×915", False, ESCURO)]],
    [[("Checklist", True, ESCURO)],
     [(f"{sit['conforme']} conformes · {sit['parcial']} parciais · "
       f"{sit['nao_conforme']} não conformes · {sit['nao_aplicavel']} não aplicável",
       False, ESCURO)]],
    [[("TalkBack", True, ESCURO)],
     [("Galaxy A15, Android 16 · 1ª tentativa abandonada aos 12 min 4 s · "
       "2ª concluída em 10 min 16 s", False, ESCURO)]],
    [[("Teclado", True, ESCURO)],
     [("117 elementos interativos · 118 pontos de parada alcançados · "
       "sem armadilha de foco", False, ESCURO)]],
], [2.5, LARG - 2.5])

# ─────────────────────────────────────────────────────────────── viradas
faixa("AS QUATRO VIRADAS")
for origem, frase in [
    ("3 → 4", "Guardem essa regra: uma falha de Nível A derruba a conformidade em "
              "qualquer nível. Ela vai decidir o resultado deste trabalho."),
    ("7 → 8", "Nota 90,48% e os erros do WAVE nem são do IFAL. Parece um site conforme. "
              "Mas nenhuma dessas ferramentas olha para o que vem agora."),
    ("10 → 11", "O recurso de acessibilidade mais visível do portal foi o único que "
                "nenhuma ferramenta automática encontrou. Isso muda o que a gente conclui."),
    ("11 → 12", "Não atinge o Nível A por dois critérios. E os dois têm correção de "
                "baixo custo."),
]:
    par([(f"{origem}   ", True, VERM), (f"“{frase}”", False, ESCURO)], tam=11.5, depois=4)

# ─────────────────────────────────────────────────────────────── perguntas
faixa("SEIS PERGUNTAS")
for pergunta, resposta in [
    ("ASES deu 90%, então é acessível?",
     "Mede aderência ao eMAG, não conformidade WCAG. Não testa 2.2.2 nem 1.4.1 — "
     "os dois que derrubam o Nível A."),
    ("90,48% com 310 avisos ao mesmo tempo?",
     "O ASES pondera por gravidade; a maioria dos avisos cai na recomendação 1.1, "
     "de peso menor."),
    ("Os 4 erros do WAVE são do IFAL?",
     "Não. Vêm do barra.brasil.gov.br: 1 imagem sem alt e 2 âncoras vazias. "
     "O terceiro link vazio não foi possível atribuir — e o relatório diz isso."),
    ("Usaram só WAVE e ASES?",
     "Também o axe-core 4.10.2, da Deque, motor do Lighthouse: zero violações A/AA. "
     "O WAVE tem motor próprio, do WebAIM. Está no relatório, seção 4.4."),
    ("Como acharam o VLibras se as ferramentas não acharam?",
     "Abrindo no Android real e fotografando. É injetado por script de terceiro, "
     "não existe no HTML que o servidor entrega."),
    ("O teste com TalkBack mediu o site ou a ferramenta?",
     "O relatório separa. Do portal: a quantidade de elementos até o edital e a "
     "sequência de leitura pouco coerente — 1.3.2 e 2.4.3."),
]:
    par([("• ", True, VERM), (pergunta + "  ", True, ESCURO), (resposta, False, ESCURO)],
        tam=11.5, depois=4)

par([("Não narrar em primeira pessoa o teste com TalkBack: foi executado por um "
      "integrante. Dizer “a equipe executou” e descrever o que foi observado.",
      True, VERM)], tam=11, antes=8, depois=0)

doc.save(SAIDA)
print("gerado:", SAIDA)
