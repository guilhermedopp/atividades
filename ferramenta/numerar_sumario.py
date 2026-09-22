#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preenche o sumário do relatório com o número de página de cada seção.

Ninguém consegue saber em que página um título vai cair sem paginar o
documento, então o número não pode ser estimado. Este script mede:

  1. gera o relatório;
  2. converte para PDF com o LibreOffice;
  3. lê o PDF e anota em que página cada título de seção aparece;
  4. grava dados/paginas_sumario.json e gera o relatório de novo, agora com os
     números.

A segunda geração não muda a paginação: o sumário já ocupava as mesmas linhas,
os números entram depois da tabulação. O script confere isso relendo o PDF
final e avisa se alguma seção mudou de página.

Uso:  python3 ferramenta/numerar_sumario.py
"""
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "ferramenta"))

DOCX = os.path.join(RAIZ, "relatorio", "RELATORIO_AVALIACAO_ACESSIBILIDADE_WCAG.docx")
PDF = DOCX[:-5] + ".pdf"
MAPA = os.path.join(RAIZ, "dados", "paginas_sumario.json")


def gerar():
    subprocess.run([sys.executable, os.path.join(RAIZ, "ferramenta", "gerar_documentos.py")],
                   check=True, cwd=RAIZ, stdout=subprocess.DEVNULL)


def para_pdf():
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", os.path.dirname(DOCX), DOCX],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def normaliza(s):
    """Compara títulos ignorando acento, caixa e espaço — o pdftotext quebra
    linha no meio de um título longo e come os acentos de algumas fontes."""
    import unicodedata
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def medir(secoes):
    txt = subprocess.run(["pdftotext", "-layout", PDF, "-"],
                         check=True, capture_output=True, text=True).stdout
    paginas = txt.split("\f")
    # o sumário também contém todos os títulos: começa a busca depois dele
    primeira = 0
    for i, pg in enumerate(paginas):
        if normaliza("Sumário") in normaliza(pg):
            primeira = i + 1
    achados = {}
    for num, nome in secoes:
        alvo = normaliza(f"{num}. {nome}")
        for i in range(primeira, len(paginas)):
            if alvo in normaliza(paginas[i]):
                achados[num] = i + 1   # pdftotext conta de 1
                break
    return achados, len(paginas)


def main():
    from gerar_documentos import SUMARIO

    if os.path.exists(MAPA):
        os.remove(MAPA)          # mede sempre sobre o documento sem números
    print("1/4 gerando o relatório sem números de página...")
    gerar()
    print("2/4 convertendo para PDF...")
    para_pdf()
    print("3/4 lendo em que página cada seção começa...")
    achados, total = medir(SUMARIO)
    faltando = [n for n, _ in SUMARIO if n not in achados]
    if faltando:
        print("  ATENÇÃO: não localizei no PDF as seções:", ", ".join(faltando))
        print("  Elas ficam sem número — nenhum valor é estimado.")
    with open(MAPA, "w", encoding="utf-8") as f:
        json.dump({"_leia_me": "Gerado por ferramenta/numerar_sumario.py. "
                               "Números medidos no PDF, nunca digitados.",
                   "total_de_paginas": total, "paginas": achados},
                  f, ensure_ascii=False, indent=2)
    print("4/4 gerando de novo, agora com os números...")
    gerar()
    para_pdf()
    conferencia, total2 = medir(SUMARIO)
    mudou = {n: (achados[n], conferencia[n]) for n in achados
             if n in conferencia and conferencia[n] != achados[n]}
    for num, nome in SUMARIO:
        print(f"  {num:<5} {nome[:52]:<52} {achados.get(num, '-')}")
    if mudou:
        print("\nATENÇÃO: a paginação mudou ao inserir os números:", mudou)
        print("Rode o script mais uma vez para estabilizar.")
    else:
        print(f"\nPaginação conferida: {total2} páginas, nenhuma seção mudou de lugar.")


if __name__ == "__main__":
    main()
