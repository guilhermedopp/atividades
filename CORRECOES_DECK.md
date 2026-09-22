# Correções do deck — o que mudou depois da reconferência

Deck conferido: `evidencias/Apresentacao_FINAL.pdf`, 14 slides, feito no Canva.
Data da reconferência: 22/09/2026.

O arquivo que chegou é idêntico ao que já estava aqui (mesmo MD5) e é um **PDF**, não um
`.pptx` — não dá para editar preservando o design a partir dele. Duas saídas:

- **No Canva:** aplicar as trocas abaixo direto no projeto. São dez, todas de texto.
- **Aqui:** no Canva, *Compartilhar → Baixar → PPTX*, mandar esse arquivo, e eu aplico
  tudo no próprio arquivo, como já fiz da outra vez.

---

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

## Slide 1 — capa

| | |
|---|---|
| **Onde** | subtítulo, logo abaixo de "Avaliação de Acessibilidade Web" |
| **Está** | `WCAG2.1 · Portal do IFAL — Campus Maceió` |
| **Fica** | `WCAG 2.1 · Portal do IFAL — Campus Maceió` |

Falta o espaço entre "WCAG" e "2.1". Aparece certo no rodapé de todos os outros slides.

---

## Slide 5 e 6 — checklist: as pílulas coloridas

**Este é o ponto mais importante da lista**, e não é um número errado: é a mesma falha que
o trabalho denuncia.

Cada item traz uma pílula verde, amarela, vermelha ou cinza **sem texto nenhum dentro**.
Quem não distingue essas cores não sabe o resultado de item algum — é exatamente o critério
**1.4.1 Uso de cores**, que o deck acusa no banner do portal dois slides depois. O mesmo
vale para os círculos numerados, coloridos pelo mesmo código.

**Correção:** escrever a situação dentro da pílula, em texto escuro sobre o fundo colorido.
As cores ficam como estão — cor pode ser usada, só não pode ser o único meio.

| Cor da pílula | Texto a escrever dentro |
|---|---|
| verde | `Conforme` |
| amarela | `Parcial` |
| vermelha | `Não conforme` |
| cinza | `Não aplicável` |

Se não couber na largura atual, alargar a pílula ou abreviar para `Conf.` / `Parc.` /
`Não conf.` / `N/A`. Se preferir símbolo a palavra, use `+` `~` `×` `–` — o Noto Sans, que
é a fonte do deck, **não tem** os glifos ✓ e ✗, e eles sairiam de outra fonte ou como
quadrado vazio.

Vale dizer isso na apresentação: *"corrigimos no nosso próprio slide a falha que estávamos
apontando no portal."*

---

## Slide 9 — "07 · MOBILE"

O painel da esquerda inteiro fala do reflow, que não é mais falha. E a imagem dele é a
foto de outro slide, ilegível no tamanho em que está.

**Bloco de números, à direita:**

| Está | Fica |
|---|---|
| `23` alvos < 24×24 px | `23 de 58` alvos < 24×24 px |
| `4` reprovações de contraste confirmadas | `3` reprovações de contraste confirmadas |
| `1,66:1` pior razão de contraste | *(mantém)* |
| `412×915` viewport do Pixel 7 emulado | *(mantém)* |

**Painel da esquerda — trocar todo o conteúdo.** O destaque atual

> **330 px de conteúdo** / em uma tela de 320 px → rolagem horizontal

sai. O lugar é o melhor do deck para receber o que hoje não tem slide nenhum: **a tarefa
complementar**, que o enunciado pede explicitamente. Sugestão de texto:

> **TAREFA COMPLEMENTAR · TALKBACK**
> Samsung Galaxy A15 5G · Android 16
> Tarefa: encontrar o primeiro edital aberto do campus.
>
> **1ª tentativa abandonada aos 12 min 4 s.**
> 2ª concluída em 10 min 16 s.
>
> Do portal: a quantidade de elementos a percorrer até o edital e a sequência de leitura
> pouco coerente com a organização visual — 1.3.2 e 2.4.3.

Ao apresentar, **não narrar em primeira pessoa**: o teste foi executado por um integrante e
o relatório o registra como da equipe. Dizer *"a equipe executou"* e descrever o observado.

---

## Slide 11 — "09 · CONFORMIDADE"

### Coluna NÍVEL A — acrescentar uma falha

Hoje a coluna tem duas entradas e sobra espaço em branco embaixo. Falta a terceira, que já
está no checklist do slide 6 como "Não conforme" (item 2, critério 1.3.1):

> **1.3.1**  Informações e relações
> Página de contato sem cabeçalho algum

Ordem sugerida: `1.3.1`, `1.4.1`, `2.2.2`.

### Coluna NÍVEL AA — três trocas e uma remoção

| Linha | O que fazer |
|---|---|
| `1.4.3` Contraste mínimo | `4 reprovações confirmadas; pior em 1,66:1` → **`3 reprovações confirmadas; pior em 1,66:1`** |
| `1.4.10` Reflow — `330 px em tela de 320 px` | **remover a linha inteira** |
| `1.4.11` Contraste não textual | *(mantém)* |
| `1.4.12` Espaçamento de texto | `Rolagem horizontal + 3 elementos cortados` → **`3 elementos cortados`** |
| `2.5.8` Tamanho do alvo | `23 de 51 alvos < 24×24 px` → **`23 de 58 alvos < 24×24 px (WCAG 2.2)`** |

O `(WCAG 2.2)` não é detalhe: **o critério 2.5.8 não existe na WCAG 2.1**, entrou na 2.2.
O enunciado admite "WCAG 2.1 ou mais recentes", então ele vale como complemento — mas
listá-lo sem essa marca, num deck intitulado WCAG 2.1, é erro técnico. Na 2.1 o equivalente
é o **2.5.5**, de Nível AAA, que o portal também não cumpre.

### Tipografia desta tabela

Os números dos critérios saem quebrados na renderização: aparecem **`1.4. 3`**,
**`1.4.1 0`**, **`1.4.1 1`**, **`1.4.1 2`**, **`2.5. 8`**. É o espaçamento entre letras
somado à largura da caixa. Reduzir o espaçamento ou alargar a caixa até `1.4.10` caber
inteiro numa linha.

### Um erro de digitação, na coluna da esquerda

`Banner avançaacada 4s, sem pausa` → **`Banner avança a cada 4 s, sem pausa`**

---

## Slide 12 — "10 · AÇÃO"

| Está | Fica |
|---|---|
| **ALTA** · Rolagem horizontal em telas estreitas · `1.4.10 (AA)` | **MÉDIA** · Layout quebra com espaçamento de texto ampliado · `1.4.12 (AA)` |

A recomendação de reflow perdeu o objeto. O 1.4.12 é falha de AA que aparece no slide 11 e
não tinha recomendação em lugar nenhum do deck — entra no lugar e fecha a lacuna.

---

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
