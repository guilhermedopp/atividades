# Avaliação de Acessibilidade Web com as Diretrizes WCAG 2.1

Trabalho da disciplina de **Interação Humano-Computador** — Bacharelado em Sistemas de
Informação, IFAL Campus Maceió.

**Equipe:** Guilherme de Oliveira Pontes Pinto e Kelven Eduardo Terto dos Santos

---

## 1. Site sugerido para a avaliação

**Portal do IFAL — Campus Maceió** — <https://www2.ifal.edu.br/campus/maceio>

Por que este site é uma boa escolha:

| Critério | Por que atende |
|---|---|
| **Simples** | Poucos padrões de página (home, listagem de notícias, editais, contato), o que permite auditar o site **inteiro** dentro do prazo, em vez de amostrar um portal gigante. |
| **Público e verificável** | A professora consegue abrir e conferir cada achado do relatório. |
| **eMAG se aplica** | Sendo órgão público federal, está sujeito ao Decreto nº 5.296/2004, à LBI (Lei nº 13.146/2015) e ao eMAG 3.1 — a avaliação ganha peso jurídico, não só técnico. |
| **Rende achados reais** | Portais institucionais em CMS costumam ter imagens sem `alt`, hierarquia de cabeçalhos quebrada e campos de busca sem `label`. |
| **Relevante para a turma** | É o portal que vocês e os colegas usam — inclusive colegas com deficiência. |

### Alternativas igualmente simples

- **Portal da Prefeitura de Maceió** — <https://maceio.al.gov.br> (também sob o eMAG)
- **Site da Biblioteca do campus** ou de um **grêmio/projeto de extensão** — menores ainda
- **Site de um comércio local** — a LBI, art. 63, também alcança empresas privadas

> Se trocarem de site, basta editar `dados/dados_trabalho.json` e rodar o gerador de novo:
> os dois documentos são reconstruídos com o novo nome, URL e justificativa.

---

## 2. O que já está pronto

```
relatorio/RELATORIO_AVALIACAO_ACESSIBILIDADE_WCAG.docx   relatório completo (ABNT)
apresentacao/APRESENTACAO_AVALIACAO_ACESSIBILIDADE.pptx  15 slides
```

O **texto todo já está escrito**: introdução, objetivos, metodologia, análise de
conformidade, recomendações priorizadas, conclusão e referências. O que falta são os
**números que só a medição real produz** — eles aparecem destacados como
`[PREENCHER: ...]` (amarelo no Word, vermelho nos slides).

---

## 3. Ferramentas incluídas

Três programas que fazem a medição e preenchem os documentos sozinhos.

### 3.1 `auditor_wcag.py` — auditoria do código-fonte

Percorre o HTML e verifica os 9 itens automatizáveis do checklist. Só usa a biblioteca
padrão do Python.

```bash
python3 ferramenta/auditor_wcag.py https://www2.ifal.edu.br/campus/maceio
python3 ferramenta/auditor_wcag.py URL1 URL2 URL3          # várias páginas
python3 ferramenta/auditor_wcag.py --arquivo pagina.html --url URL   # HTML salvo, sem rede
```

### 3.2 `simulador_mobile.py` — acesso por celular com acessibilidade

Emula um smartphone real no Chromium (viewport, densidade de pixels, eventos de toque,
user-agent móvel) e roda seis baterias de teste:

| Bateria | O que mede | Critério WCAG |
|---|---|---|
| **A — Leitor de tela** | Percorre a **árvore de acessibilidade** (a mesma que TalkBack e VoiceOver consomem) e gera a transcrição do que seria anunciado a cada deslize | 1.1.1 / 4.1.2 (A) |
| **B — Foco** | Simula Tab/Shift+Tab, registra a ordem de foco, detecta foco invisível e armadilhas | 2.4.7 (AA) / 2.1.2 (A) |
| **C — Alvos de toque** | Mede os elementos interativos | 2.5.5 (AAA) / 2.5.8 (AA) |
| **D — Reflow** | Renderiza em 320 px e detecta rolagem horizontal | 1.4.10 (AA) |
| **E — Zoom** | Bloqueio de ampliação e espaçamento de texto | 1.4.4 / 1.4.12 (AA) |
| **F — Contraste** | Calcula a razão sobre a página **renderizada**, com as cores efetivas | 1.4.3 (AA) |

```bash
pip install playwright && playwright install chromium     # uma vez
python3 ferramenta/simulador_mobile.py https://www2.ifal.edu.br/campus/maceio
python3 ferramenta/simulador_mobile.py URL --aparelho iphone13    # ou pixel7, galaxya54
```

Salva capturas de tela em `evidencias/mobile/` — servem de anexo no relatório.

> O simulador **não substitui** a tarefa complementar pedida pela professora: ele mede o
> que a máquina consegue medir. Acessar o site com o TalkBack/VoiceOver ligado de verdade
> continua sendo necessário — é o que preenche a seção 4.6. O simulador dá a base
> objetiva; o teste real dá a experiência.

### 3.3 `gerar_documentos.py` — monta o relatório e os slides

```bash
pip install python-docx python-pptx    # uma vez
python3 ferramenta/gerar_documentos.py

# opcional: usar outro arquivo de dados / outra pasta de saída
python3 ferramenta/gerar_documentos.py --dados outro.json --saida-dir rascunho
```

Lê tudo de `dados/` e reescreve os dois arquivos. Ao final informa quantos campos ainda
estão pendentes.

---

## 4. Passo a passo até entregar

1. **Confirmem o site** (ou troquem em `dados/dados_trabalho.json`).
2. **Rodem as duas ferramentas** nas páginas escolhidas:
   ```bash
   python3 ferramenta/auditor_wcag.py URL1 URL2 URL3
   python3 ferramenta/simulador_mobile.py URL1
   ```
3. **Rodem o WAVE** (<https://wave.webaim.org/>) e o **ASES**
   (<https://asesweb.governoeletronico.gov.br/>). Anotem os números e **salvem prints em
   `evidencias/wave/` e `evidencias/ases/`**.
4. **Façam a inspeção manual** dos 15 itens com o site aberto — principalmente os 6 que
   exigem julgamento humano (contraste, uso de cor, teclado, foco, erros de formulário,
   conteúdo em movimento). O checklist comentado está em `dados/checklist.json`.
5. **Façam a tarefa complementar**: um de vocês acessa o site pelo celular com o leitor de
   tela ligado e tenta cumprir uma tarefa sem olhar a tela. Anotem tempo, se concluíram e
   como foi. É a parte mais valiosa do trabalho — escrevam o relato com honestidade,
   inclusive a frustração.
6. **Preencham `dados/dados_trabalho.json`** com tudo que anotaram.
7. **Rodem `gerar_documentos.py`** de novo. Quando ele disser
   *"Todos os campos preenchidos"*, acabou.

### Como ativar o leitor de tela (passo 5)

- **Android (TalkBack):** Configurações → Acessibilidade → TalkBack. Atalho: segurar os
  dois botões de volume por 3 segundos.
  Gestos: deslizar para a direita = próximo item · toque duplo = ativar · deslizar com
  dois dedos = rolar.
- **iPhone (VoiceOver):** Ajustes → Acessibilidade → VoiceOver. Atalho: três cliques no
  botão lateral.
  Gestos: deslizar para a direita = próximo item · toque duplo = ativar · três dedos =
  rolar.

---

## 5. Estrutura do repositório

```
relatorio/          relatório final (.docx)
apresentacao/       apresentação final (.pptx)
ferramenta/
  auditor_wcag.py         auditoria do HTML
  simulador_mobile.py     simulação de celular com acessibilidade
  gerar_documentos.py     montagem do .docx e do .pptx
  textos.py               textos corridos do relatório
  modelo_apresentacao.pptx  tema visual dos slides
  exemplo/portal-demo/    portal fictício de 3 páginas para testar as ferramentas
dados/
  checklist.json          os 15 itens, mapeados à WCAG 2.1 e ao eMAG 3.1
  dados_trabalho.json     >>> É AQUI QUE VOCÊS PREENCHEM <<<
demonstracao/       exemplo completo das ferramentas rodando (não é a entrega)
evidencias/         prints do WAVE, do ASES e do celular
```

### Testar as ferramentas sem depender do site

`ferramenta/exemplo/portal-demo/` é um portal fictício de três páginas com os defeitos mais
comuns de sítios institucionais (imagens sem `alt`, cabeçalhos pulando nível, campo de busca
sem `label`, contraste baixo, zoom bloqueado, tabela de largura fixa). Serve para conferir
que tudo funciona:

```bash
cd ferramenta/exemplo/portal-demo && python3 -m http.server 8777 &
cd -
python3 ferramenta/auditor_wcag.py http://localhost:8777/index.html \
        http://localhost:8777/noticias.html http://localhost:8777/contato.html
python3 ferramenta/simulador_mobile.py http://localhost:8777/index.html
```

A pasta `demonstracao/` traz o relatório e os slides gerados a partir desse portal, já sem
nenhum marcador pendente, para você ver como fica o resultado final. Veja
`demonstracao/LEIA-ME.md`.

---

## 6. Material de consulta

- [WCAG 2.1 — tradução W3C Brasil](https://www.w3c.br/traducoes/wcag/wcag21-pt-BR/)
- [WCAG 2.0 — tradução pt-BR](https://www.w3.org/Translations/WCAG20-pt-br/)
- [eMAG 3.1 — Modelo de Acessibilidade em Governo Eletrônico](https://emag.governoeletronico.gov.br/)
- [WAVE — WebAIM](https://wave.webaim.org/) · [ASES](https://asesweb.governoeletronico.gov.br/)
- [Cartilha de Acessibilidade na Web — Fascículo III](https://ceweb.br/guias/cartilha-de-acessibilidade-na-web-fasciculo-iii/)
- [Cartilha de Acessibilidade na Web — Fascículo IV](https://ceweb.br/cartilhas/cartilha-w3cbr-acessibilidade-web-fasciculo-IV/)
- [Acessibilidade para deficiência visual — Apple](https://www.apple.com/br/accessibility/vision/)
