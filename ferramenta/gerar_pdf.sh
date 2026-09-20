#!/usr/bin/env bash
# Converte o relatório e a apresentação para PDF, para conferir o layout.
#
# Exige libreoffice-writer e libreoffice-impress. O ambiente de nuvem costuma
# trazer só o libreoffice-core, que não lê .docx nem .pptx e falha com
# "source file could not be loaded" — nesse caso, instale antes:
#
#   apt-get update && apt-get install -y libreoffice-writer libreoffice-impress
set -uo pipefail
cd "$(dirname "$0")/.."
PERFIL="$(mktemp -d)/lo"
# O guia de pendências é Markdown: passa antes por um .docx intermediário.
if [ -f PENDENCIAS.md ]; then
  echo "convertendo PENDENCIAS.md ..."
  TMPD="$(mktemp -d)"
  python3 ferramenta/md_para_docx.py PENDENCIAS.md "$TMPD/PENDENCIAS.docx" >/dev/null &&
  soffice -env:UserInstallation="file://$PERFIL" --headless \
          --convert-to pdf --outdir "$TMPD" "$TMPD/PENDENCIAS.docx" >/dev/null 2>&1 &&
  cp "$TMPD/PENDENCIAS.pdf" PENDENCIAS.pdf && echo "  -> PENDENCIAS.pdf"
  rm -rf "$TMPD"
fi

for ARQ in relatorio/*.docx apresentacao/*.pptx; do
  [ -e "$ARQ" ] || continue
  DEST="$(dirname "$ARQ")"
  echo "convertendo $ARQ ..."
  soffice -env:UserInstallation="file://$PERFIL" --headless \
          --convert-to pdf --outdir "$DEST" "$ARQ" >/dev/null 2>&1
  PDF="${ARQ%.*}.pdf"
  [ -e "$PDF" ] && echo "  -> $PDF" || echo "  FALHOU: $ARQ" >&2
done
