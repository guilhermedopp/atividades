# Guia de estudo para a apresentação

Material curto para as duas pessoas defenderem o trabalho sem ler slide. O que está aqui
é o que o relatório sustenta e o que a banca costuma perguntar.

---

## 1. O essencial da WCAG, em meia página

**WCAG** = *Web Content Accessibility Guidelines*, do W3C. Versão 2.1, de 2018.
Cuidado: a página de Acessibilidade do próprio IFAL expande a sigla errado, como
"World Content Accessibility Guide". Isso está no relatório como achado.

Organiza-se em **4 princípios (POUR)**:

| Princípio | Pergunta que ele responde |
|---|---|
| **P**erceptível | A informação chega aos sentidos da pessoa? |
| **O**perável | Dá para usar a interface por qualquer forma de entrada? |
| **C**ompreensível | O conteúdo e o funcionamento são previsíveis? |
| **R**obusto | O código funciona com tecnologia assistiva? |

Dentro dos princípios há **critérios de sucesso**, cada um com um nível: **A** (mínimo),
**AA** (o patamar exigido por lei na prática) e **AAA** (máximo).

**A regra que decide tudo:** a conformidade é **integral**. Só é conforme no nível AA quem
cumpre 100% do A e 100% do AA. **Uma única falha de Nível A derruba a conformidade em
qualquer nível.** É por isso que nosso portal, apesar de ir bem em quase tudo, não atinge
nem o Nível A.

**eMAG 3.1** é o Modelo de Acessibilidade em Governo Eletrônico, de 2014. Adapta a WCAG ao
governo brasileiro e organiza as recomendações em 6 seções (Marcação, Comportamento,
Conteúdo, Apresentação, Multimídia, Formulários). É o que o ASES mede.

**Base legal:** Decreto nº 5.296/2004 (portais públicos) e Lei Brasileira de Inclusão
(Lei nº 13.146/2015, art. 63, sites em geral).

---

## 2. O que fizemos, em quatro frentes

| Frente | Ferramenta | O que só ela pegou |
|---|---|---|
| Inspeção manual | Checklist de 15 itens | o julgamento humano dos critérios subjetivos |
| Avaliação automática | WAVE, ASES, axe-core | a contagem objetiva de erros de código |
| Medição própria | scripts Python | contraste por pixel, teclado, reflow, alvos |
| Uso real | TalkBack em Android | a experiência, que nenhuma métrica captura |

A razão de usar quatro frentes, e não uma: **cada uma tem ponto cego**. Os dois achados
que derrubam o Nível A não foram encontrados por nenhum avaliador automático.

---

## 3. Os achados — e por que cada um é falha

Decorem o **porquê**, não o número. A banca pergunta "por que isso é um problema?".

### Nível A — os dois que derrubam tudo

**2.2.2 Pausar, Parar, Ocultar — banner sem pausa**
O banner troca de slide a cada 4 segundos, indefinidamente, e não há botão de pausa.
*Por que é falha:* a WCAG exige que conteúdo em movimento que dure mais de 5 segundos
tenha mecanismo de pausar, parar ou ocultar. Quem lê devagar, quem usa leitor de tela ou
quem tem déficit de atenção perde o conteúdo antes de terminar de ler.
*Como descobrimos:* lendo o `banner_rotativo.js`. Nenhum avaliador automático testa isso.

**1.4.1 Uso de cores — slide ativo marcado só pela cor**
O botão do slide em exibição fica âmbar; os outros, verdes. Só a cor muda.
*Por que é falha:* a informação "você está no slide 2" depende exclusivamente da
percepção de cor. Quem não distingue essas cores não sabe onde está.
*Regra prática:* cor pode ser usada, mas nunca sozinha — precisa vir com forma, contorno,
ícone ou texto.

### Nível AA — os cinco

| Critério | O que falha | Por quê |
|---|---|---|
| **1.4.3** Contraste mínimo | botões do banner a **1,66:1** | exige 4,5:1 para texto normal |
| **1.4.10** Reflow | 330 px de conteúdo em tela de 320 px | força rolagem nos dois eixos |
| **1.4.11** Contraste não textual | foco a **1,56:1** no branco | exige 3:1 para o indicador |
| **1.4.12** Espaçamento de texto | layout quebra e corta 3 elementos | o texto tem de suportar ajuste |
| **2.5.8** Tamanho do alvo | 23 de 51 alvos < 24×24 px | dedo não acerta alvo pequeno |

### O que está certo no portal (digam isso também)

Não é um site ruim. Declara `lang="pt-br"`, tem títulos únicos, **todas** as imagens com
`alt`, **todos** os campos com rótulo, quatro atalhos de salto (Alt+1 a Alt+4), indicador
de foco em **118** pontos de parada, sem armadilha de foco, e **VLibras** em todas as
páginas. Uma avaliação que só lista defeitos é uma avaliação mal feita.

---

## 4. Números de cabeceira

| | |
|---|---|
| **ASES** | nota **90,48%** · 40 erros · 310 avisos |
| **WAVE** | 4 erros · 21 de contraste · 32 alertas · 16 recursos · 42 estruturais · 0 ARIA |
| **axe-core** | **0** violações WCAG A/AA nas 3 páginas |
| **Contraste** | 4 reprovações confirmadas · pior **1,66:1** |
| **Checklist** | 5 conformes · 5 parciais · 4 não conformes · 1 não aplicável |
| **TalkBack** | concluída na 2ª tentativa · **10 min 16 s** |
| **Veredito** | **não atinge o Nível A** |

---

## 5. As cinco perguntas prováveis

**"Se o ASES deu 90% e o axe-core não achou nada, o site não é acessível?"**
Não é conforme. As três ferramentas somadas não testam 2.2.2 nem 1.4.1, que são
justamente os critérios que derrubam o Nível A. Nota alta em avaliador automático mede a
qualidade do código, não a conformidade. É o achado metodológico central do trabalho.

**"Por que 90,48% no ASES e 310 avisos ao mesmo tempo?"**
O ASES pondera por gravidade. A maior parte dos avisos cai na recomendação 1.1
(conformidade com padrões web), de peso menor. Contagem bruta e nota medem coisas
diferentes.

**"Os 4 erros do WAVE são do IFAL?"**
Não. Nossa auditoria de código achou 0 imagens sem `alt` e 0 links sem texto nas três
páginas. O script `barra.brasil.gov.br/barra.js`, que monta a Barra do Governo Federal em
tempo de execução, tem exatamente 1 imagem sem `alt` e 2 âncoras vazias. Isso explica o
erro de alt e 2 dos 3 links vazios. O terceiro não conseguimos atribuir — e dizemos isso
no relatório em vez de fingir que fechou.

**"O WAVE conta 1 região de navegação. Então o site tem uma?"**
Tem uma na página, mas ela não é do campus: é o único `<nav>` da barra federal, e delimita
os links do gov.br. As três páginas servidas pelo IFAL têm **zero** `<nav>` e zero
`role="navigation"`.

**"Como acharam o VLibras se as ferramentas não acharam?"**
Abrindo o site num Android real e fotografando a tela. O widget não existe no HTML que o
servidor entrega — é injetado por script de terceiro. É a demonstração prática de que
avaliação automática isolada não basta, que é o que o W3C recomenda.

---

## 6. Três coisas para corrigir nos slides antes de apresentar

Conferidas contra o relatório.

**1. Slide 9 contradiz o slide 8.** O slide 9 mostra "7 / 51 trechos com contraste
reprovado" e "1:1 pior razão". Esses eram números de uma versão antiga do simulador, que
calculava o fundo subindo a árvore do DOM e lia texto branco sobre cabeçalho verde como
branco-no-branco. **Eram falsos positivos.** A medição por amostragem de pixels, que está
no relatório e no slide 8, dá **4 reprovações confirmadas, pior 1,66:1**. Trocar os dois
números do slide 9.

**2. Faltam WAVE e ASES no deck.** O slide 7 diz "WAVE e ASES exigem execução no
navegador" — era verdade quando o slide foi feito, mas vocês rodaram os dois depois. A
professora pediu explicitamente o uso de avaliador. Vale um slide com a nota **90,48%** do
ASES e os números do WAVE, ou pelo menos acrescentá-los ao slide 7.

**3. Glitch de fonte no slide 13.** "Visual ≠] acessível" e "Automação ≠] experiência" —
sobrou um `]` depois do sinal. Provavelmente o caractere `≠` não existe na fonte e o
editor deixou resíduo.

---

## 7. Glossário de bolso

| Termo | O que é |
|---|---|
| **Critério de sucesso** | requisito testável da WCAG, com nível A, AA ou AAA |
| **Landmark / região** | marcação que diz ao leitor de tela o papel de um bloco (`<nav>`, `<main>`) |
| **Razão de contraste** | relação entre a luminância do texto e a do fundo; 21:1 é preto no branco |
| **Reflow** | conteúdo se reorganizar em tela estreita sem exigir rolagem horizontal |
| **Alvo (target)** | área clicável ou tocável de um controle |
| **Leitor de tela** | software que narra a interface; TalkBack no Android, VoiceOver no iOS |
| **Árvore de acessibilidade** | estrutura que o navegador expõe à tecnologia assistiva |
| **eMAG** | modelo brasileiro de acessibilidade em governo eletrônico |
| **VLibras** | tradutor automático de Português para Libras, do governo federal |

---

## 8. Se sobrar tempo de fala

O trabalho tem uma boa história para contar, e ela não é a lista de defeitos: é que
**três ferramentas automáticas aprovaram um portal que não atinge o Nível A**. Os dois
critérios que o derrubam só apareceram lendo código-fonte e medindo pixel. E o recurso de
acessibilidade mais visível do site — o VLibras — só foi encontrado quando alguém pegou o
celular e olhou.

Isso, e não o número de erros, é o que o trabalho demonstra.
