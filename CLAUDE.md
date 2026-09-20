# Trabalho de IHC — Avaliação de acessibilidade WCAG 2.1

Equipe: **Guilherme de Oliveira Pontes Pinto** e **Kelven Eduardo Terto dos Santos**
Disciplina: Interação Humano-Computador — Bacharelado em Sistemas de Informação, IFAL Maceió.

Entregáveis: um relatório (`relatorio/*.docx`) e uma apresentação (`apresentacao/*.pptx`),
ambos gerados por script a partir de `dados/`.

## Regra que não se quebra

**Nenhum número entra nos documentos sem ter sido medido.** Campos ainda não medidos ficam
com valor `null` em `dados/dados_trabalho.json` e aparecem destacados como `[PREENCHER: ...]`
— amarelo no Word, vermelho nos slides. Nunca preencher um campo com estimativa, valor
plausível ou número inventado. Se uma ferramenta não pôde ser executada, o campo diz isso.

## Estado atual

- Texto do relatório e dos slides: **pronto** (introdução, objetivos, metodologia, análise de
  conformidade, 12 recomendações priorizadas, conclusão, referências)
- Medições do site real: **feitas** em 20/09/2026 sobre as 3 páginas avaliadas —
  auditor próprio, axe-core 4.10.2, contraste por amostragem de pixels, percurso completo
  de teclado e simulação em Pixel 7. Resultados em `dados/dados_trabalho.json`
  (blocos `checklist_manual`, `axe`, `contraste_pixel`, `conformidade`).
- Capturas de tela do site em `evidencias/telas/`, embutidas no relatório (Figuras 1 a 5)
  e nos slides 11 a 13.
- **Ainda pendentes (26 campos):** WAVE, ASES e o teste em aparelho real com
  TalkBack/VoiceOver. WAVE e ASES exigem navegador — o ASES protege o envio com CAPTCHA,
  e o WAVE recebe a URL no fragmento `#`, que não chega ao servidor.
- `demonstracao/`: exemplo completo das ferramentas rodando sobre um portal fictício local,
  com zero marcadores pendentes. **Não é a entrega.**

## Achados principais (medidos)

O portal não atinge o Nível A, por dois critérios, ambos no banner rotativo da home:
2.2.2 (troca de slide a cada 4000 ms, sem botão de pausa — confirmado lendo
`banner_rotativo.js`) e 1.4.1 (slide ativo sinalizado apenas pela cor de fundo).
Em AA falham 1.4.3, 1.4.10, 1.4.11, 1.4.12 e 2.5.8. O axe-core não encontrou nenhuma
violação direta de critério WCAG A/AA nas 3 páginas: a base Plone/IDG é sólida.

## Nota sobre a renderização no ambiente de nuvem

O Chromium desta sessão não confia na CA do proxy e não abre o site por HTTPS. As medições
que exigem renderização foram feitas sobre um **espelho local fiel** (`wget -E -H -k -p`,
servido em `127.0.0.1:8899`), com 13 folhas de estilo e 19 imagens carregadas. Só não
carregam recursos de terceiros: `barra.brasil.gov.br`, Google Tag Manager, SDK do Facebook
e o embed do YouTube. Cuidado: o `wget` converte `url(...)` de CSS para caminhos com espaço
sem aspas, o que invalida o `@import` e derruba o layout — o espelho precisa desse conserto
antes de qualquer medição de contraste ou reflow.

## Site a avaliar

Sugerido: **Portal do IFAL — Campus Maceió**, <https://www2.ifal.edu.br/campus/maceio>
(definido em `dados/dados_trabalho.json` → `site`). Se a equipe trocar, basta editar esse
bloco e regerar.

## Próximos passos, em ordem

1. Conferir que a rede alcança o site:
   `curl -sS -o /dev/null -w '%{http_code}\n' https://www2.ifal.edu.br/campus/maceio`
   Se der `000`, o ambiente ainda não libera o domínio — ver "Acesso de rede" abaixo.
2. Rodar `./ferramenta/avaliar.sh` (auditor nas 3 páginas + simulador na home).
3. Conferir, na saída do simulador, o bloco **INTEGRIDADE DA MEDIÇÃO**. Se ele avisar que
   recursos não carregaram, **contraste e reflow não valem** — liberar os domínios citados
   e rodar de novo antes de usar esses números.
4. A equipe roda WAVE (<https://wave.webaim.org/>) e ASES
   (<https://asesweb.governoeletronico.gov.br/>) no navegador e informa os números; prints
   vão para `evidencias/wave/` e `evidencias/ases/`.
5. A equipe faz a inspeção manual dos 6 itens de julgamento humano (5, 6, 8, 9, 12, 14) e a
   tarefa complementar com TalkBack/VoiceOver num aparelho real. Isso **não** pode ser
   substituído pelo simulador.
6. Preencher `dados/dados_trabalho.json` e rodar `python3 ferramenta/gerar_documentos.py`
   até ele dizer "Todos os campos preenchidos".

## Acesso de rede

Sessões em nuvem têm allowlist por ambiente. Para alcançar o site:
ícone de nuvem → editar ambiente → **Network access: Custom** → **Allowed domains** com
`www2.ifal.edu.br` e `*.ifal.edu.br`, mantendo marcado *"Also include default list of common
package managers"* (senão o pip para de funcionar). **Exige sessão nova.**

Atenção: se o site carregar CSS ou fontes de outros domínios (CDNs), eles também precisam
estar liberados, senão o simulador mede uma página sem a aparência real. O nível **Full**
evita esse problema. O passo 3 acima detecta o caso.

## Dependências

```bash
pip install python-docx python-pptx playwright
```
O Chromium já vem instalado em `/opt/pw-browsers` — **não rodar `playwright install`**.
O simulador usa esse caminho sozinho (variável `CHROMIUM_PATH` sobrescreve).

## Convenções

- Português do Brasil **com acentuação** em tudo que aparece nos documentos.
  Cuidado: acentuar strings de código pode quebrar chaves de dicionário e identificadores
  dentro de f-strings.
- Não sobrescrever `relatorio/` e `apresentacao/` com dados de teste — usar
  `--dados` e `--saida-dir`.
- `dados/resultados_automaticos.json` e `dados/resultados_mobile.json` são saídas
  transitórias e estão no `.gitignore`.
