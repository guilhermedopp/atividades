# Resumo verificado para a apresentação

Todos os números abaixo saem de `dados/dados_trabalho.json`, o mesmo arquivo que
gera o relatório. Se o slide divergir daqui, diverge do relatório.

## O veredito, em uma frase

**Portal do IFAL - Campus Maceió — Não atinge o Nível A.**

- **Nível A:** 1.3.1 Informações e relações (a página de contato não declara nenhum elemento de cabeçalho, embora apresente seções visualmente tituladas, de modo que a estrutura percebida por quem enxerga não é programaticamente determinável); 1.4.1 Uso de cores (marcador do slide ativo diferenciado apenas pela cor de fundo); e 2.2.2 Pausar, Parar, Ocultar (banner rotativo com avanço automático a cada 4 segundos, sem mecanismo de pausa).
- **Nível AA:** 1.4.3 Contraste mínimo (3 reprovações confirmadas por amostragem de pixels, a pior em 1,66:1); 1.4.11 Contraste não textual (indicador de foco de 2 px na cor rgb(241,202,127), que atinge apenas 1,56:1 sobre o fundo branco da área de conteúdo, onde exige-se 3:1); e 1.4.12 Espaçamento de texto (3 elementos com conteúdo cortado sob o espaçamento exigido pelo critério). Acrescenta-se o critério 2.5.8 Tamanho do alvo (mínimo), que mede 23 dos 58 alvos interativos da versão móvel abaixo de 24 por 24 pixels: ele pertence à WCAG 2.2, e não à 2.1, e é aqui adotado como complemento, conforme facultado pelo enunciado do trabalho ao admitir "WCAG 2.1 ou mais recentes". Na WCAG 2.1 o requisito equivalente é o 2.5.5 Tamanho do alvo, de Nível AAA, que o sítio também não cumpre. O critério 1.4.10 Reflow, registrado como falho na primeira medição, foi reclassificado como atendido — ver a nota de reconferência.

## Números das ferramentas

| Ferramenta | Resultado |
|---|---|
| WAVE | 4 erros · 21 de contraste · 32 alertas · 16 recursos · 42 estruturais · 0 ARIA · AIM 5,3 de 10 |
| ASES (eMAG 3.1) | nota **90,48%** · 40 erros · 310 avisos |
| axe-core 4.10.2 | **0** violações WCAG A/AA nas 3 páginas · 41 / 40 / 35 regras aprovadas |
| Contraste por pixel | 3 reprovações confirmadas · pior 1,66:1 |
| TalkBack (Samsung Galaxy A15 5G) | Sim, na segunda tentativa · primeira tentativa abandonada aos 12 min 4 s; segunda tentativa concluída em 10 min 16 s |

### ASES por seção do eMAG

| Seção | Erros | Avisos |
|---|---|---|
| 1. Marcação | 29 | 236 |
| 2. Comportamento | 0 | 5 |
| 3. Conteúdo / Informação | 11 | 69 |
| 4. Apresentação / Design | 0 | 0 |
| 5. Multimídia | 0 | 0 |
| 6. Formulários | 0 | 0 |
| **Total** | **40** | **310** |

### Contraste reprovado (medido na tela, não estimado)

| Elemento | Razão | Exigido |
|---|---|---|
| Botão de navegação do banner rotativo (slides 1, 3 e 4) | 1,66:1 | 4,5:1 |
| Botão de navegação do banner rotativo (slide ativo) | 3,0:1 | 4,5:1 |
| Link "Voltar para o topo" | 4,48:1 | 4,5:1 |

Indicador de foco: **1,56:1** sobre o branco do conteúdo (exige 3,0:1); 5,81:1 sobre o verde do cabeçalho.

## Checklist de 15 itens

| # | Item | Situação |
|---|---|---|
| 1 | Texto alternativo em imagens | Parcial |
| 2 | Hierarquia de cabeçalhos | Não conforme |
| 3 | Idioma da página declarado | Conforme |
| 4 | Título de página descritivo | Conforme |
| 5 | Contraste mínimo de cores | Não conforme |
| 6 | Cor não é o único meio de transmitir informação | Não conforme |
| 7 | Redimensionamento de texto até 200% | Parcial |
| 8 | Navegação completa por teclado | Conforme |
| 9 | Indicador de foco visível | Parcial |
| 10 | Link para pular ao conteúdo principal | Conforme |
| 11 | Rótulos associados aos campos de formulário | Conforme |
| 12 | Identificação e sugestão de correção de erros | Não aplicável |
| 13 | Links com texto descritivo | Parcial |
| 14 | Controle de conteúdo em movimento | Não conforme |
| 15 | Estrutura semântica e marcação válida | Parcial |

## As 12 recomendações, na ordem

1. **[Crítica]** Banner rotativo sem controle de pausa — WCAG 2.2.2 (A)
2. **[Crítica]** Slide ativo identificado apenas pela cor — WCAG 1.4.1 (A)
3. **[Alta]** Contraste insuficiente nos controles do banner — WCAG 1.4.3 (AA)
4. **[Alta]** Página inicial e página de contato sem <h1> — WCAG 1.3.1 / 2.4.6 (A/AA)
5. **[Alta]** Ausência de região de navegação no código do campus — WCAG 1.3.1 (A)
6. **[Média]** Indicador de foco pouco perceptível sobre fundo branco — WCAG 1.4.11 (AA)
7. **[Média]** Alvos de toque abaixo do mínimo — WCAG 2.5.8 (AA, WCAG 2.2)
8. **[Média]** Layout quebra com espaçamento de texto ampliado — WCAG 1.4.12 (AA)
9. **[Média]** Texto alternativo redundante — WCAG 1.1.1 (A)
10. **[Baixa]** URL crua como texto de link — WCAG 2.4.4 (A)
11. **[Baixa]** Página de Acessibilidade desatualizada — eMAG 3.1
12. **[Baixa]** Marcação provisória da Barra do Governo em estado degradado — WCAG 1.4.10 / 1.4.3 (AA), apenas em estado degradado

## Cuidado: seis coisas que o deck NÃO deve dizer

Cada uma destas eu afirmei em algum momento e tive de corrigir depois de medir.

1. **"O site não tem VLibras."** Tem, em todas as páginas. Não aparece no HTML
   servido porque é injetado por `barra.brasil.gov.br/barra.js`.
2. **"Os 4 erros do WAVE são do IFAL."** Não são. A auditoria de código-fonte achou
   0 imagens sem alt e 0 links sem texto nas 3 páginas; o `barra.js` tem exatamente
   1 imagem sem alt e 2 âncoras vazias. O terceiro link vazio ficou sem atribuição.
3. **"O WAVE achou 1 região de navegação, então o site tem uma."** Essa região é o
   único `<nav>` do `barra.js`. As 3 páginas do IFAL têm zero `<nav>` e zero
   `role="navigation"`.
4. **"Nota 90,48% e zero violações no axe-core, então está conforme."** Nenhuma das
   três ferramentas testa 2.2.2 nem 1.4.1 — justamente os dois critérios que derrubam
   o Nível A. Aprovação em avaliador automático não é atestado de conformidade.
5. **"O site falha o 1.4.10 Reflow: 330 px em tela de 320 px."** Falhava só na
   medição. Os 330 px vinham do bloco provisório `<div id="barra-brasil">`, que o
   `barra.js` substitui ao carregar. Com o script no ar o conteúdo mede 320 px e o
   critério é atendido. São **4** falhas de AA, não 5.
6. **"O axe-core é o motor do WAVE."** É o motor do Lighthouse. O WAVE tem motor
   próprio, do WebAIM — por isso os dois discordam.

## Imagens prontas em `evidencias/telas/`

| Arquivo | Serve para mostrar |
|---|---|
| `02-topo-barra-acessibilidade.png` | os 4 atalhos Alt+1..4 e o Alto Contraste |
| `13-carrossel-banner-rotativo.png` | onde estão as piores falhas |
| `04-foco-teclado.png` | o contorno de foco âmbar |
| `08-reflow-320px.png` | o bloco provisório da barra federal cortado a 320 px |
| `14-vlibras-botao-flutuante.jpg` | o VLibras, achado no aparelho real |
| `05-pagina-acessibilidade.png` | a página institucional desatualizada |

Prints do WAVE em `evidencias/wave/` e do ASES em `evidencias/ases/`.
