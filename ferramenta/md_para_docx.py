# -*- coding: utf-8 -*-
"""Renderiza PENDENCIAS.md em .docx com a mesma aparência dos entregáveis."""
import re, sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONTE = "Arial"
MONO = "Consolas"
ORIGEM, DESTINO = sys.argv[1], sys.argv[2]

doc = Document()
n = doc.styles["Normal"]
n.font.name = FONTE
n.font.size = Pt(11)
n._element.rPr.rFonts.set(qn("w:eastAsia"), FONTE)
n.paragraph_format.line_spacing = 1.3
n.paragraph_format.space_after = Pt(0)
s = doc.sections[0]
s.page_width, s.page_height = Cm(21.01), Cm(29.69)
s.left_margin = s.right_margin = Cm(2.2)
s.top_margin = s.bottom_margin = Cm(2.2)

# numero da pagina
fp = s.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = fp.add_run(); r.font.name, r.font.size = FONTE, Pt(9)
for tipo, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    el = OxmlElement("w:fldChar") if tipo else OxmlElement("w:instrText")
    if tipo: el.set(qn("w:fldCharType"), tipo)
    else:
        el.set(qn("xml:space"), "preserve"); el.text = txt
    r._r.append(el)

# A ordem importa: negrito antes de itálico, senão '**x**' casa como itálico duas vezes.
INLINE = re.compile(
    r'(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`]+`|\[[^\]]+\]\([^)]+\)|<https?://[^>]+>)')

def escrever(p, texto, tam=11, negrito=False, cor=None):
    for pedaco in INLINE.split(texto):
        if not pedaco: continue
        b, mono, ital, txt = negrito, False, False, pedaco
        if pedaco.startswith("**") and pedaco.endswith("**"):
            b, txt = True, pedaco[2:-2]
        elif pedaco.startswith("*") and pedaco.endswith("*") and len(pedaco) > 2:
            ital, txt = True, pedaco[1:-1]
        elif pedaco.startswith("`") and pedaco.endswith("`"):
            mono, txt = True, pedaco[1:-1]
        elif pedaco.startswith("<http"):
            txt = pedaco[1:-1]
        else:
            m = re.match(r'\[([^\]]+)\]\(([^)]+)\)', pedaco)
            if m: txt = m.group(1)
        run = p.add_run(txt)
        run.font.name = MONO if mono else FONTE
        run.font.size = Pt(tam - 1 if mono else tam)
        run.bold = b
        run.italic = ital
        if mono: run.font.color.rgb = RGBColor(0xA0, 0x30, 0x20)
        elif cor: run.font.color.rgb = cor

def par(texto, tam=11, negrito=False, antes=0, depois=6, recuo=0, cor=None, esp=1.3):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(antes), Pt(depois)
    pf.line_spacing = esp
    pf.left_indent = Cm(recuo)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    escrever(p, texto, tam, negrito, cor)
    return p

def sombrear(cel, cor):
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), cor)
    cel._tc.get_or_add_tcPr().append(sh)

brutas = open(ORIGEM, encoding="utf-8").read().split("\n")

# O Markdown quebra parágrafos e itens de lista em várias linhas por causa da
# largura da coluna. Sem juntar antes, um **negrito** aberto numa linha e
# fechado na seguinte não é reconhecido, e a continuação do item de lista vira
# parágrafo solto. Junta-se a quebra suave, preservando os blocos de código.
def e_bloco(l):
    t = l.strip()
    return (not t or t.startswith(("#", ">", "|", "```", "- ", "---"))
            or bool(re.match(r"^\d+\.\s", t)))

linhas, i, dentro_codigo = [], 0, False
while i < len(brutas):
    L = brutas[i]
    if L.strip().startswith("```"):
        dentro_codigo = not dentro_codigo
        linhas.append(L); i += 1; continue
    if dentro_codigo or not L.strip() or L.strip().startswith(("|", "#", "---")):
        linhas.append(L); i += 1; continue
    junto = L.rstrip()
    prefixo = ">" if L.strip().startswith("> ") else ""
    i += 1
    while i < len(brutas):
        prox = brutas[i]
        if not prox.strip() or prox.strip().startswith("```"):
            break
        if prefixo:
            # Dentro de citação, a continuação também começa com ">".
            if not prox.strip().startswith("> "):
                break
            junto += " " + prox.strip()[2:]
        else:
            if e_bloco(prox):
                break
            junto += " " + prox.strip()
        i += 1
    linhas.append(junto)

i = 0
while i < len(linhas):
    L = linhas[i]
    t = L.strip()

    if t.startswith("```"):                              # bloco de código
        i += 1; buf = []
        while i < len(linhas) and not linhas[i].strip().startswith("```"):
            buf.append(linhas[i]); i += 1
        i += 1
        tb = doc.add_table(rows=1, cols=1); tb.style = "Table Grid"
        c = tb.rows[0].cells[0]; c.text = ""
        sombrear(c, "F4F4F4")
        # O bloco para copiar não pode partir no meio entre duas páginas.
        ns = OxmlElement("w:cantSplit")
        tb.rows[0]._tr.get_or_add_trPr().append(ns)
        for k, ln in enumerate(buf):
            p = c.paragraphs[0] if k == 0 else c.add_paragraph()
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            rr = p.add_run(ln if ln.strip() else " ")
            rr.font.name, rr.font.size = MONO, Pt(9)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        continue

    if t.startswith("|") and i + 1 < len(linhas) and set(linhas[i+1].strip()) <= set("|-: "):
        cab = [x.strip() for x in t.strip("|").split("|")]
        i += 2; corpo = []
        while i < len(linhas) and linhas[i].strip().startswith("|"):
            corpo.append([x.strip() for x in linhas[i].strip().strip("|").split("|")]); i += 1
        tb = doc.add_table(rows=1, cols=len(cab)); tb.style = "Table Grid"
        tb.alignment = WD_TABLE_ALIGNMENT.CENTER
        for j, h in enumerate(cab):
            cl = tb.rows[0].cells[j]; cl.text = ""
            pp = cl.paragraphs[0]; pp.paragraph_format.space_after = Pt(2)
            escrever(pp, h, 10, negrito=True); sombrear(cl, "DDDDDD")
        for ln in corpo:
            cels = tb.add_row().cells
            for j, v in enumerate(ln[:len(cab)]):
                cels[j].text = ""
                pp = cels[j].paragraphs[0]
                pp.paragraph_format.space_after = Pt(2)
                pp.paragraph_format.line_spacing = 1.1
                escrever(pp, v, 10)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        continue

    if t.startswith("### "):   par(t[4:], 12, True, antes=10, depois=4)
    elif t.startswith("## "):  par(t[3:], 14, True, antes=14, depois=6)
    elif t.startswith("# "):   par(t[2:], 18, True, antes=0, depois=10)
    elif t == "---":
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
        pb = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "6"); bt.set(qn("w:color"), "BBBBBB")
        pb.append(bt); p._p.get_or_add_pPr().append(pb)
    elif t.startswith("> "):
        par(t[2:], 10, recuo=0.6, depois=6, cor=RGBColor(0x44, 0x44, 0x44))
    elif re.match(r'^\d+\.\s', t):
        par("    " + t, 11, recuo=0.5, depois=3)
    elif t.startswith("- "):
        par("•  " + t[2:], 11, recuo=0.5, depois=3)
    elif t == "":
        pass
    else:
        par(t, 11)
    i += 1

doc.save(DESTINO)
print("gerado:", DESTINO)
