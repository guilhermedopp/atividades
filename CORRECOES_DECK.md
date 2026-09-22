# Correções aplicadas no deck final

Arquivo corrigido: **`apresentacao/APRESENTACAO_FINAL_CORRIGIDA.pptx`** (PDF ao lado).
Original preservado em `evidencias/Apresentacao_FINAL_original.pptx`.
Script que aplicou tudo: `ferramenta/corrigir_deck_final.py` — roda de novo a qualquer
momento sobre o original, então nenhuma correção depende de ter sido feita à mão.

O design do Kelven está intacto: nenhuma forma foi recriada, só reescrita ou reposicionada.
São 14 slides, como antes.

## Por que os números mudaram

Duas constatações da primeira medição eram **artefato do ambiente**, não defeito do site.
A causa é a mesma nas duas: o espelho local usado para medir não carregava o
`barra.brasil.gov.br/barra.js`, e o portal exibe, enquanto esse script não chega, um bloco
de espera — `<div id="barra-brasil" style="background:#7F7F7F">` com o texto *"Atualize sua
Barra de Governo"*.

- **Reflow (1.4.10).** Esse bloco media 330 px e era o **único** elemento a ultrapassar a
  tela de 320 px. Com o `barra.js` no ar o conteúdo mede 320 px exatos. Medido nas duas
  condições, com e sem o script, e também com as fontes da barra servidas localmente.
  **O critério é atendido.**
- **Contraste (1.4.3).** O cinza `#7F7F7F` lido como "cor da Barra do Governo Federal" era
  o fundo desse mesmo bloco. A barra em operação tem texto `rgb(96,96,96)` sobre
  `rgb(241,241,241)`: **5,57:1**, aprovada. **Restam 3 reprovações**, não 4.

As outras três reprovações foram reproduzidas sem alteração (banner a 1,66:1 e 3,0:1,
"Voltar para o topo" a 4,48:1), assim como o foco a 1,56:1 e os 3 elementos cortados.

É a **terceira vez** que conteúdo de terceiro injetado em tempo de execução distorce um
resultado, depois do VLibras e da região de navegação contada pelo WAVE. Se a banca
perguntar, é uma resposta forte: o erro foi encontrado pela própria equipe, medindo de novo.

---

## O que mudou, slide a slide

| Slide | Correção |
|---|---|
| **1** capa | `WCAG2.1` → `WCAG 2.1`. A caixa foi dimensionada para o texto sem o espaço, então também se desligou a quebra de linha — senão "Maceió" caía para a segunda linha. |
| **5 e 6** checklist | Os 15 selos de situação estavam escritos **na mesma cor da pílula em que estão**: o texto existia, mas ninguém lia. Sobrava só a cor — que é a falha **1.4.1 Uso de cores**, a mesma que o deck acusa no banner do portal. Agora a palavra aparece em azul escuro sobre a pílula (9,7:1 no verde, 11,1:1 no amarelo, 6,3:1 no vermelho). De quebra, o `Parc ial` do item 1 virou `Parcial`. |
| **6** item 9 | `Indicador de focovisível` → `Indicador de foco visível`. |
| **8** contraste medido | Sai a linha `4,0:1 · Barra do Governo Federal` — esse cinza era o do bloco provisório, não o da barra. As outras quatro se redistribuem no mesmo espaço. |
| **9** mobile | `4` → `3` reprovações. `alvos < 24×24 px` → `de 58 alvos < 24×24 px`. O painel da esquerda, que era todo sobre o reflow e trazia a foto de outro slide, dá lugar à **tarefa complementar com TalkBack** — que o enunciado pede e que não tinha slide nenhum. Título do slide ajustado ao novo conteúdo. |
| **11** Nível A | Entra o **1.3.1 Informações e relações** (página de contato sem cabeçalho algum), que já constava como "Não conforme" no item 2 do checklist e não aparecia aqui. Três linhas, em ordem numérica. `Banner avançaacada 4s` → `Banner avança a cada 4 s`. |
| **11** Nível AA | Sai a linha do **1.4.10 Reflow**. `4 reprovações` → `3`. `Rolagem horizontal + 3 elementos cortados` → `3 elementos cortados`. `23 de 51` → `23 de 58`. Os números saíam quebrados (`1.4. 3`, `1.4.1 0`) porque o Canva gravou espaços literais dentro deles — agora cada um é uma caixa só, com o texto certo. No rodapé do painel, a nota de que o **2.5.8 é da WCAG 2.2**, não da 2.1. |
| **12** recomendações | `Rolagem horizontal em telas estreitas · 1.4.10 (AA)` (ALTA) → `Layout quebra com espaçamento de texto ampliado · 1.4.12 (AA)` (MÉDIA). O 1.4.12 é falha de AA que aparecia no slide 11 e não tinha recomendação em lugar nenhum. |

## O que ficou de fora, de propósito

- **A imagem do slide 8** ainda é a foto de outro slide, em baixa resolução. Trocá-la aqui
  exigiria esticar a `13-carrossel-banner-rotativo.png` (800×620) numa moldura de proporção
  2,46:1, o que distorceria. **No Canva a troca é de dois cliques** e vale a pena: a captura
  real do carrossel é evidência muito melhor.
- **Os círculos numerados** dos slides 5 e 6 continuam coloridos pelo mesmo código. Não é
  mais problema de 1.4.1: eles carregam o número e a situação agora está escrita ao lado.

## Resumo: os números certos, para conferir de uma vez

| | |
|---|---|
| Falhas de **Nível A** | **3** — 1.3.1, 1.4.1, 2.2.2 |
| Falhas de **Nível AA** | **4** — 1.4.3, 1.4.11, 1.4.12 e o 2.5.8 (WCAG 2.2) como complemento |
| Reprovações de contraste | **3** · pior **1,66:1** |
| Alvos de toque | **23 de 58** abaixo de 24×24 px |
| Reflow em 320 px | **atendido** |
| Checklist | 5 conformes · 5 parciais · 4 não conformes · 1 não aplicável *(não muda)* |
| ASES | 90,48% · 40 erros · 310 avisos *(não muda)* |
| WAVE | 4 erros · 21 de contraste · 32 alertas *(não muda)* |
| Veredito | **não atinge o Nível A** *(não muda)* |

O relatório, o guia de estudo e a cola já estão com esses números.
