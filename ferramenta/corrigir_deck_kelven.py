# -*- coding: utf-8 -*-
"""Aplica as correções no deck original, preservando a formatação.

Regra: nunca atribuir text_frame.text (isso colapsa o parágrafo num run sem
estilo). Reescreve-se run.text, mantendo fonte, tamanho, cor e negrito.
"""
from pptx import Presentation

ARQ_ENT, ARQ_SAI = "work.pptx", "corrigido.pptx"
pres = Presentation(ARQ_ENT)


def acha(slide, trecho):
    """Primeira forma cujo texto contém o trecho."""
    for sh in slide.shapes:
        if sh.has_text_frame and trecho in sh.text_frame.text:
            return sh
    raise SystemExit(f"NAO ACHOU {trecho!r}")


def troca_paragrafo(shape, indice, novo):
    """Substitui o texto de um parágrafo mantendo o estilo do primeiro run."""
    par = shape.text_frame.paragraphs[indice]
    if not par.runs:
        raise SystemExit(f"parágrafo {indice} sem run em {shape.shape_id}")
    par.runs[0].text = novo
    for r in par.runs[1:]:
        r.text = ""


def troca(slide, trecho, novo, indice=0):
    troca_paragrafo(acha(slide, trecho), indice, novo)


# ───────────────────────────────── slide 8 (novo): WAVE e ASES
s8 = pres.slides[7]
troca(s8, "05 · AUTOMAÇÃO", "05 · AVALIADORES OFICIAIS", 0)
troca(s8, "O que os avaliadores automáticos", "O que o WAVE e o ASES apontaram", 1)
troca(s8, "axe-core 4.10.2", "ASES · GOVERNO FEDERAL · eMAG 3.1")

cartao_ases = acha(s8, "violações diretas")
troca_paragrafo(cartao_ases, 0, "de aderência ao modelo brasileiro")
troca_paragrafo(cartao_ases, 1, "Total: 40 erros e 310 avisos")

for sh in s8.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip() == "0":
        sh.text_frame.paragraphs[0].runs[0].text = "90,48%"
        break

troca(s8, "Motor usado por extensões",
      "Marcação: 29 erros · Conteúdo: 11 erros · demais seções sem erro.")
troca(s8, "Regras aprovadas por página", "WAVE · WebAIM")

for alvo, rotulo, numero in (("Página 1", "erros", "4"),
                             ("Página 2", "contraste", "21"),
                             ("Página 3", "alertas", "32")):
    sh = acha(s8, alvo)
    troca_paragrafo(sh, 0, rotulo)
    troca_paragrafo(sh, 1, numero)

troca(s8, "LIMITAÇÃO IMPORTANTE", "ATENÇÃO NA LEITURA")
troca(s8, "WAVE e ASES exigem execução",
      "16 recursos corretos e 42 elementos estruturais. Os 4 erros vêm da Barra do "
      "Governo Federal, não do código do IFAL.")

# As caixas do slide original foram dimensionadas para o texto que tinham: a do
# número grande cabia um único caractere ("0"), e os rótulos cabiam "Página 1".
# Com texto mais largo elas quebram linha. Reposiciona e desliga a quebra.
from pptx.util import Inches

def geometria(shape, x=None, y=None, w=None, h=None, quebra=None):
    if x is not None: shape.left = Inches(x)
    if y is not None: shape.top = Inches(y)
    if w is not None: shape.width = Inches(w)
    if h is not None: shape.height = Inches(h)
    if quebra is not None: shape.text_frame.word_wrap = quebra

# cartão do ASES: número grande em cima, legenda embaixo, ocupando a largura útil
geometria(acha(s8, "90,48%"), x=1.06, y=2.30, w=3.45, h=1.05, quebra=False)
geometria(acha(s8, "de aderência ao modelo"), x=1.06, y=3.45, w=3.45, h=0.90, quebra=True)
geometria(acha(s8, "ASES · GOVERNO FEDERAL"), x=1.24, y=4.62, w=3.00, quebra=False)

# nota do cartão direito: o texto original cabia numa linha; o novo é mais longo
# e, centralizado sem quebra, transbordava para fora do cartão.
geometria(acha(s8, "16 recursos corretos"), x=5.42, y=5.05, w=6.85, h=1.20, quebra=True)

# rótulos do WAVE: "contraste" não cabe na largura feita para "Página 2".
# Busca por posição, não por texto: "erros" também aparece na nota e na legenda
# do ASES, e casar por substring desligava a quebra na caixa errada.
for x_pol in (6.14, 8.35, 10.56):
    for sh in s8.shapes:
        if sh.has_text_frame and abs(sh.left - Inches(x_pol)) < Inches(0.05) \
                and abs(sh.top - Inches(2.75)) < Inches(0.05):
            sh.text_frame.word_wrap = False
            break
    else:
        raise SystemExit(f"rótulo do WAVE não encontrado em x={x_pol}")

# ───────────────────────────────── slide 10 (era 9): contraste medido
s10 = pres.slides[9]
troca(s10, "7 / 51", "4")
troca(s10, "1:1", "1,66:1")
troca(s10, "trechos com contraste reprovado", "reprovações de contraste confirmadas")
# a caixa fora dimensionada para "1:1"; "1,66:1" quebrava em duas linhas
for sh in s10.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip() == "1,66:1":
        sh.text_frame.word_wrap = False
        break

# ───────────────────────────────── slide 14 (era 13): resíduo de caractere
s14 = pres.slides[13]
# O original trazia "≠]" — um ] digitado por engano depois do sinal. Em vez de
# só remover o ], troca-se o símbolo por palavras: o glifo U+2260 desenha mal em
# parte das fontes e o sentido fica mais claro escrito por extenso.
troca(s14, "Visual ≠] acessível", "Aparência não é acessibilidade")
troca(s14, "Automação ≠] experiência", "Automação não é experiência")

# ───────────────────────────────── renumera o rodapé de todos os slides
ajustados = 0
for n, slide in enumerate(pres.slides, 1):
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text.strip()
        # o número de página fica isolado, na borda direita do rodapé
        # 13,00 pol = 11.887.200 EMU; 6,9 pol = 6.309.360 EMU
        if t.isdigit() and sh.left > 11_500_000 and sh.top > 6_300_000:
            if t != str(n):
                sh.text_frame.paragraphs[0].runs[0].text = str(n)
                ajustados += 1
            # a caixa do número foi feita para um dígito; "10" quebrava em duas linhas
            sh.text_frame.word_wrap = False
            break

pres.save(ARQ_SAI)
print(f"salvo {ARQ_SAI} — {len(pres.slides)} slides, {ajustados} rodapé(s) renumerado(s)")
