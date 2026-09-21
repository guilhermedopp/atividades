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
- Capturas de tela do site em `evidencias/telas/`, embutidas no relatório (Figuras 1 a 6)
  e nos slides 11 a 14.
- **Pendências: nenhuma.** A equipe entregou WAVE, ASES e o teste em aparelho real em
  21/09/2026 (`evidencias/Resultados_testes_equipe.pdf`, prints em `evidencias/wave/` e
  `evidencias/ases/`). O gerador confirma "Todos os campos preenchidos".
  WAVE: 4 erros, 21 de contraste, 32 alertas, 16 recursos, 42 elementos estruturais,
  0 ARIA, pontuação AIM 5,3/10. ASES: nota 90,48%, 40 erros e 310 avisos no total.
  Aparelho: Samsung Galaxy A15 5G, Android 16, TalkBack — tarefa concluída na 2ª tentativa.
- `demonstracao/`: exemplo completo das ferramentas rodando sobre um portal fictício local,
  com zero marcadores pendentes. **Não é a entrega.**

## VLibras: o achado que a automação perdeu

O portal **tem VLibras** em todas as páginas. Nenhuma das três frentes automatizadas viu:
o widget não está no HTML entregue pelo servidor (buscar `vlibras` nas 4 páginas retorna
zero), é injetado em tempo de execução por `barra.brasil.gov.br/barra.js`, e esse domínio
de terceiro não carrega no espelho local. Só apareceu porque um dos avaliadores abriu o
site no próprio Android e fotografou a tela (`evidencias/telas/10-...jpg`).

Lição que vale para a próxima medição: **widget injetado por script de terceiro é ponto
cego deste pipeline**. Antes de afirmar que um recurso não existe, conferir no aparelho.

Registrado em `dados/dados_trabalho.json` → `recursos_assistivos`, seção 4.7 e Figura 6 do
relatório, slide 14. O widget em si não foi auditado (contraste, alvo, teclado) porque não
carregou no ambiente de medição — fica para a inspeção presencial.

## Atribuição dos erros do WAVE (não é código do IFAL)

Os 4 erros do WAVE não pertencem ao que o IFAL entrega. A auditoria de código-fonte já
registrara 0 imagens sem alt e 0 links sem texto acessível nas 3 páginas. O
`barra.brasil.gov.br/barra.js` contém exatamente 1 imagem sem alt e 2 âncoras vazias
(`menu-icon` e o logotipo do VLibras) — explica o erro de alt e 2 dos 3 links vazios;
o terceiro não foi possível atribuir.

O mesmo vale para a região de navegação: o WAVE conta 1, mas ela vem do único `<nav>` do
`barra.js`. As 3 páginas servidas pelo IFAL têm **zero** `<nav>` e zero
`role="navigation"`. É o mesmo ponto cego do VLibras — conteúdo injetado por script de
terceiro. **Antes de atribuir um achado do WAVE ao site, conferir se ele está no HTML
servido ou na barra federal.**

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

## Conferir o layout em PDF

`./ferramenta/gerar_pdf.sh` gera os PDFs ao lado do .docx e do .pptx.

Cuidado: o ambiente de nuvem vem só com `libreoffice-core`, que não lê .docx nem
.pptx — falha com `source file could not be loaded`, inclusive com o modelo da
disciplina. Instalar antes: `apt-get update && apt-get install -y
libreoffice-writer libreoffice-impress`. Para ver as páginas como imagem,
`poppler-utils` (dá o `pdftoppm` e o `pdfinfo`).

## Convenções

- Português do Brasil **com acentuação** em tudo que aparece nos documentos.
  Cuidado: acentuar strings de código pode quebrar chaves de dicionário e identificadores
  dentro de f-strings.
- Não sobrescrever `relatorio/` e `apresentacao/` com dados de teste — usar
  `--dados` e `--saida-dir`.
- `dados/resultados_automaticos.json` e `dados/resultados_mobile.json` são saídas
  transitórias e estão no `.gitignore`.
