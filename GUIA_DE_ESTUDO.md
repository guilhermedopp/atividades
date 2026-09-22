# Guia de estudo — apresentação final

Baseado nos dois documentos entregues: o relatório de 28 páginas e o deck de 14 slides.

**A professora sorteia quem apresenta.** Quem for sorteado apresenta sozinho, o deck
inteiro. Então os dois precisam dar conta dos 14 slides, inclusive das partes que o outro
executou. Este guia é escrito para isso.

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
| 9 | Mobile | 23 de 58 alvos abaixo de 24×24 px. 3 elementos cortados com o espaçamento de texto ampliado. |
| 10 | Tecnologia assistiva | **VLibras existe em todas as páginas** e nenhuma ferramenta automática viu — só apareceu no celular. E a página de Acessibilidade não menciona o recurso. |
| 11 | Conformidade | **Não atinge o Nível A.** Três falhas de A (1.3.1, 1.4.1 e 2.2.2), quatro de AA. |
| 12 | Recomendações | Oito, priorizadas. As duas críticas resolvem o Nível A: botão de pausa e marcador não cromático. |
| 13 | Fechamento | As quatro lições. A mais forte: **automação não é experiência**. |
| 14 | Obrigado | Abrir para perguntas. |

### Ritmo, para 14 slides sozinho

Em 15 minutos dá pouco mais de 1 minuto por slide. Os slides 5 e 6 (checklist) e o 12
(recomendações) são os que mais tentam roubar tempo — **não leia item por item**, aponte o
padrão e siga. O tempo economizado ali vale nos slides 7, 8 e 11, que são o argumento.

Se o tempo apertar, estes cinco sustentam o trabalho sozinhos: **3** (a regra da
conformidade integral), **7** (nota 90,48%), **8** (o banner), **11** (não atinge o Nível A)
e **13** (fechamento). Os outros nove podem ser passados em poucos segundos cada.

### As quatro viradas

O que amarra a narrativa. Decorar estas quatro frases vale mais que decorar números.

1. **Do slide 3 para o 4:** "Guardem essa regra: uma falha de Nível A derruba a
   conformidade em qualquer nível. Ela vai decidir o resultado deste trabalho."
2. **Do slide 7 para o 8:** "Nota 90,48%, quatro erros que nem são do IFAL. Parece um site
   conforme. Mas nenhuma dessas ferramentas olha para o que vem agora."
3. **Do slide 10 para o 11:** "O recurso de acessibilidade mais visível do portal foi o
   único que nenhuma ferramenta automática encontrou. Isso muda o que a gente conclui."
4. **Do slide 11 para o 12:** "Não atinge o Nível A por dois critérios. E os dois têm
   correção de baixo custo."

### Se o sorteio cair em você

O teste com TalkBack foi feito por um de vocês, num aparelho só. Quem apresentar **não deve
narrar em primeira pessoa** uma experiência que não teve — a banca percebe, e o relatório
registra o teste como da equipe, não de um indivíduo.

A forma honesta e que soa melhor: *"a equipe executou a tarefa com TalkBack num Galaxy A15;
a primeira tentativa foi abandonada aos 12 minutos e a segunda concluída em 10 min 16 s"*.
Descreva o que foi observado, não o que você sentiu.

Vale o mesmo para o WAVE e o ASES, executados por um só: os números são da equipe. O que
importa é saber **de onde saiu cada um** — está na tabela da seção 4 e nas perguntas da
seção 5.

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

### Nível AA — as quatro

| Critério | O que falha | Por quê |
|---|---|---|
| **1.4.3** Contraste mínimo | botões do banner a **1,66:1** | exige 4,5:1 |
| **1.4.11** Contraste não textual | foco a **1,56:1** no branco | exige 3:1 |
| **1.4.12** Espaçamento de texto | layout quebra, corta 3 elementos | texto deve suportar ajuste |
| **2.5.8** Tamanho do alvo (WCAG **2.2**) | 23 de 58 alvos < 24×24 px | dedo não acerta alvo pequeno |

Cuidado com o 2.5.8: ele **não existe na WCAG 2.1** — entrou na 2.2. O enunciado admite
"WCAG 2.1 ou mais recentes", então ele vale como complemento. Na 2.1 o equivalente é o
**2.5.5**, de Nível AAA, que o portal também não cumpre.

**Se perguntarem do 1.4.10 Reflow:** a primeira medição o deu como falho (330 px em tela
de 320 px) e a reconferência o corrigiu. Os 330 px eram do bloco provisório
`<div id="barra-brasil">`, que o script da barra federal substitui ao carregar; como no
espelho de medição esse script não carregava, o bloco ficava na tela e transbordava. Com
o script no ar o conteúdo mede 320 px exatos. **O critério é atendido.**

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
| **Contraste** | 3 reprovações confirmadas · pior **1,66:1** |
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
Não. O relatório traz também o **axe-core 4.10.2**, da Deque, motor usado pelo
Lighthouse — o WAVE tem motor próprio, do WebAIM, e por isso os dois podem discordar:
**zero violações** de critério A/AA nas três páginas. Ficou de fora do
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
