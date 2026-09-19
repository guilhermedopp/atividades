#!/usr/bin/env bash
# Roda a avaliação completa do site definido em dados/dados_trabalho.json.
#
#   ./ferramenta/avaliar.sh                  # usa as páginas do arquivo de dados
#   ./ferramenta/avaliar.sh URL1 URL2 ...    # usa as URLs informadas
set -uo pipefail
cd "$(dirname "$0")/.."

if [ $# -gt 0 ]; then
  PAGINAS=("$@")
else
  mapfile -t PAGINAS < <(python3 -c "
import json
d = json.load(open('dados/dados_trabalho.json', encoding='utf-8'))
print('\n'.join(d['site'].get('paginas_avaliadas') or [d['site']['url']]))")
fi

if [ ${#PAGINAS[@]} -eq 0 ]; then
  echo "Nenhuma página para avaliar. Preencha site.paginas_avaliadas em dados/dados_trabalho.json." >&2
  exit 1
fi

echo "Páginas a avaliar:"; printf '  %s\n' "${PAGINAS[@]}"; echo

echo "== Checando alcance da rede =="
CODIGO=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 "${PAGINAS[0]}" || echo 000)
if [ "$CODIGO" = "000" ]; then
  echo "FALHA: não foi possível alcançar ${PAGINAS[0]}." >&2
  echo "O ambiente provavelmente não libera esse domínio. Veja 'Acesso de rede' no CLAUDE.md." >&2
  exit 2
fi
echo "OK (HTTP $CODIGO)"; echo

echo "== 1/2  Auditoria do código-fonte =="
python3 ferramenta/auditor_wcag.py "${PAGINAS[@]}" || exit 3

echo; echo "== 2/2  Simulação em smartphone (página principal) =="
python3 ferramenta/simulador_mobile.py "${PAGINAS[0]}" --aparelho pixel7 || exit 4

echo; echo "== Gerando documentos com o que já foi medido =="
python3 ferramenta/gerar_documentos.py

cat <<'FIM'

Falta o que só pessoa faz:
  - WAVE e ASES no navegador (prints em evidencias/wave/ e evidencias/ases/)
  - inspeção manual dos itens 5, 6, 8, 9, 12 e 14
  - tarefa complementar com TalkBack/VoiceOver num aparelho real
Preencha dados/dados_trabalho.json e rode ferramenta/gerar_documentos.py de novo.
FIM
