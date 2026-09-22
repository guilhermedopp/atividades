# Guia de estudo — apresentação final

Baseado nos dois documentos entregues: o relatório de 28 páginas e o deck de 14 slides.
Serve para as duas pessoas defenderem o trabalho sem ler slide.

---

## 1. O essencial da WCAG

**WCAG** = *Web Content Accessibility Guidelines*, do W3C, versão 2.1 (2018).
Cuidado: a página de Acessibilidade do próprio IFAL expande a sigla errado, como
"World Content Accessibility Guide" — isso é um dos achados do relatório.

Quatro princípios, o **POUR** do slide 3:

| | Pergunta que responde |
|---|---|
| **P**erceptível | A informação chega aos sentidos da pessoa? |
| **O**perável | Dá para usar por qualquer forma de entrada? |
| **C**ompreensível | O conteúdo e o funcionamento são previsíveis? |
| **R**obusto | O código funciona com tecnologia assistiva? |

Dentro deles ficam os **critérios de sucesso**, cada um com nível **A** (mínimo),
**AA** (o patamar cobrado na prática) ou **AAA**.

**A regra que decide o trabalho todo:** conformidade é **integral**. Só é conforme em AA
quem cumpre 100% de A e 100% de AA. **Uma única falha de Nível A derruba tudo.** É por
isso que o portal, indo bem em quase tudo, não atinge nem o Nível A.

**eMAG 3.1** (2014) adapta a WCAG ao governo brasileiro em 6 seções — é o que o ASES mede.
**Base legal:** Decreto 5.296/2004 (portais públicos) e LBI 13.146/2015, art. 63.

---

## 2. Roteiro slide a slide

O que dizer em cada um. Os números estão todos no relatório.

| # | Slide | O que falar |
|---|---|---|
| 1 | Capa | Nome, portal avaliado, disciplina. |
| 2 | Por que importa | 14,4 milhões de brasileiros com deficiência (Censo 2022). Não é boa prática: é **obrigação legal** — Decreto 5.296 e LBI art. 63. |
| 3 | WCAG em uma visão | POUR, níveis A/AA/AAA, e **a regra da conformidade integral**. Plante aqui: uma falha de A derruba tudo. |
| 4 | Escopo | 3 páginas do portal, 4 frentes: checklist de 15 itens, avaliadores automáticos, medição própria em Python, teste real com TalkBack. Frisar: **cada frente tem ponto cego**. |
| 5 | Checklist 1/2 | 5 conformes, 5 parciais, 4 não conformes, 1 não aplicável. Não ler item por item — apontar os vermelhos. |
| 6 | Checklist 2/2 | Destacar o **14 (conteúdo em movimento), não conforme** — é o que derruba o Nível A. |
| 7 | WAVE e ASES | **90,48%** no ASES, 40 erros e 310 avisos. WAVE: 4 erros, 21 de contraste, 32 alertas. **Ponto-chave:** os 4 erros não são do IFAL, vêm da barra do governo federal. |
| 8 | Achados críticos | O banner rotativo concentra as piores falhas: botões de 22×20 px, **1,66:1**, slide ativo só pela cor, troca a cada 4 s sem pausa. |
| 9 | Mobile | 330 px de conteúdo em tela de 320 px → rolagem horizontal. 23 alvos abaixo de 24×24 px. |
| 10 | Tecnologia assistiva | **VLibras existe em todas as páginas** e nenhuma ferramenta automática viu — só apareceu no celular. E a página de Acessibilidade não menciona o recurso. |
| 11 | Conformidade | **Não atinge o Nível A.** Duas falhas de A (1.4.1 e 2.2.2), cinco de AA. |
| 12 | Recomendações | Oito, priorizadas. As duas críticas resolvem o Nível A: botão de pausa e marcador não cromático. |
| 13 | Fechamento | As quatro lições. A mais forte: **automação não é experiência**. |
| 14 | Obrigado | Abrir para perguntas. |

**Divisão sugerida:** slides 1 a 6 para quem abre (contexto e método), 7 a 14 para quem
fecha (resultados e conclusão). A virada de turno cai bem no slide 7.

---

## 3. Os achados e por que cada um é falha

Decorem o **porquê**. A banca pergunta "por que isso é um problema?".

### Nível A — as duas que derrubam tudo

**2.2.2 Pausar, Parar, Ocultar — banner sem pausa.** Troca de slide a cada 4 segundos,
indefinidamente, sem botão de pausa.
*Por quê:* conteúdo em movimento que dura mais de 5 segundos precisa de mecanismo para
pausar, parar ou ocultar. Quem lê devagar, usa leitor de tela ou tem déficit de atenção
perde o conteúdo antes de terminar.
*Como foi descoberto:* lendo o `banner_rotativo.js`. Nenhum avaliador automático testa isso.

**1.4.1 Uso de cores — slide ativo marcado só pela cor.** O botão do slide em exibição fica
âmbar, os outros verdes. Só a cor muda.
*Por quê:* a informação "você está no slide 2" depende exclusivamente de perceber cor.
*Regra prática:* cor pode ser usada, nunca sozinha — precisa vir com forma, contorno ou texto.

### Nível AA — as cinco

| Critério | O que falha | Por quê |
|---|---|---|
| **1.4.3** Contraste mínimo | botões do banner a **1,66:1** | exige 4,5:1 |
| **1.4.10** Reflow | 330 px em tela de 320 px | força rolagem nos dois eixos |
| **1.4.11** Contraste não textual | foco a **1,56:1** no branco | exige 3:1 |
| **1.4.12** Espaçamento de texto | layout quebra, corta 3 elementos | texto deve suportar ajuste |
| **2.5.8** Tamanho do alvo | 23 de 51 alvos < 24×24 px | dedo não acerta alvo pequeno |

### O que o portal acerta — digam isso também

Não é um site ruim. `lang="pt-br"` declarado, títulos únicos, **todas** as imagens com
`alt`, **todos** os campos com rótulo, quatro atalhos de salto (Alt+1 a Alt+4), indicador
de foco em **118** pontos de parada, sem armadilha de foco, e **VLibras** em todas as
páginas. Uma avaliação que só lista defeitos é uma avaliação mal feita.

---

## 4. Números de cabeceira

| | |
|---|---|
| **ASES** | nota **90,48%** · 40 erros · 310 avisos |
| **WAVE** | 4 erros · 21 de contraste · 32 alertas · 16 recursos · 42 estruturais · 0 ARIA |
| **axe-core** (só no relatório) | **0** violações WCAG A/AA nas 3 páginas |
| **Contraste** | 4 reprovações confirmadas · pior **1,66:1** |
| **Checklist** | 5 conformes · 5 parciais · 4 não conformes · 1 não aplicável |
| **TalkBack** | concluída na 2ª tentativa · **10 min 16 s** |
| **Veredito** | **não atinge o Nível A** |

---

## 5. Seis perguntas prováveis

**"Se o ASES deu 90%, o site não é acessível?"**
Não é conforme. O ASES mede aderência ao eMAG, não conformidade WCAG, e não testa 2.2.2
nem 1.4.1 — os dois critérios que derrubam o Nível A. Nota alta em avaliador automático
mede qualidade de código, não conformidade. É o achado metodológico central do trabalho.

**"Por que 90,48% e 310 avisos ao mesmo tempo?"**
O ASES pondera por gravidade. A maior parte dos avisos cai na recomendação 1.1
(conformidade com padrões web), de peso menor. Contagem bruta e nota medem coisas diferentes.

**"Os 4 erros do WAVE são do IFAL?"**
Não. A auditoria de código-fonte achou 0 imagens sem `alt` e 0 links sem texto nas três
páginas. O `barra.brasil.gov.br/barra.js`, que monta a Barra do Governo Federal em tempo de
execução, tem exatamente 1 imagem sem `alt` e 2 âncoras vazias. Isso cobre o erro de alt e
2 dos 3 links vazios. O terceiro não conseguimos atribuir — e o relatório diz isso em vez
de fingir que fechou.

**"Usaram só WAVE e ASES?"**
Não. O relatório traz também o **axe-core 4.10.2**, motor usado pelas próprias extensões
WAVE e Lighthouse: **zero violações** de critério A/AA nas três páginas. Ficou de fora do
deck por espaço, mas está na seção 4.4. Reforça o argumento: três ferramentas aprovaram um
portal que não é conforme.

**"Como acharam o VLibras se as ferramentas não acharam?"**
Abrindo o site num Android real e fotografando a tela. O widget não existe no HTML que o
servidor entrega — é injetado por script de terceiro. É a demonstração prática de que
avaliação automática isolada não basta, exatamente como o W3C recomenda.

**"O teste com TalkBack mediu o site ou a ferramenta?"**
Boa parte do tempo da primeira tentativa foi curva de aprendizado do próprio TalkBack e
navegação no sistema — e o relatório distingue isso explicitamente. O que é do portal é o
trecho final: a quantidade de elementos a percorrer até o edital e a sequência de leitura
pouco coerente com a organização visual, que remetem a 1.3.2 e 2.4.3.

---

## 6. Glossário de bolso

| Termo | O que é |
|---|---|
| **Critério de sucesso** | requisito testável da WCAG, com nível A, AA ou AAA |
| **Landmark / região** | marcação que diz ao leitor de tela o papel de um bloco (`<nav>`, `<main>`) |
| **Razão de contraste** | relação entre a luminância do texto e a do fundo; 21:1 é preto no branco |
| **Reflow** | conteúdo se reorganizar em tela estreita sem exigir rolagem horizontal |
| **Alvo (target)** | área clicável ou tocável de um controle |
| **Leitor de tela** | software que narra a interface: TalkBack no Android, VoiceOver no iOS |
| **eMAG** | modelo brasileiro de acessibilidade em governo eletrônico |
| **VLibras** | tradutor automático de Português para Libras, do governo federal |

---

## 7. O fio da apresentação

O trabalho tem uma história, e ela não é a lista de defeitos: é que **avaliadores
automáticos aprovaram um portal que não atinge o Nível A**. Os dois critérios que o
derrubam só apareceram lendo código-fonte e medindo pixel. E o recurso de acessibilidade
mais visível do site — o VLibras — só foi encontrado quando alguém pegou o celular e olhou.

Se der para segurar a tensão entre o slide 7 (nota 90,48%) e o slide 11 (não atinge o
Nível A), a defesa fica muito mais forte do que enumerar problemas em sequência.
