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
for ARQ in relatorio/*.docx apresentacao/*.pptx; do
  [ -e "$ARQ" ] || continue
  DEST="$(dirname "$ARQ")"
  echo "convertendo $ARQ ..."
  soffice -env:UserInstallation="file://$PERFIL" --headless \
          --convert-to pdf --outdir "$DEST" "$ARQ" >/dev/null 2>&1
  PDF="${ARQ%.*}.pdf"
  [ -e "$PDF" ] && echo "  -> $PDF" || echo "  FALHOU: $ARQ" >&2
done
