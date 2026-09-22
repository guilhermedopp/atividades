#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_documentos.py - Monta o relatório (.docx) e a apresentação (.pptx) a partir
dos dados coletados.

Fontes de dados:
    dados/checklist.json             - os 15 itens do checklist (fixo)
    dados/dados_trabalho.json        - dados da equipe, do site e dos avaliadores
    dados/resultados_automaticos.json - saida de ferramenta/auditor_wcag.py (opcional)
    dados/resultados_mobile.json      - saida de ferramenta/simulador_mobile.py (opcional)

Campos ainda não preenchidos aparecem destacados em amarelo no relatório e em
vermelho nos slides, como [PREENCHER: ...].

Uso:
    python3 ferramenta/gerar_documentos.py
"""

import argparse
import json
import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX,
                            WD_TAB_ALIGNMENT, WD_TAB_LEADER)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from pptx import Presentation
from pptx.dml.color import RGBColor as PPTColor
from pptx.util import Emu, Inches, Pt as PPt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textos as T                                                   # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
MODELO_PPTX = os.path.join(RAIZ, "ferramenta", "modelo_apresentacao.pptx")
SAIDA_DOCX = os.path.join(RAIZ, "relatorio", "RELATORIO_AVALIACAO_ACESSIBILIDADE_WCAG.docx")
SAIDA_PPTX = os.path.join(RAIZ, "apresentacao", "APRESENTACAO_AVALIACAO_ACESSIBILIDADE.pptx")

FONTE = "Arial"
MARCADOR = re.compile(r"\x00(.*?)\x01", re.S)


# ------------------------------------------------------------------ carga
def carregar(nome, padrao=None):
    caminho = os.path.join(DADOS, nome)
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def preparar(arquivo_dados="dados_trabalho.json"):
    d = carregar(arquivo_dados)
    if d is None:
        sys.exit("ERRO: dados/dados_trabalho.json não encontrado.")
    ck = carregar("checklist.json")
    d["_checklist"] = {str(i["id"]): i for i in ck["itens"]}
    d["_checklist_meta"] = ck
    d["_auto"] = carregar("resultados_automaticos.json", {}) or {}
    d["_mobile"] = carregar("resultados_mobile.json", {}) or {}
    return d


# ---------------------------------------------------- utilidades de texto
def V(valor, dica):
    return T.V(valor, dica)


def segmentos(texto):
    """Divide o texto em pedacos (conteúdo, e_marcador)."""
    saida, pos = [], 0
    for m in MARCADOR.finditer(texto):
        if m.start() > pos:
            saida.append((texto[pos:m.start()], False))
        saida.append((m.group(1), True))
        pos = m.end()
    if pos < len(texto):
        saida.append((texto[pos:], False))
    return saida or [(texto, False)]


def tem_marcador(texto):
    return "\x00" in str(texto)


def limpo(texto):
    return str(texto).replace("\x00", "").replace("\x01", "")


# --------------------------------------------------------------- DOCX
def estilo_base(doc):
    n = doc.styles["Normal"]
    n.font.name = FONTE
    n.font.size = Pt(12)
    n._element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
    pf = n.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Medidas retiradas do modelo entregue pela disciplina: margens de 2,54 cm
    # nos quatro lados, corpo em Arial 12, entrelinha 1,5.
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.01), Cm(29.69)
    s.left_margin = s.right_margin = Cm(2.54)
    s.top_margin = s.bottom_margin = Cm(2.54)


def numerar_paginas(sec):
    """Insere o número da página no rodapé da seção (campo PAGE do Word).

    O modelo da disciplina não numera as páginas, mas ele tem seis páginas e
    este relatório passa de trinta. Mantém-se a numeração, desligada na capa e
    na folha de rosto: elas ficam em uma seção própria, sem rodapé.
    """
    sec.footer.is_linked_to_previous = False
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run()
    r.font.name, r.font.size = FONTE, Pt(10)
    for tipo, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        el = OxmlElement("w:fldChar") if tipo else OxmlElement("w:instrText")
        if tipo:
            el.set(qn("w:fldCharType"), tipo)
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        r._r.append(el)


def par(doc, texto="", *, negrito=False, tamanho=12, alinhamento=None, espaco_depois=0,
        espaco_antes=0, recuo=None, espacamento=1.5, maiusculas=False, cor=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = espacamento
    pf.space_after = Pt(espaco_depois)
    pf.space_before = Pt(espaco_antes)
    if alinhamento is not None:
        pf.alignment = alinhamento
    if recuo is not None:
        pf.first_line_indent = Cm(recuo)
    for conteudo, marcador in segmentos(str(texto)):
        if not conteudo:
            continue
        r = p.add_run(conteudo.upper() if maiusculas else conteudo)
        r.font.name, r.font.size = FONTE, Pt(tamanho)
        r.bold = negrito
        if cor:
            r.font.color.rgb = cor
        if marcador:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r.bold = True
    return p


def titulo_secao(doc, texto, nivel=1):
    """Título de seção no formato do modelo: 14 pt no nível 1, 13 pt no nível 2,
    negrito, justificado, com 12 pt de espaço antes e depois."""
    par(doc, texto, negrito=True, tamanho=14 if nivel == 1 else 13,
        alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY,
        espaco_antes=12, espaco_depois=12, maiusculas=(nivel == 1))


def corpo(doc, texto):
    """Parágrafo de corpo no formato do modelo: Arial 12, justificado,
    entrelinha 1,5, 12 pt antes e depois, sem recuo de primeira linha."""
    par(doc, texto, alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY,
        espaco_antes=12, espaco_depois=12)


def item_lista(doc, texto, simbolo="•"):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(f"{simbolo} ")
    r.font.name, r.font.size = FONTE, Pt(12)
    for conteudo, marcador in segmentos(str(texto)):
        if not conteudo:
            continue
        r = p.add_run(conteudo)
        r.font.name, r.font.size = FONTE, Pt(12)
        if marcador:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r.bold = True


def celula(cel, texto, *, negrito=False, tamanho=10, centralizar=False, cor=None):
    cel.text = ""
    p = cel.paragraphs[0]
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(2)
    # Em coluna estreita, o justificado do corpo abre vãos enormes entre as
    # palavras. Dentro de tabela o texto fica alinhado à esquerda.
    p.alignment = (WD_ALIGN_PARAGRAPH.CENTER if centralizar
                   else WD_ALIGN_PARAGRAPH.LEFT)
    for conteudo, marcador in segmentos(str(texto)):
        if not conteudo:
            continue
        r = p.add_run(conteudo)
        r.font.name, r.font.size = FONTE, Pt(tamanho)
        r.bold = negrito
        if cor:
            r.font.color.rgb = cor
        if marcador:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r.bold = True


def sombrear(cel, cor="D9D9D9"):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:fill"), cor)
    cel._tc.get_or_add_tcPr().append(sh)


def legenda(doc, texto):
    par(doc, texto, tamanho=10, alinhamento=WD_ALIGN_PARAGRAPH.LEFT, espaco_depois=10,
        espacamento=1.0)


def tabela(doc, cabecalhos, larguras, linhas):
    t = doc.add_table(rows=1, cols=len(cabecalhos))
    t.style = "Table Grid"
    t.autofit = False
    # Sem tblLayout fixo o Word e o LibreOffice redistribuem as colunas pelo
    # conteúdo e ignoram as larguras pedidas.
    tbl_pr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    grid = OxmlElement("w:tblGrid")
    for l in larguras:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(Cm(l).twips)))
        grid.append(col)
    antigo = t._tbl.find(qn("w:tblGrid"))
    if antigo is not None:
        t._tbl.replace(antigo, grid)
    else:
        t._tbl.insert(1, grid)
    for i, (h, l) in enumerate(zip(cabecalhos, larguras)):
        celula(t.rows[0].cells[i], h, negrito=True, centralizar=True)
        sombrear(t.rows[0].cells[i])
        for row in t.rows:
            row.cells[i].width = Cm(l)
    # Centralizar é decisão de coluna, não de célula: só se todos os valores
    # daquela coluna forem curtos, como a de numeração. Misturar centralizado e
    # alinhado à esquerda na mesma coluna deixa a tabela visualmente torta.
    centrar = []
    for i in range(len(cabecalhos)):
        valores = [str(limpo(ln[i])) for ln in linhas if i < len(ln)]
        centrar.append(bool(valores) and max(len(v) for v in valores) <= 6)

    for dados in linhas:
        cels = t.add_row().cells
        for i, (valor, l) in enumerate(zip(dados, larguras)):
            celula(cels[i], valor, centralizar=centrar[i])
            cels[i].width = Cm(l)
    return t


SITUACAO = {
    "conforme": ("Conforme", RGBColor(0x1B, 0x5E, 0x20)),
    "nao_conforme": ("Não conforme", RGBColor(0xB7, 0x1C, 0x1C)),
    "parcial": ("Parcial", RGBColor(0xE6, 0x5B, 0x00)),
    "nao_aplicavel": ("Não aplicável", RGBColor(0x42, 0x42, 0x42)),
    "verificar_manualmente": ("Verificar", RGBColor(0x42, 0x42, 0x42)),
}


def rotulo_situacao(valor):
    if not valor:
        return V(None, "Conforme / Não conforme / Parcial"), None
    chave = str(valor).strip().lower().replace(" ", "_").replace("ã", "a").replace("ç", "c")
    return SITUACAO.get(chave, (str(valor), None))


def execucao_principal(d):
    """Escolhe a execução do simulador que corresponde à página principal.

    O simulador pode ter sido rodado várias vezes, em páginas e aparelhos
    diferentes. O relatório descreve uma delas, e a escolhida deve ser a
    primeira página declarada em site.paginas_avaliadas — caso contrário o
    texto acaba citando uma página enquanto os números vêm de outra.
    """
    exes = d["_mobile"].get("execucoes", [])
    if not exes:
        return None
    alvo = (d.get("site", {}).get("paginas_avaliadas") or [None])[0]
    for e in exes:
        if alvo and e.get("url") == alvo:
            return e
    return exes[-1]


def auto_por_item(d):
    """Mapeia item do checklist -> pior resultado automático entre as páginas."""
    mapa = {}
    for pag in d["_auto"].get("paginas", []):
        for it in pag["itens"]:
            k = str(it["item"])
            ant = mapa.get(k)
            if ant is None or (it["status"] == "nao_conforme" and ant["status"] != "nao_conforme"):
                mapa[k] = it
            elif ant and it["status"] == ant["status"]:
                ant["ocorrencias"] = ant.get("ocorrencias", 0) + it.get("ocorrencias", 0)
    return mapa


# ------------------------------------------------------------ montagem docx
LOGO = os.path.join(RAIZ, "ferramenta", "logo_ifal.png")


def inserir_logo(doc):
    """Brasão do IFAL centralizado, nas medidas do modelo (2,15 x 2,75 cm)."""
    if not os.path.exists(LOGO):
        return
    try:
        doc.add_picture(LOGO, width=Cm(2.15), height=Cm(2.75))
    except Exception:
        return
    p = doc.paragraphs[-1]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(0)


def capa(doc, d):
    ins, eq = d["instituicao"], d["equipe"]
    inserir_logo(doc)
    for linha in (ins["nome"], ins["campus"], ins["curso"]):
        par(doc, linha, negrito=True, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)
    for _ in range(6):
        par(doc, "", espacamento=1.5)
    par(doc, "RELATÓRIO DE AVALIAÇÃO DE ACESSIBILIDADE WEB",
        negrito=True, tamanho=13, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.5)
    par(doc, V(d["site"].get("nome"), "nome do site avaliado").upper()
        if not tem_marcador(V(d["site"].get("nome"), "x"))
        else V(d["site"].get("nome"), "nome do site avaliado"),
        negrito=True, tamanho=13, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.5)
    for _ in range(6):
        par(doc, "", espacamento=1.5)
    for nome in eq:
        par(doc, nome, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.5)
    for _ in range(5):
        par(doc, "", espacamento=1.5)
    par(doc, ins["cidade"], alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)
    par(doc, ins["data"], alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)
    if d.get("demonstracao"):
        par(doc, "", espacamento=1.0)
        par(doc, "DOCUMENTO DE DEMONSTRAÇÃO - os dados abaixo provêm de um portal "
                 "fictício servido localmente, criado apenas para exercitar as ferramentas. "
                 "Não se trata da avaliação de um site real.",
            negrito=True, tamanho=10, alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
            espacamento=1.0, cor=RGBColor(0xB7, 0x1C, 0x1C))
    doc.add_page_break()


def folha_rosto(doc, d):
    ins, eq = d["instituicao"], d["equipe"]
    inserir_logo(doc)
    for linha in (ins["nome"], ins["campus"], ins["curso"]):
        par(doc, linha, negrito=True, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)
    for _ in range(4):
        par(doc, "", espacamento=1.5)
    for nome in eq:
        par(doc, nome, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.5)
    for _ in range(3):
        par(doc, "", espacamento=1.5)
    par(doc, "RELATÓRIO DE AVALIAÇÃO DE ACESSIBILIDADE WEB",
        negrito=True, tamanho=13, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
    nome_site = V(d["site"].get("nome"), "nome do site avaliado")
    par(doc, nome_site.upper() if not tem_marcador(nome_site) else nome_site,
        negrito=True, tamanho=13, alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(3):
        par(doc, "", espacamento=1.5)
    # No modelo, a natureza do trabalho ocupa a largura da mancha, justificada,
    # em 12 pt com 12 pt de espaço antes e depois.
    par(doc, "Relatório de Avaliação apresentado como requisito integrante à nota da "
             f"disciplina de {ins['disciplina']} do "
             f"{ins.get('curso_nominal') or ins['curso'].title()}.",
        alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, espaco_antes=12, espaco_depois=12)
    for _ in range(6):
        par(doc, "", espacamento=1.5)
    par(doc, ins["cidade"], alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)
    par(doc, ins["data"], alinhamento=WD_ALIGN_PARAGRAPH.CENTER, espacamento=1.0)


SUMARIO = [
    ("1", "INTRODUÇÃO"), ("2", "OBJETIVO"), ("2.1", "Objetivo geral"),
    ("2.2", "Objetivos específicos"), ("3", "METODOLOGIA"),
    ("3.1", "Site avaliado e justificativa da escolha"),
    ("3.2", "Etapas da avaliação"), ("3.3", "Instrumentos utilizados"),
    ("4", "AVALIAÇÃO E RESULTADOS"),
    ("4.1", "Resultados da inspeção manual (checklist de 15 itens)"),
    ("4.2", "Resultados do avaliador automático WAVE"),
    ("4.3", "Resultados do avaliador automático ASES"),
    ("4.4", "Resultados do avaliador automático axe-core"),
    ("4.5", "Medição de contraste por amostragem de pixels"),
    ("4.6", "Evidências visuais da avaliação"),
    ("4.7", "Recurso de tradução para Libras (VLibras)"),
    ("4.8", "Resultados da auditoria programática do código-fonte"),
    ("4.9", "Simulação automatizada de acesso por smartphone"),
    ("4.10", "Tarefa complementar: uso real com leitor de tela"),
    ("4.11", "Análise do nível de conformidade WCAG"),
    ("5", "RECOMENDAÇÕES DE CORREÇÃO"), ("6", "CONCLUSÃO"), ("7", "REFERÊNCIAS"),
]


ALTURA_MAX_FIGURA_CM = 19.0   # sobra espaço para título, fonte e um parágrafo
_QUADROS = {"n": 0}
_FIGURAS_N = {"n": 0}


def _nao_separar(paragrafo):
    """Prende o parágrafo ao seguinte (w:keepNext).

    Sem isto, o Word quebra a página entre o título da figura e a imagem, que
    foi o que aconteceu com as Figuras 3, 4 e 5.
    """
    pPr = paragrafo._p.get_or_add_pPr()
    for nome in ("w:keepNext", "w:keepLines"):
        el = OxmlElement(nome)
        el.set(qn("w:val"), "true")
        pPr.append(el)


def figura(doc, caminho, texto, fonte="Fonte: os autores."):
    """Figura no padrão ABNT: título acima, imagem, fonte abaixo.

    Devolve o número atribuído, ou None se o arquivo não existir — assim a
    numeração nunca avança por uma figura que não entrou.
    """
    completo = os.path.join(RAIZ, caminho)
    if not os.path.exists(completo):
        return None
    # Capturas de página inteira são muito mais altas do que largas: a 15,5 cm
    # de largura, a da página de Acessibilidade passaria de 38 cm e sozinha não
    # cabe em página nenhuma — era por isso que a imagem se separava do título.
    largura, altura = Cm(15.5), None
    try:
        from PIL import Image
        with Image.open(completo) as img:
            lado = img.width / img.height
        if 15.5 / lado > ALTURA_MAX_FIGURA_CM:
            # limita pela altura; Emu aqui seria o do python-pptx, importado
            # depois neste módulo — fazer a conta em centímetros evita a troca
            altura = Cm(ALTURA_MAX_FIGURA_CM)
            largura = Cm(ALTURA_MAX_FIGURA_CM * lado)
    except Exception:
        pass

    n = _FIGURAS_N["n"] + 1
    titulo = par(doc, f"Figura {n} - {texto}", tamanho=10, espaco_depois=4,
                 espacamento=1.0, alinhamento=WD_ALIGN_PARAGRAPH.LEFT)
    _nao_separar(titulo)
    try:
        doc.add_picture(completo, width=largura, height=altura)
    except Exception:
        titulo._p.getparent().remove(titulo._p)
        return None
    imagem = doc.paragraphs[-1]
    imagem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _nao_separar(imagem)
    legenda(doc, fonte)
    _FIGURAS_N["n"] = n
    return n


def novo_quadro():
    """Número do próximo quadro.

    Era literal em cada legenda, e bastava um quadro deixar de ser emitido —
    o de contraste da simulação móvel, que só aparece quando há reprovação —
    para a sequência pular um número. Agora cada seção pede o seu na ordem em
    que escreve, e o texto do corpo usa o mesmo valor.
    """
    _QUADROS["n"] += 1
    return _QUADROS["n"]


def paginas_do_sumario():
    """Página de início de cada seção, medida no PDF da última geração.

    O arquivo é escrito por ferramenta/numerar_sumario.py, que gera o relatório,
    converte para PDF e lê em que página cada título caiu. Enquanto ele não
    existir, o sumário sai sem os números — a regra do projeto não admite
    estimar um número de página que ninguém mediu.
    """
    caminho = os.path.join(RAIZ, "dados", "paginas_sumario.json")
    if not os.path.exists(caminho):
        return {}
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f).get("paginas", {})
    except (ValueError, OSError):
        return {}


def sumario(doc):
    """Sumário no formato do modelo: título em 16 pt e itens em 12 pt negrito,
    ligados ao número da página por uma linha de pontos."""
    paginas = paginas_do_sumario()
    par(doc, "Sumário", negrito=True, tamanho=16, alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
        espaco_antes=14, espaco_depois=12)
    for num, nome in SUMARIO:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 1.5
        pf.space_after = Pt(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        recuo = Cm(0.635) if "." in num else Cm(0)
        pf.left_indent = recuo
        # Tabulação à direita da mancha (15,93 cm) com preenchimento de pontos:
        # assim toda a linha pontilhada termina rente à margem.
        pf.tab_stops.add_tab_stop(Cm(15.93) - recuo, WD_TAB_ALIGNMENT.RIGHT,
                                  WD_TAB_LEADER.DOTS)
        r = p.add_run(f"{num}. {nome}\t" + str(paginas.get(num, "")))
        r.font.name, r.font.size = FONTE, Pt(12)
        r.bold = True
    doc.add_page_break()


def secao_checklist(doc, d):
    q = novo_quadro()
    titulo_secao(doc, "4.1 Resultados da inspeção manual (checklist de 15 itens)", 2)
    corpo(doc, "A inspeção manual aplicou o checklist de 15 itens essenciais sobre as páginas "
               "do recorte, com o sítio aberto no navegador e com uso das ferramentas de "
               "desenvolvedor para leitura do código-fonte. O Quadro " + str(q) +
               " apresenta o resultado "
               "item a item, com a indicação do critério de sucesso da WCAG 2.1 e da "
               "recomendação correspondente do eMAG 3.1.")
    auto = auto_por_item(d)
    linhas = []
    for i in range(1, 16):
        item = d["_checklist"][str(i)]
        reg = (d.get("checklist_manual") or {}).get(str(i), {}) or {}
        rot, _ = rotulo_situacao(reg.get("situacao"))
        obs = reg.get("observacao")
        if not obs and str(i) in auto:
            a = auto[str(i)]
            if a["status"] in ("nao_conforme", "conforme"):
                obs = "Auditoria automática: " + a["detalhe"]
        linhas.append([
            str(i), item["nome"], f"{item['wcag']} ({item['nivel']})",
            item.get("emag", "-"), rot,
            obs or V(None, f"observação do item {i}"),
        ])
    tabela(doc, ["#", "Item verificado", "Critério WCAG 2.1 (nível)",
                 "Recomendação eMAG 3.1", "Situação", "Observação"],
           [0.72, 2.45, 2.35, 2.75, 2.15, 5.48], linhas)
    legenda(doc, f"Quadro {q} - Resultado da inspeção manual pelo checklist de 15 itens. "
                 "Fonte: elaborado pelos autores.")


def secao_wave(doc, d):
    q = novo_quadro()
    w = d.get("wave", {})
    titulo_secao(doc, "4.2 Resultados do avaliador automático WAVE", 2)
    corpo(doc, "O WAVE, desenvolvido pelo WebAIM da Utah State University, sobrepõe ícones à "
               "própria renderização da página, distinguindo erros (falhas certas de "
               "acessibilidade), alertas (situações que exigem julgamento humano) e "
               "recursos (boas práticas já aplicadas). O Quadro " + str(q) +
               " sintetiza a contagem obtida.")
    tabela(doc, ["Categoria", "Quantidade", "O que significa"], [4.29, 2.6, 9.01], [
        ["Errors", V(w.get("errors"), "n. de Errors no WAVE"),
         "Falhas certas que impedem o acesso por tecnologia assistiva."],
        ["Contrast Errors", V(w.get("contrast_errors"), "n. de Contrast Errors"),
         "Textos abaixo da razão mínima de contraste exigida (WCAG 1.4.3)."],
        ["Alerts", V(w.get("alerts"), "n. de Alerts"),
         "Ocorrências que exigem verificação manual para confirmar a falha."],
        ["Features", V(w.get("features"), "n. de Features"),
         "Recursos de acessibilidade corretamente implementados."],
        ["Structural Elements", V(w.get("structural_elements"), "n. de Structural Elements"),
         "Cabeçalhos, listas e regiões que estruturam a leitura da página."],
        ["ARIA", V(w.get("aria"), "n. de itens ARIA"),
         "Atributos ARIA presentes, que podem ajudar ou atrapalhar se mal usados."],
    ])
    legenda(doc, f"Quadro {q} - Síntese do relatório WAVE. "
                 "Fonte: WebAIM (wave.webaim.org).")
    corpo(doc, "Os erros de maior incidência relatados pela ferramenta foram: "
               + V(w.get("principais_erros"),
                   "liste os erros mais frequentes, ex.: 'Missing alternative text (12), "
                   "Empty link (7), Missing form label (3)'") + ".")
    if w.get("pontuacao_aim"):
        corpo(doc, "A ferramenta resumiu o conjunto em uma pontuação AIM de "
                   + str(w["pontuacao_aim"]) + ".")
    if w.get("observacao_atribuicao"):
        corpo(doc, "A leitura desses erros exige uma distinção que o próprio WAVE não faz. "
              + str(w["observacao_atribuicao"]))
    if w.get("observacao_landmark"):
        corpo(doc, str(w["observacao_landmark"]))
    corpo(doc, "Cabe registrar a limitação intrínseca desse tipo de ferramenta: o WAVE "
               "identifica a ausência do atributo alt, mas não avalia se o texto alternativo "
               "existente descreve adequadamente a imagem. Por isso os números deste quadro "
               "representam o piso, e não o total, dos problemas de acessibilidade do sítio.")


def secao_ases(doc, d):
    a = d.get("ases", {})
    titulo_secao(doc, "4.3 Resultados do avaliador automático ASES", 2)
    corpo(doc, "O ASES é o avaliador oficial do Governo Federal brasileiro e verifica a "
               "aderência ao eMAG 3.1, atribuindo nota de 0 a 100 e agrupando as ocorrências "
               "nas seis seções do modelo. A nota geral obtida pelo sítio avaliado foi de "
               + V(a.get("nota_geral"), "nota do ASES, ex.: 78,4") + "%.")
    tabela(doc, ["Seção do eMAG", "Erros", "Avisos"], [7.95, 3.98, 3.97], [
        ["1. Marcação", V(a.get("marcacao_erros"), "erros"), V(a.get("marcacao_avisos"), "avisos")],
        ["2. Comportamento", V(a.get("comportamento_erros"), "erros"),
         V(a.get("comportamento_avisos"), "avisos")],
        ["3. Conteúdo / Informação", V(a.get("conteudo_erros"), "erros"),
         V(a.get("conteudo_avisos"), "avisos")],
        ["4. Apresentação / Design", V(a.get("apresentacao_erros"), "erros"),
         V(a.get("apresentacao_avisos"), "avisos")],
        ["5. Multimídia", V(a.get("multimidia_erros"), "erros"),
         V(a.get("multimidia_avisos"), "avisos")],
        ["6. Formulários", V(a.get("formularios_erros"), "erros"),
         V(a.get("formularios_avisos"), "avisos")],
    ])
    legenda(doc, f"Quadro {novo_quadro()} - Ocorrências por seção do eMAG 3.1 segundo o ASES. "
                 "Fonte: asesweb.governoeletronico.gov.br.")
    if a.get("total_erros") is not None:
        corpo(doc, f"O somatório alcança {a['total_erros']} erros e "
                   f"{a['total_avisos']} avisos, concentrados em duas seções.")
    if a.get("detalhamento"):
        corpo(doc, str(a["detalhamento"]))
    corpo(doc, "Dois aspectos deste resultado merecem atenção. O primeiro é a distância "
               "entre a nota e a contagem bruta: uma aderência de 90,48% convive com "
               "centenas de avisos porque o ASES pondera as ocorrências pela gravidade da "
               "recomendação violada, e a maior parte dos avisos recai sobre a "
               "recomendação 1.1, de conformidade com os padrões web, cujo peso é menor. "
               "O segundo é a convergência com as demais ferramentas: o erro registrado na "
               "recomendação 1.3, sobre níveis de cabeçalho, é a mesma falha que o WAVE "
               "relata como \"Missing first level heading\" e que a auditoria de "
               "código-fonte havia identificado como ausência de <h1>. Três instrumentos "
               "independentes apontando o mesmo defeito dão a ele uma solidez que nenhum "
               "deles teria isoladamente.")


def secao_axe(doc, d):
    a = d.get("axe") or {}
    pags = a.get("paginas") or {}
    if not pags:
        return
    titulo_secao(doc, "4.4 Resultados do avaliador automático axe-core", 2)
    corpo(doc, "O WAVE e o ASES dependem de execução interativa no navegador — o ASES, "
               "inclusive, protege o envio com CAPTCHA. Para que a etapa de avaliação "
               "automatizada não ficasse sem medição, utilizou-se o axe-core, motor de "
               "auditoria mantido pela Deque Systems e empregado, entre outras ferramentas, "
               "pela extensão Lighthouse do Google Chrome. O WAVE possui motor próprio, "
               "desenvolvido pelo WebAIM, e não se confunde com o axe-core. " + str(a.get("como_foi_executado", "")))
    linhas = []
    for url, r in pags.items():
        linhas.append([url.replace("https://www2.ifal.edu.br", ""),
                       str(r.get("passes", "-")), str(r.get("violacoes_wcag", "-")),
                       str(sum(b.get("ocorrencias", 0) for b in r.get("boas_praticas", []))),
                       str(sum(m.get("ocorrencias", 0) for m in r.get("revisao_manual", [])))])
    tabela(doc, ["Página", "Regras aprovadas", "Violações WCAG A/AA",
                 "Boas práticas", "Revisão manual"], [5.32, 2.4, 2.6, 2.2, 3.38], linhas)
    legenda(doc, f"Quadro {novo_quadro()} - Resultado do axe-core 4.10.2 por página avaliada. "
                 "Fonte: os autores.")
    corpo(doc, "O resultado exige leitura cuidadosa. O axe-core não encontrou nenhuma "
               "violação direta de Critério de Sucesso da WCAG 2.1 nos níveis A e AA nas "
               "três páginas, o que confirma que a base técnica do portal, herdada do "
               "Plone com a Identidade Digital do Governo, é sólida: idioma declarado, "
               "títulos presentes, rótulos associados e nenhum identificador duplicado.")
    bp, man = {}, {}
    for r in pags.values():
        for b in r.get("boas_praticas", []):
            bp.setdefault(b["regra"], [b["descricao"], 0])[1] += b.get("ocorrencias", 0)
        for m in r.get("revisao_manual", []):
            man.setdefault(m["regra"], [m["descricao"], 0])[1] += m.get("ocorrencias", 0)
    if bp:
        corpo(doc, "As ocorrências classificadas como boas práticas, somadas às três "
                   "páginas, foram:")
        for regra, (desc, n) in sorted(bp.items(), key=lambda x: -x[1][1]):
            item_lista(doc, f"{regra} — {n} ocorrência(s): {desc}.")
    if man:
        corpo(doc, "A ferramenta ainda devolveu ocorrências que ela própria não consegue "
                   "decidir sozinha e transfere ao avaliador humano:")
        for regra, (desc, n) in sorted(man.items(), key=lambda x: -x[1][1]):
            item_lista(doc, f"{regra} — {n} ocorrência(s): {desc}.")
    corpo(doc, "O dado mais relevante deste quadro é justamente o que a ferramenta "
               "devolveu sem resposta: a regra de contraste apareceu como indecidível "
               "dezenas de vezes porque o texto é desenhado sobre fotografias. Isso não "
               "significa aprovação — significa que o critério 1.4.3 precisou ser medido "
               "por outro caminho, descrito na subseção seguinte.")


def secao_corroboracao(doc, d):
    c = d.get("conformidade") or {}
    if c.get("corroboracao"):
        corpo(doc, str(c["corroboracao"]))
    if c.get("reconferencia_22_09"):
        par(doc, "Nota de reconferência", negrito=True,
            alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, espaco_antes=12, espaco_depois=2)
        corpo(doc, str(c["reconferencia_22_09"]))


def secao_contraste(doc, d):
    c = d.get("contraste_pixel") or {}
    if not c:
        return
    titulo_secao(doc, "4.5 Medição de contraste por amostragem de pixels", 2)
    corpo(doc, str(c.get("metodo", "")))
    reps = c.get("reprovacoes_confirmadas") or []
    if reps:
        tabela(doc, ["Elemento", "Texto", "Fundo", "Razão", "Exigido"],
               [5.52, 2.99, 2.99, 1.7, 2.7],
               [[r["elemento"], r["cor_texto"], r["cor_fundo"],
                 f"{r['razao']}:1", f"{r['exigido']}:1"] for r in reps])
        legenda(doc, f"Quadro {novo_quadro()} - Reprovações de contraste confirmadas por amostragem de "
                     "pixels na página renderizada. Fonte: os autores.")
        corpo(doc, "A reprovação mais severa é a dos botões numéricos que controlam o "
                   "banner rotativo: com 1,66:1, o texto azul sobre o verde institucional "
                   "fica praticamente indistinguível do fundo. São, ao mesmo tempo, os "
                   "únicos controles do banner e alvos de apenas 22 por 20 pixels, o que "
                   "os faz falhar também no critério 2.5.8 Tamanho do alvo (mínimo) — critério "
                   "da WCAG 2.2, aqui adotado como complemento.")
    f = c.get("indicador_de_foco") or {}
    if f:
        corpo(doc, "O indicador de foco do teclado merece registro separado. Ele está "
                   f"sempre presente, na cor {f.get('cor')}, e atinge "
                   f"{f.get('sobre_verde_cabecalho')}:1 sobre o verde do cabeçalho e "
                   f"{f.get('sobre_verde_rodape')}:1 sobre o verde do rodapé. Sobre o "
                   f"fundo branco da área de conteúdo, porém, cai para "
                   f"{f.get('sobre_branco')}:1, abaixo dos {f.get('exigido_1411')}:1 "
                   "exigidos pelo critério 1.4.11. O resultado é que o foco fica nítido "
                   "nas bordas da página e quase invisível exatamente onde se concentra "
                   "a maior parte dos links.")
    if c.get("nao_mensuravel"):
        corpo(doc, "Registra-se, por honestidade metodológica, o que não foi possível "
                   "medir: " + str(c["nao_mensuravel"]))


def secao_vlibras(doc, d):
    r = ((d.get("recursos_assistivos") or {}).get("vlibras") or {})
    if not r.get("presente"):
        return
    titulo_secao(doc, "4.7 Recurso de tradução para Libras (VLibras)", 2)
    corpo(doc, "O portal disponibiliza o VLibras, tradutor automático de Português para "
               "Língua Brasileira de Sinais mantido pelo Governo Federal, por meio de um "
               "botão flutuante presente em todas as páginas. " + str(r.get("origem", "")))
    corpo(doc, "O modo como esse recurso foi identificado merece registro metodológico, "
               "por expor um limite comum a todas as frentes automatizadas empregadas. "
               + str(r.get("por_que_escapou", "")) + " O recurso só apareceu porque um dos "
               "avaliadores abriu o portal em seu próprio aparelho Android e fotografou a "
               "tela, episódio que ilustra de forma concreta a razão pela qual o W3C "
               "recomenda que a avaliação automática jamais seja empregada isoladamente.")
    figura(doc, "evidencias/telas/14-vlibras-botao-flutuante.jpg",
           "Botão flutuante do VLibras, à direita, sobre a página institucional de "
           "Acessibilidade aberta em aparelho Android. Na mesma captura aparece o link "
           "que exibe a URL completa do Decreto n. 5.296/2004 como texto visível.",
           fonte="Fonte: captura feita pelos autores em aparelho real.")
    if r.get("lacuna_documental"):
        corpo(doc, "Há, porém, uma incoerência a assinalar. " + str(r["lacuna_documental"])
              + " Um recurso de acessibilidade que o público não sabe existir tem seu "
                "alcance reduzido, e a própria página que deveria anunciá-lo é a que o "
                "omite.")
    if r.get("nao_auditado"):
        corpo(doc, "Delimita-se o alcance desta constatação: registra-se a presença do "
                   "recurso, não a sua qualidade. " + str(r["nao_auditado"]))


FIGURAS = [
    ("evidencias/telas/02-topo-barra-acessibilidade.png",
     "Barra de acessibilidade do portal. O portal declara sete teclas de acesso "
     "(accesskey): quatro atalhos de salto (Alt+1 conteúdo, Alt+2 menu, Alt+3 busca, "
     "Alt+4 rodapé) e mais três para Acessibilidade, Alto Contraste e Mapa do site."),
    ("evidencias/telas/13-carrossel-banner-rotativo.png",
     "Banner rotativo da página inicial. Os botões numéricos no canto inferior "
     "direito são os únicos controles do carrossel: medem 22 por 20 pixels, "
     "apresentam razão de contraste de 1,66:1 e sinalizam o slide em exibição "
     "apenas pela cor de fundo."),
    ("evidencias/telas/04-foco-teclado.png",
     "Indicador de foco do teclado sobre o link Acessibilidade. Sobre o verde do "
     "cabeçalho o contorno âmbar é nítido (5,81:1); sobre o branco da área de "
     "conteúdo cai para 1,56:1."),
    ("evidencias/telas/08-reflow-320px.png",
     "Página inicial renderizada em 320 pixels de largura com o script da Barra do "
     "Governo Federal bloqueado. A faixa cinza do topo é a marcação provisória "
     "\"Atualize sua Barra de Governo\", cortada à direita: é ela, e só ela, que faz "
     "o conteúdo ocupar 330 pixels. Com o script carregado o conteúdo mede 320 "
     "pixels e o critério 1.4.10 é atendido."),
    ("evidencias/telas/05-pagina-acessibilidade.png",
     "Página institucional de Acessibilidade, publicada em 2013 e modificada pela "
     "última vez em 2020. Descreve apenas três das sete teclas de acesso "
     "declaradas pelo portal e "
     "expande a sigla WCAG incorretamente."),
]


def secao_evidencias(doc, d):
    """Insere as capturas de tela como figuras numeradas, se existirem no disco."""
    disponiveis = [(c, l) for c, l in FIGURAS if os.path.exists(os.path.join(RAIZ, c))]
    if not disponiveis:
        return
    titulo_secao(doc, "4.6 Evidências visuais da avaliação", 2)
    corpo(doc, "As figuras a seguir registram o estado do portal no momento da "
               "avaliação e sustentam as medições apresentadas nas subseções "
               "anteriores. Todas foram capturadas em Chromium, sobre as folhas de "
               "estilo e as imagens do próprio sítio.")
    for caminho, texto in disponiveis:
        figura(doc, caminho, texto)


def secao_auditoria(doc, d):
    titulo_secao(doc, "4.8 Resultados da auditoria programática do código-fonte", 2)
    corpo(doc, "Como quarta frente de verificação, ao lado do WAVE, do ASES e do axe-core, "
               "desenvolveu-se um auditor próprio em "
               "Python (ferramenta/auditor_wcag.py), que percorre o HTML das páginas e "
               "verifica programaticamente os nove itens automatizáveis do checklist. Seu "
               "papel é servir de conferência cruzada aos avaliadores comerciais e permitir "
               "reexecutar a medição sempre que o sítio for atualizado.")
    paginas = d["_auto"].get("paginas", [])
    if not paginas:
        item_lista(doc, V(None, "execute 'python3 ferramenta/auditor_wcag.py <URL>' e gere "
                                "novamente este relatório para preencher o Quadro 7"))
        return
    linhas = []
    for p in paginas:
        linhas.append([p["pagina"], str(p["total_nao_conforme"]), str(p["total_conforme"]),
                       str(p["total_manual"]), str(p["total_ocorrencias"])])
    tabela(doc, ["Página auditada", "Não conf.", "Conformes", "Manual", "Ocorrências"],
           [6.96, 2.19, 2.19, 1.79, 2.77], linhas)
    legenda(doc, f"Quadro {novo_quadro()} - Síntese da auditoria programática por página. "
                 "Fonte: elaborado pelos autores.")
    pior = max(paginas, key=lambda p: p["total_ocorrencias"])
    falhas = [i for i in pior["itens"] if i["status"] == "nao_conforme"]
    if falhas:
        corpo(doc, f"A página com maior número de ocorrências foi {pior['pagina']}, "
                   f"com {pior['total_ocorrencias']} problemas somados. O detalhamento das "
                   "falhas identificadas nessa página é apresentado no Quadro 8.")
        tabela(doc, ["#", "Item", "Diagnóstico automático"], [0.89, 3.98, 11.03],
               [[str(f["item"]), f["nome"], f["detalhe"]] for f in falhas])
        legenda(doc, f"Quadro {novo_quadro()} - Falhas detectadas pela auditoria programática. "
                     "Fonte: elaborado pelos autores.")


def secao_mobile_auto(doc, d):
    titulo_secao(doc, "4.9 Simulação automatizada de acesso por smartphone", 2)
    corpo(doc, "Para tornar a avaliação mobile reproduzível e verificável, construiu-se um "
               "ambiente de teste automatizado (ferramenta/simulador_mobile.py) que emula um "
               "aparelho real em Chromium - com viewport, densidade de pixels, eventos de "
               "toque e user-agent móveis - e executa seis baterias de medição. A principal "
               "delas percorre a árvore de acessibilidade da página, que é exatamente a "
               "estrutura consumida pelo TalkBack e pelo VoiceOver, e produz a transcrição do "
               "que seria anunciado ao usuário a cada deslize.")
    e = execucao_principal(d)
    if e is None:
        item_lista(doc, V(None, "execute 'python3 ferramenta/simulador_mobile.py <URL>' e gere "
                                "novamente este relatório para preencher os Quadros 6 e 7"))
        return
    lt, fk, at = e["leitor_tela"], e["foco_teclado"], e["alvos_toque"]
    rf, zm, ct = e["reflow_320px"], e["zoom"], e["contraste"]
    q_medicoes = novo_quadro()
    _QUADROS["medicoes_mobile"] = q_medicoes
    corpo(doc, "A simulação foi executada sobre uma cópia local fiel da página "
               "inicial do portal, servida em servidor HTTP próprio porque o navegador "
               "de automação deste ambiente não estabelece a conexão TLS com o sítio, "
               f"emulando o aparelho "
               f"{e['aparelho']} em viewport de {e['viewport']['width']}x"
               f"{e['viewport']['height']} pixels lógicos. O Quadro {q_medicoes} "
               "reúne as medições.")
    d_cont = lt["deslizes_ate_conteudo"]
    tabela(doc, ["Medição", "Resultado", "Critério WCAG 2.1"], [6.36, 3.58, 5.96], [
        ["Elementos anunciados sem rótulo", str(lt["elementos_sem_rotulo"]),
         "1.1.1 / 4.1.2 (A)"],
        ["Deslizes até o conteúdo principal",
         str(d_cont) if d_cont else "conteúdo principal não identificado", "2.4.1 (A)"],
        ["Elementos focáveis sem foco visível", str(fk["sem_indicador_visivel"]), "2.4.7 (AA)"],
        ["Elementos focáveis sem nome acessível", str(fk["sem_nome_acessivel"]), "4.1.2 (A)"],
        ["Armadilha de foco", "detectada" if fk["possivel_armadilha_foco"] else "não detectada",
         "2.1.2 (A)"],
        ["Alvos de toque menores que 24x24 px", str(at["menores_que_24px_AA"]),
         "2.5.8 (AA, WCAG 2.2)"],
        ["Alvos de toque menores que 44x44 px", str(at["menores_que_44px_AAA"]), "2.5.5 (AAA)"],
        ["Rolagem horizontal em 320 px",
         "sim" if rf["rolagem_horizontal"] else "não", "1.4.10 (AA)"],
        ["Zoom bloqueado pela meta viewport",
         "sim" if zm["zoom_bloqueado"] else "não", "1.4.4 (AA)"],
        ["Trechos reprovados no contraste",
         f"{ct['reprovados']} de {ct['trechos_analisados']}", "1.4.3 (AA)"],
    ])
    legenda(doc, f"Quadro {q_medicoes} - Medições da simulação automatizada em smartphone. "
                 "Fonte: elaborado pelos autores.")
    corpo(doc, "Três linhas deste quadro pedem leitura cuidadosa, porque à primeira vista "
               "contradizem seções anteriores.")
    item_lista(doc, "Os elementos sem nome acessível e o único elemento sem foco visível não "
                    "pertencem ao código do IFAL. Conferidos na árvore de acessibilidade do "
                    "próprio navegador, são três links da Barra de Identidade do Governo "
                    "Federal — o ícone de menu, o logotipo do VLibras e o selo Acesso à "
                    "Informação — e é também o link do VLibras o que não recebe contorno de "
                    "foco. Nenhum deles existe no HTML servido pelo IFAL, o que mantém "
                    "válido o resultado do item 15 do checklist. A contagem maior que aparece "
                    "no quadro vem da heurística do próprio simulador, que procura o nome no "
                    "texto do elemento e não na árvore de acessibilidade, e por isso não "
                    "enxerga o nome que vem do atributo alt de uma imagem interna.")
    item_lista(doc, "O contraste desta bateria aparece sem reprovação alguma, em aparente "
                    "conflito com as três reprovações da seção 4.5. A explicação é simples e "
                    "vale como limitação registrada: a bateria descarta trechos com menos de "
                    "dois caracteres, e os controles do banner rotativo — onde estão as duas "
                    "piores razões medidas — são dígitos isolados, de 1 a 4. Eles nunca "
                    "entram nesta amostra. Quem os mede é a amostragem de pixels da seção "
                    "4.5, e é ela que vale.")
    trans = lt["transcricao"][:12]
    if trans:
        q_transcricao = novo_quadro()
        corpo(doc, f"O Quadro {q_transcricao} reproduz os primeiros anúncios que o leitor "
                   "de tela emitiria ao "
                   "percorrer a página, permitindo verificar como a estrutura do código se "
                   "converte em experiência sonora.")
        tabela(doc, ["Deslize", "Anúncio do leitor de tela"], [2.19, 13.71],
               [[str(i), t] for i, t in enumerate(trans, 1)])
        legenda(doc, f"Quadro {q_transcricao} - Transcrição dos anúncios do leitor de tela. "
                     "Fonte: elaborado pelos autores.")
    if ct["exemplos"]:
        corpo(doc, "Quanto ao contraste, esta bateria calcula a razão supondo o fundo "
                   "pela subida da árvore do DOM, método que não resolve o fundo quando "
                   "o texto é desenhado sobre um irmão posicionado ou sobre imagem: por "
                   "isso ela classifica "
                   f"{ct.get('indeterminados', 0)} trecho(s) como indeterminados, que "
                   "exigem conferência visual. A medição de contraste que vale para "
                   "este relatório é a da seção 4.5, feita por amostragem dos pixels "
                   "efetivamente pintados na tela; os números abaixo servem apenas de "
                   "triagem. O pior resultado confiável desta triagem foi "
                   f"{ct['pior_razao']}:1.")
        tabela(doc, ["Trecho de texto", "Razão obtida", "Razão exigida"], [8.94, 3.48, 3.48],
               [[x["texto"], f"{x['razao']}:1", f"{x['exigido']}:1"] for x in ct["exemplos"][:6]])
        legenda(doc, f"Quadro {novo_quadro()} - Trechos reprovados no critério de contraste. "
                     "Fonte: elaborado pelos autores.")


def secao_mobile_real(doc, d):
    m = d.get("mobile", {})
    titulo_secao(doc, "4.10 Tarefa complementar: uso real com leitor de tela", 2)
    corpo(doc, "A simulação automatizada mede o que a máquina consegue medir; a experiência "
               "de uso, porém, só se revela no uso. Por isso a avaliação foi complementada "
               "com um teste presencial: um dos autores acessou o sítio pelo próprio "
               "smartphone, com o leitor de tela ativado e a tela desligada do seu campo de "
               "visão, e tentou executar uma tarefa real de ponta a ponta.")
    tabela(doc, ["Parâmetro do teste", "Registro"], [5.96, 9.94], [
        ["Aparelho utilizado", V(m.get("dispositivo"), "modelo do aparelho")],
        ["Sistema operacional", V(m.get("sistema"), "ex.: Android 14 / iOS 17")],
        ["Leitor de tela", V(m.get("leitor_tela"), "TalkBack ou VoiceOver")],
        ["Tarefa proposta", m.get("tarefa_testada") or V(None, "descreva a tarefa")],
        ["Tempo gasto", V(m.get("tempo_gasto"), "ex.: 6 min 40 s")],
        ["Tarefa concluída", V(m.get("tarefa_concluida"), "Sim / Não / Parcialmente")],
    ])
    legenda(doc, f"Quadro {novo_quadro()} - Condições do teste com leitor de tela. "
                 "Fonte: elaborado pelos autores.")
    corpo(doc, "Relato da experiência: " + V(m.get("relato"),
          "descreva em 8 a 12 linhas: como foi ativar o leitor, o que o aparelho anunciou "
          "ao abrir a página, onde a navegação travou, quais elementos foram anunciados como "
          "'botão sem rótulo' ou 'imagem', se foi possível concluir a tarefa e qual a "
          "sensação ao depender apenas do áudio"))
    corpo(doc, "A confrontação entre este relato e as medições automatizadas da seção "
               "anterior é o ponto central da avaliação: cada elemento anunciado sem rótulo "
               f"contado no Quadro {_QUADROS.get('medicoes_mobile', '-')} corresponde, na "
               "experiência real, a um momento de interrupção em que o usuário precisa "
               "adivinhar a função do que está tocando.")
    corpo(doc, "Cabe separar, no relato acima, o que é do portal e o que é da tecnologia "
               "assistiva. " + str(m.get("leitura_critica", "")))


def secao_recomendacoes(doc, d):
    titulo_secao(doc, "5. RECOMENDAÇÕES DE CORREÇÃO")
    corpo(doc, "As recomendações a seguir estão ordenadas por severidade, considerando o "
               "impacto sobre o usuário e o nível WCAG afetado. Problemas de severidade "
               "crítica bloqueiam integralmente o acesso de determinados grupos e devem ser "
               "corrigidos com prioridade. A severidade não coincide com o nível WCAG: as "
               "duas recomendações críticas tratam das falhas de Nível A do banner rotativo, "
               "que nenhum avaliador automático detectou e que bastam para impedir a "
               "declaração de conformidade, mas há também uma falha de Nível A entre as "
               "recomendações de severidade alta — a ausência de cabeçalhos na página de "
               "contato (1.3.1) —, classificada assim por afetar uma página do recorte, e "
               "não todas.")
    tabela(doc, ["Severidade", "Problema", "Correção recomendada", "Critério"],
           [2.19, 3.58, 7.55, 2.58],
           [[s, p, c, cr] for s, p, c, cr in T.RECOMENDACOES])
    legenda(doc, f"Quadro {novo_quadro()} - Recomendações de correção priorizadas. "
                 "Fonte: elaborado pelos autores.")
    corpo(doc, "Estima-se que as correções de severidade crítica e alta sejam implementáveis "
               "sem redesenho visual do sítio, uma vez que dizem respeito à camada de "
               "marcação semântica do HTML e a ajustes pontuais de paleta, e não a "
               "arquitetura da aplicação.")


def gerar_docx(d):
    doc = Document()
    estilo_base(doc)
    capa(doc, d)
    folha_rosto(doc, d)
    # Capa e folha de rosto ficam sem rodapé: a numeração começa no sumário.
    corpo_doc = doc.add_section(WD_SECTION.NEW_PAGE)
    corpo_doc.page_width, corpo_doc.page_height = Cm(21.01), Cm(29.69)
    corpo_doc.left_margin = corpo_doc.right_margin = Cm(2.54)
    corpo_doc.top_margin = corpo_doc.bottom_margin = Cm(2.54)
    numerar_paginas(corpo_doc)
    sumario(doc)

    titulo_secao(doc, "1. INTRODUÇÃO")
    for p in T.introducao(d):
        corpo(doc, p)

    titulo_secao(doc, "2. OBJETIVO")
    titulo_secao(doc, "2.1 Objetivo geral", 2)
    corpo(doc, T.objetivo_geral(d))
    titulo_secao(doc, "2.2 Objetivos específicos", 2)
    for o in T.OBJETIVOS_ESPECIFICOS:
        item_lista(doc, o)

    titulo_secao(doc, "3. METODOLOGIA")
    titulo_secao(doc, "3.1 Site avaliado e justificativa da escolha", 2)
    corpo(doc, "O sítio selecionado para a avaliação foi o "
               + V(d["site"].get("nome"), "nome do site") + ", acessível em "
               + V(d["site"].get("url"), "URL") + ", mantido pelo "
               + V(d["site"].get("responsavel"), "instituicao responsavel") + ".")
    corpo(doc, V(d["site"].get("justificativa"), "justificativa da escolha do site"))
    titulo_secao(doc, "3.2 Etapas da avaliação", 2)
    for p in T.metodologia(d):
        corpo(doc, p)
    titulo_secao(doc, "3.3 Instrumentos utilizados", 2)
    tabela(doc, ["Instrumento", "Natureza", "Finalidade na avaliação"], [3.99, 3.19, 8.72], [
        ["Checklist de 15 itens", "Manual",
         "Verificação guiada dos requisitos essenciais, com julgamento humano."],
        ["WAVE (WebAIM)", "Automática",
         "Detecção de erros sobre a página renderizada e contagem por categoria."],
        ["ASES (Governo Federal)", "Automática",
         "Nota de aderência ao eMAG 3.1 e ocorrências por seção do modelo."],
        ["axe-core 4.10.2 (Deque)", "Automática",
         "Verificação das regras WCAG 2.1 sobre a página já renderizada."],
        ["Amostragem de pixels", "Automática (própria)",
         "Contraste medido na imagem da tela, sem supor a cor do fundo."],
        ["auditor_wcag.py", "Automática (própria)",
         "Conferência cruzada dos itens automatizáveis diretamente no HTML."],
        ["simulador_mobile.py", "Automática (própria)",
         "Emulação de smartphone, árvore de acessibilidade, alvos de toque e contraste."],
        ["Leitor de tela em smartphone", "Empírica",
         "Execução de tarefa real sem apoio visual, para avaliar a experiência de uso."],
    ])
    legenda(doc, f"Quadro {novo_quadro()} - Instrumentos empregados na avaliação. "
                 "Fonte: elaborado pelos autores.")

    titulo_secao(doc, "4. AVALIAÇÃO E RESULTADOS")
    corpo(doc, "Esta seção apresenta os resultados obtidos em cada frente de avaliação, "
               "partindo da inspeção humana, passando pelas medições automatizadas e "
               "encerrando na análise consolidada de conformidade.")
    secao_checklist(doc, d)
    secao_wave(doc, d)
    secao_ases(doc, d)
    secao_axe(doc, d)
    secao_contraste(doc, d)
    secao_evidencias(doc, d)
    secao_vlibras(doc, d)
    secao_auditoria(doc, d)
    secao_mobile_auto(doc, d)
    secao_mobile_real(doc, d)

    titulo_secao(doc, "4.11 Análise do nível de conformidade WCAG", 2)
    for p in T.analise_conformidade(d):
        corpo(doc, p)
    secao_corroboracao(doc, d)

    secao_recomendacoes(doc, d)

    titulo_secao(doc, "6. CONCLUSÃO")
    for p in T.conclusao(d):
        corpo(doc, p)

    titulo_secao(doc, "7. REFERÊNCIAS")
    data = d["instituicao"].get("data_acesso", "")
    for ref in T.REFERENCIAS:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(ref.replace("\x02DATA\x02", data))
        r.font.name, r.font.size = FONTE, Pt(12)

    os.makedirs(os.path.dirname(SAIDA_DOCX), exist_ok=True)
    doc.save(SAIDA_DOCX)
    return SAIDA_DOCX


# --------------------------------------------------------------- PPTX
AZUL = PPTColor(0x1F, 0x3B, 0x63)
VERM = PPTColor(0xC0, 0x1C, 0x1C)
CINZA = PPTColor(0x44, 0x44, 0x44)


RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def limpar_slides(prs):
    """Remove os slides do modelo, preservando tema, mestre e layouts.

    Não basta retirar a entrada de sldIdLst: e preciso descartar também a
    relacao correspondente, senao a parte antiga continua sendo gravada no
    arquivo final e o pacote sai com slides duplicados.
    """
    ids = prs.slides._sldIdLst
    for s in list(ids):
        prs.part.drop_rel(s.get(RID))
        ids.remove(s)


def layout(prs, nome):
    for l in prs.slide_layouts:
        if l.name == nome:
            return l
    return prs.slide_layouts[1]


def escrever(tf, linhas, tamanho=18, espaco=6):
    """linhas: lista de (texto, nivel) ou str."""
    tf.word_wrap = True
    primeiro = True
    for linha in linhas:
        texto, nivel = linha if isinstance(linha, tuple) else (linha, 0)
        p = tf.paragraphs[0] if primeiro else tf.add_paragraph()
        primeiro = False
        p.level = nivel
        p.space_after = PPt(espaco)
        for conteudo, marcador in segmentos(str(texto)):
            if not conteudo:
                continue
            r = p.add_run()
            r.text = conteudo
            r.font.size = PPt(tamanho if nivel == 0 else max(tamanho - 3, 12))
            r.font.name = "Arial"
            if marcador:
                r.font.color.rgb = VERM
                r.font.bold = True


def slide_titulo(prs, titulo, subtitulo):
    s = prs.slides.add_slide(layout(prs, "Slide de Título") if
                             any(l.name == "Slide de Título" for l in prs.slide_layouts)
                             else layout(prs, "Slide de Título"))
    if s.shapes.title:
        s.shapes.title.text_frame.text = titulo
    for ph in s.placeholders:
        if ph.placeholder_format.idx == 1:
            escrever(ph.text_frame, [subtitulo], tamanho=20)
    return s


def slide_conteudo(prs, titulo, linhas, tamanho=18):
    s = prs.slides.add_slide(layout(prs, "Título e Conteúdo"))
    if s.shapes.title:
        tf = s.shapes.title.text_frame
        tf.text = ""
        escrever(tf, [titulo], tamanho=28, espaco=0)
    corpo_ph = None
    for ph in s.placeholders:
        if ph.placeholder_format.idx != 0:
            corpo_ph = ph
            break
    if corpo_ph is not None:
        escrever(corpo_ph.text_frame, linhas, tamanho=tamanho)
    return s


def slide_imagem(prs, titulo, caminho, nota=""):
    """Slide com uma captura de tela ocupando a área de conteúdo."""
    completo = os.path.join(RAIZ, caminho)
    if not os.path.exists(completo):
        return None
    s = prs.slides.add_slide(layout(prs, "Título e Conteúdo"))
    if s.shapes.title:
        tf = s.shapes.title.text_frame
        tf.text = ""
        escrever(tf, [titulo], tamanho=26, espaco=0)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)

    from PIL import Image as _Img
    with _Img.open(completo) as im:
        prop = im.height / im.width

    # A imagem começa abaixo do título e reserva o rodapé da área de conteúdo
    # para a legenda. Sem isso a figura sobe e cobre o título do slide.
    base_titulo = (s.shapes.title.top + s.shapes.title.height) if s.shapes.title \
        else Inches(2.3)
    topo = int(base_titulo) + Inches(0.12)
    altura_legenda = Inches(0.95) if nota else Inches(0.15)
    alt_max = int(prs.slide_height - topo - altura_legenda - Inches(0.15))
    larg_max = int(prs.slide_width * 0.80)

    larg = larg_max
    alt = int(larg * prop)
    if alt > alt_max:
        alt = alt_max
        larg = int(alt / prop)
    s.shapes.add_picture(completo, Emu(int((prs.slide_width - larg) / 2)), Emu(int(topo)),
                         width=Emu(larg), height=Emu(alt))
    if nota:
        cx = Emu(int(prs.slide_width * 0.08))
        cy = Emu(int(topo + alt + Inches(0.10)))
        cw = Emu(int(prs.slide_width * 0.84))
        cxn = s.shapes.add_textbox(cx, cy, cw, Emu(int(altura_legenda)))
        cxn.text_frame.word_wrap = True
        escrever(cxn.text_frame, [nota], tamanho=13)
    return s


def gerar_pptx(d):
    prs = Presentation(MODELO_PPTX) if os.path.exists(MODELO_PPTX) else Presentation()
    if os.path.exists(MODELO_PPTX):
        limpar_slides(prs)
    else:
        prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

    site = d["site"]
    ins = d["instituicao"]
    auto = auto_por_item(d)
    e = execucao_principal(d)
    w, a, m, c = d.get("wave", {}), d.get("ases", {}), d.get("mobile", {}), d.get("conformidade", {})

    # 1 capa
    selo = ("\n[DEMONSTRAÇÃO - portal fictício local, não é um site real]"
            if d.get("demonstracao") else "")
    slide_titulo(prs,
                 "Avaliação de Acessibilidade Web com as Diretrizes WCAG 2.1",
                 limpo(V(site.get("nome"), "site avaliado")) + "\n"
                 + " · ".join(d["equipe"]) + "\n"
                 + f"{ins.get('curso_nominal') or ins['curso']} — {ins['disciplina']} — {ins['data']}"
                 + selo)

    # 2 o que é
    slide_conteudo(prs, "O que são as WCAG?", [
        "Web Content Accessibility Guidelines — recomendação do W3C, versão 2.1 (2018)",
        "Organizadas em 4 princípios (POUR):", 
        ("Perceptível — a informação precisa chegar aos sentidos do usuário", 1),
        ("Operável — a interface precisa ser utilizável por qualquer forma de entrada", 1),
        ("Compreensível — conteúdo e operação precisam ser previsíveis", 1),
        ("Robusto — o código precisa funcionar com tecnologias assistivas", 1),
        "78 critérios de sucesso distribuídos em 3 níveis: A, AA e AAA",
        "No Brasil: eMAG 3.1 (2014) adapta as WCAG ao governo eletrônico",
    ], tamanho=17)

    # 3 por que importa
    slide_conteudo(prs, "Por que avaliar acessibilidade?", [
        "14,4 milhões de brasileiros com deficiência (Censo IBGE 2022)",
        "Exigência legal, não apenas boa prática:",
        ("Decreto nº 5.296/2004 — portais da administração pública", 1),
        ("Lei Brasileira de Inclusão nº 13.146/2015, art. 63 — sites em geral", 1),
        "Acessibilidade beneficia todos: legendas, contraste e navegação por teclado",
        ("melhoram a experiência de qualquer usuário em qualquer contexto", 1),
    ], tamanho=18)

    # 4 site escolhido
    slide_conteudo(prs, "Site avaliado", [
        V(site.get("nome"), "nome do site"),
        (V(site.get("url"), "URL do site"), 1),
        "Por que este site:",
        (limpo(V(site.get("justificativa"), "justificativa"))[:400], 1),
    ], tamanho=17)

    # 5 metodologia
    slide_conteudo(prs, "Metodologia em 4 etapas", [
        "1. Inspeção manual — checklist de 15 itens mapeados à WCAG 2.1 e ao eMAG 3.1",
        "2. Avaliação automatizada — WAVE, ASES e auditor próprio em Python",
        "3. Simulação mobile automatizada — Chromium emulando smartphone, árvore de",
        ("acessibilidade, alvos de toque, reflow e contraste", 1),
        "4. Teste real com leitor de tela — tarefa completa sem apoio visual",
        "Triangulação: ferramenta automática cobre só parte dos critérios;",
        ("os demais exigem julgamento humano", 1),
    ], tamanho=17)

    # 6 checklist parte 1
    def linha_item(i):
        it = d["_checklist"][str(i)]
        reg = (d.get("checklist_manual") or {}).get(str(i), {}) or {}
        rot, _ = rotulo_situacao(reg.get("situacao"))
        if tem_marcador(rot) and str(i) in auto and auto[str(i)]["status"] in (
                "conforme", "nao_conforme"):
            rot = SITUACAO[auto[str(i)]["status"]][0] + " (auditoria automática)"
        return f"{i}. {it['nome']} — {it['wcag'].split(' ')[0]} ({it['nivel']}): {rot}"

    slide_conteudo(prs, "Checklist de 15 itens — resultados (1/2)",
                   [linha_item(i) for i in range(1, 9)], tamanho=15)
    slide_conteudo(prs, "Checklist de 15 itens — resultados (2/2)",
                   [linha_item(i) for i in range(9, 16)], tamanho=15)

    # 8 WAVE + ASES
    slide_conteudo(prs, "Avaliadores automáticos: WAVE e ASES", [
        "WAVE (WebAIM):",
        (f"Errors: {limpo(V(w.get('errors'), '?'))}   |   "
         f"Contrast Errors: {limpo(V(w.get('contrast_errors'), '?'))}   |   "
         f"Alerts: {limpo(V(w.get('alerts'), '?'))}", 1),
        ("Principais erros: " + limpo(V(w.get("principais_erros"), "listar"))[:150], 1),
        "ASES (Governo Federal — eMAG 3.1):",
        (f"Nota geral: {limpo(V(a.get('nota_geral'), '?'))}%", 1),
        (f"Marcação {limpo(V(a.get('marcacao_erros'), '?'))} erros · "
         f"Conteúdo {limpo(V(a.get('conteudo_erros'), '?'))} erros · "
         f"Formulários {limpo(V(a.get('formularios_erros'), '?'))} erros", 1),
        "Limitação: detectam ausência de alt, mas não julgam se o alt descreve bem a imagem",
        "WAVE e ASES exigem execução no navegador — o ASES protege o envio com CAPTCHA",
    ], tamanho=16)

    # 8b axe-core
    ax = (d.get("axe") or {}).get("paginas") or {}
    if ax:
        regras = {}
        manual = {}
        for r in ax.values():
            for b in r.get("boas_praticas", []):
                regras[b["regra"]] = regras.get(b["regra"], 0) + b.get("ocorrencias", 0)
            # Não usar 'm' aqui: é o dicionário do teste em aparelho real, usado
            # mais adiante no slide da tarefa complementar.
            for rv in r.get("revisao_manual", []):
                manual[rv["regra"]] = manual.get(rv["regra"], 0) + rv.get("ocorrencias", 0)
        linhas = [
            "axe-core 4.10.2 (Deque) — motor usado pelo Lighthouse",
            f"Violações diretas de critério WCAG A/AA: "
            f"{sum(r.get('violacoes_wcag', 0) for r in ax.values())} nas 3 páginas",
            (f"Regras aprovadas: "
             f"{' · '.join(str(r.get('passes')) for r in ax.values())}", 1),
            "Ocorrências de boas práticas:",
        ]
        for regra, n in sorted(regras.items(), key=lambda x: -x[1]):
            linhas.append((f"{regra} — {n}x", 1))
        if manual:
            linhas.append("Devolvido para julgamento humano:")
            for regra, n in sorted(manual.items(), key=lambda x: -x[1]):
                linhas.append((f"{regra} — {n}x", 1))
        slide_conteudo(prs, "Avaliador automático: axe-core", linhas, tamanho=15)

    # 8c contraste medido por pixel
    cp = d.get("contraste_pixel") or {}
    if cp.get("reprovacoes_confirmadas"):
        linhas = ["Método: o texto é apagado, a área é fotografada e a cor dominante "
                  "da imagem vira o fundo — sem supor nada pela árvore do DOM.",
                  "Reprovações confirmadas:"]
        for r in cp["reprovacoes_confirmadas"]:
            linhas.append((f"{r['razao']}:1 (exige {r['exigido']}:1) — {r['elemento']}", 1))
        f = cp.get("indicador_de_foco") or {}
        if f:
            linhas.append(f"Indicador de foco: {f.get('sobre_verde_cabecalho')}:1 sobre o "
                          f"verde, mas {f.get('sobre_branco')}:1 sobre o branco "
                          f"(exige {f.get('exigido_1411')}:1)")
        slide_conteudo(prs, "Contraste medido na tela renderizada", linhas, tamanho=15)

    # 8d evidências visuais
    slide_imagem(prs, "Barra de acessibilidade do portal",
                 "evidencias/telas/02-topo-barra-acessibilidade.png",
                 "Quatro atalhos de salto (Alt+1 a Alt+4), Alto Contraste e Mapa do site: "
                 "o portal acerta o essencial da navegação assistida.")
    slide_imagem(prs, "Onde estão as piores falhas: o banner rotativo",
                 "evidencias/telas/13-carrossel-banner-rotativo.png",
                 "Botões de 22x20 px, contraste de 1,66:1, slide ativo marcado só pela cor "
                 "e troca automática a cada 4 segundos sem botão de pausa.")
    slide_imagem(prs, "Reflow em 320 px",
                 "evidencias/telas/08-reflow-320px.png",
                 "Com a Barra do Governo Federal carregada, o conteúdo cabe em 320 px: "
                 "1.4.10 atendido. Os 330 px da imagem vêm da marcação provisória da "
                 "barra, visível só quando o script de terceiro falha.")

    # 8e VLibras: achado que só apareceu no aparelho real
    vl = ((d.get("recursos_assistivos") or {}).get("vlibras") or {})
    if vl.get("presente"):
        slide_imagem(prs, "O que só o aparelho real mostrou: VLibras",
                     "evidencias/telas/14-vlibras-botao-flutuante.jpg",
                     "O tradutor de Libras existe em todas as páginas, injetado por "
                     "barra.brasil.gov.br. Não aparece no HTML entregue pelo servidor e "
                     "escapou a todas as frentes automatizadas — mas a página de "
                     "Acessibilidade do portal nunca o menciona.")

    # 9 simulação mobile
    if e:
        lt, fk, at = e["leitor_tela"], e["foco_teclado"], e["alvos_toque"]
        dc = lt["deslizes_ate_conteudo"]
        slide_conteudo(prs, "Simulação automatizada em smartphone", [
            f"Aparelho emulado: {e['aparelho']} — {e['viewport']['width']}×"
            f"{e['viewport']['height']} px",
            f"Elementos anunciados SEM RÓTULO: {lt['elementos_sem_rotulo']}  (WCAG 1.1.1 / 4.1.2 — A)",
            f"Deslizes até o conteúdo principal: {dc if dc else 'conteúdo principal não identificado'}"
            "  (WCAG 2.4.1 — A)",
            f"Sem indicador de foco visível: {fk['sem_indicador_visivel']}  (WCAG 2.4.7 — AA)",
            f"Alvos de toque menores que 24×24 px: {at['menores_que_24px_AA']}  (WCAG 2.2, 2.5.8 — AA)",
            f"Rolagem horizontal em 320 px: "
            f"{'sim' if e['reflow_320px']['rolagem_horizontal'] else 'não'}  (WCAG 1.4.10 — AA)",
            f"Contraste reprovado em {e['contraste']['reprovados']} de "
            f"{e['contraste']['trechos_analisados']} trechos — pior razão "
            f"{e['contraste']['pior_razao']}:1  (WCAG 1.4.3 — AA)",
        ], tamanho=16)
        trans = lt["transcricao"][:9]
        if trans:
            slide_conteudo(prs, "O que o leitor de tela realmente anuncia",
                           [(f"{i}. {t}", 0) for i, t in enumerate(trans, 1)], tamanho=16)
    else:
        slide_conteudo(prs, "Simulação automatizada em smartphone", [
            V(None, "execute ferramenta/simulador_mobile.py e gere os documentos novamente"),
        ], tamanho=18)

    # 11 experiência real
    slide_conteudo(prs, "Tarefa complementar: uso real com leitor de tela", [
        f"Aparelho: {limpo(V(m.get('dispositivo'), 'modelo'))} — "
        f"{limpo(V(m.get('leitor_tela'), 'TalkBack / VoiceOver'))}",
        "Tarefa: " + (m.get("tarefa_testada") or limpo(V(None, "descreva a tarefa"))),
        f"Concluída: {limpo(V(m.get('tarefa_concluida'), 'Sim/Não'))} — "
        f"tempo: {limpo(V(m.get('tempo_gasto'), '?'))}",
        "Relato:",
        (limpo(V(m.get("relato"), "resuma a experiência em 3 a 4 linhas"))[:320], 1),
    ], tamanho=17)

    # 12 conformidade
    slide_conteudo(prs, "Nível de conformidade WCAG 2.1", [
        "Regra do W3C: a conformidade é integral — uma única falha de Nível A",
        ("impede a conformidade em qualquer nível", 1),
        f"Falhas em critérios de Nível A: {limpo(V(c.get('criterios_a_falhos'), '?'))}",
        f"Falhas em critérios de Nível AA: {limpo(V(c.get('criterios_aa_falhos'), '?'))}",
        "Resultado: " + limpo(V(c.get("nivel_atingido"), "Não conforme / A / AA / AAA")),
        "Nível AA é o patamar exigido da administração pública brasileira",
    ], tamanho=17)

    # 13 recomendações
    slide_conteudo(prs, "Recomendações priorizadas", [
        f"[{s}] {p} → {cr}" for s, p, _, cr in T.RECOMENDACOES[:8]
    ], tamanho=15)

    # 14 conclusão
    slide_conteudo(prs, "Conclusão", [
        "Boa aparência visual não significa boa acessibilidade:",
        ("as barreiras estão na camada de marcação, invisíveis ao usuário vidente", 1),
        "Ferramentas automáticas quantificam; só o teste humano revela a experiência",
        "A maior parte das correções é de baixo custo — atributos alt, labels,",
        ("hierarquia de cabeçalhos e elementos semânticos de região", 1),
        "Acessibilidade se projeta desde o início; corrigir depois custa mais",
        "Recomenda-se reavaliação periódica: cada publicação pode reintroduzir barreiras",
    ], tamanho=17)

    # 15 fim
    s = prs.slides.add_slide(layout(prs, "Título e Conteúdo"))
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 0:
            ph._element.getparent().remove(ph._element)
    for ph in s.placeholders:
        tf = ph.text_frame
        tf.text = ""
        escrever(tf, ["Obrigado!", ("Perguntas?", 0)], tamanho=54)
        break

    os.makedirs(os.path.dirname(SAIDA_PPTX), exist_ok=True)
    prs.save(SAIDA_PPTX)
    return SAIDA_PPTX


def contar_pendencias(d):
    """Quantos campos ainda precisam ser preenchidos."""
    n = 0

    def anda(o):
        nonlocal n
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith("_"):
                    continue
                anda(v)
        elif isinstance(o, list):
            for v in o:
                anda(v)
        elif o is None:
            n += 1
    anda({k: v for k, v in d.items() if not k.startswith("_")})
    return n


def main():
    global SAIDA_DOCX, SAIDA_PPTX
    ap = argparse.ArgumentParser(
        description="Monta o relatório (.docx) e a apresentação (.pptx)")
    ap.add_argument("--dados", default="dados_trabalho.json",
                    help="arquivo de dados dentro de dados/ (padrão: dados_trabalho.json)")
    ap.add_argument("--saida-dir", default=None,
                    help="grava os dois arquivos nesta pasta, em vez de relatorio/ e apresentacao/")
    args = ap.parse_args()

    if args.saida_dir:
        destino = os.path.join(RAIZ, args.saida_dir)
        os.makedirs(destino, exist_ok=True)
        SAIDA_DOCX = os.path.join(destino, os.path.basename(SAIDA_DOCX))
        SAIDA_PPTX = os.path.join(destino, os.path.basename(SAIDA_PPTX))

    d = preparar(args.dados)
    docx = gerar_docx(d)
    pptx = gerar_pptx(d)
    print("Documentos gerados:")
    print("  relatório    ->", os.path.relpath(docx, RAIZ))
    print("  apresentação ->", os.path.relpath(pptx, RAIZ))
    p = contar_pendencias(d)
    if p:
        print(f"\nAtenção: {p} campo(s) de dados/dados_trabalho.json ainda estão com valor null.")
        print("Eles aparecem destacados como [PREENCHER: ...] (amarelo no Word, vermelho nos slides).")
    else:
        print("\nTodos os campos preenchidos — nenhum marcador pendente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
