# O que falta preencher — 26 campos

Tudo o que dava para medir por ferramenta já foi medido. O que sobrou depende de
navegador com interação humana ou de aparelho real, e por isso é tarefa de vocês.

Enquanto esses campos estiverem vazios, eles aparecem destacados em **amarelo no
Word** e em **vermelho nos slides**, como `[PREENCHER: ...]`.

**Regra que não se quebra:** nenhum número entra nos documentos sem ter sido
medido. Se alguma ferramenta não rodar, o campo fica vazio e o relatório diz
isso. Não inventem valor plausível.

---

## Tarefa 1 — WAVE (7 campos)

**Quem faz:** um de vocês, no navegador do computador.
**Tempo:** uns 10 minutos.

### Passo a passo

1. Abra <https://wave.webaim.org/>
2. Cole a URL: `https://www2.ifal.edu.br/campus/maceio`
3. Clique em **WAVE this page!**
4. Na barra lateral esquerda, aba **Summary**, anote os seis números.
5. Clique na aba **Details** e anote os erros que mais aparecem, com a
   quantidade de cada um.
6. **Print da barra lateral inteira** (com os números visíveis) →
   salvar em `evidencias/wave/`

> Se preferir, dá para instalar a extensão do WAVE no Chrome ou Firefox e rodar
> direto na página. O resultado é o mesmo.

### O que anotar

| Campo | Onde está no WAVE |
|---|---|
| `errors` | Summary → **Errors** (círculo vermelho) |
| `contrast_errors` | Summary → **Contrast Errors** (círculo preto/amarelo) |
| `alerts` | Summary → **Alerts** (triângulo amarelo) |
| `features` | Summary → **Features** (círculo verde) |
| `structural_elements` | Summary → **Structural Elements** (círculo azul) |
| `aria` | Summary → **ARIA** (círculo roxo) |
| `principais_erros` | Details → os erros mais frequentes, com a contagem |

---

## Tarefa 2 — ASES (13 campos)

**Quem faz:** o outro, no navegador do computador.
**Tempo:** uns 10 minutos.

Eu não consegui rodar por código: o ASES protege o envio com **CAPTCHA**, e não
vou contornar isso.

### Passo a passo

1. Abra <https://asesweb.governoeletronico.gov.br/>
2. No campo **URL**, cole: `https://www2.ifal.edu.br/campus/maceio`
3. Resolva o CAPTCHA e clique em **Avaliar**
4. Anote a **nota geral** (aparece em porcentagem, ex.: `72,93`)
5. Desça até a tabela de ocorrências por seção do eMAG e anote **erros** e
   **avisos** de cada uma das seis seções.
6. **Print da nota e da tabela** → salvar em `evidencias/ases/`

### O que anotar

Seis seções, dois números cada (erros e avisos):

| Seção do eMAG | Campos |
|---|---|
| 1. Marcação | `marcacao_erros`, `marcacao_avisos` |
| 2. Comportamento | `comportamento_erros`, `comportamento_avisos` |
| 3. Conteúdo / Informação | `conteudo_erros`, `conteudo_avisos` |
| 4. Apresentação / Design | `apresentacao_erros`, `apresentacao_avisos` |
| 5. Multimídia | `multimidia_erros`, `multimidia_avisos` |
| 6. Formulários | `formularios_erros`, `formularios_avisos` |

Mais a `nota_geral`.

> Se alguma seção não aparecer no relatório do ASES, escrevam `0` **apenas se o
> ASES mostrar zero**. Se a seção simplesmente não for exibida, digam isso — é
> diferente de zero e o relatório precisa registrar a diferença.

---

## Tarefa 3 — Teste no celular com leitor de tela (6 campos)

**Quem faz:** um de vocês, em aparelho real. O outro cronometra e anota.
**Tempo:** uns 30 minutos, contando a curva de aprendizado dos gestos.

Isto é a **tarefa complementar** que a professora sugeriu. O simulador que eu
rodei não substitui: ele mede a árvore de acessibilidade, não a experiência.

### Como ativar o leitor de tela

- **Android (TalkBack):** Configurações → Acessibilidade → TalkBack → ativar.
  Atalho: segurar os dois botões de volume por 3 segundos.
- **iPhone (VoiceOver):** Ajustes → Acessibilidade → VoiceOver → ativar.
  Atalho: triplo clique no botão lateral.

Gestos básicos do TalkBack: deslizar para a direita avança para o próximo
elemento, toque duplo ativa, deslizar com dois dedos rola a tela.

### A tarefa a executar

> Localizar, a partir da página inicial, o edital mais recente publicado pelo
> campus e abrir o documento correspondente.

Comece em `https://www2.ifal.edu.br/campus/maceio`, **de olhos fechados ou com a
tela desligada** — é o ponto do exercício. Cronometre do início até abrir o
edital, ou até desistir.

### O que anotar

| Campo | O que é |
|---|---|
| `dispositivo` | modelo do aparelho, ex.: `Samsung Galaxy A54` |
| `sistema` | ex.: `Android 14` ou `iOS 17` |
| `leitor_tela` | `TalkBack` ou `VoiceOver` |
| `tempo_gasto` | ex.: `7 minutos` ou `não concluída em 15 minutos` |
| `tarefa_concluida` | `sim` ou `não` |
| `relato` | o texto do relato — ver abaixo |

### O relato (a parte que mais vale nota)

Escrevam de 5 a 10 linhas, em primeira pessoa do plural. Vale mais o que deu
errado do que o que deu certo. Pontos que ajudam:

- Em que momento se perderam, e por quê
- O que o leitor anunciou que não ajudou (ex.: "link", "imagem", "lista")
- Quantos deslizes até chegar ao conteúdo principal
- **O banner rotativo atrapalhou?** Ele troca de slide a cada 4 segundos. Se a
  leitura foi interrompida no meio, isso é a falha de WCAG 2.2.2 acontecendo na
  prática — e é o achado mais forte do trabalho. Descrevam com detalhe.
- **Testem o VLibras junto.** O botão azul flutuante que o Guilherme fotografou.
  Com o TalkBack ligado, ele é alcançável? É anunciado com algum nome? Isso
  ninguém mediu ainda e rende parágrafo próprio.
- A sensação de usar assim. Frustração, cansaço, vontade de desistir — isso é
  dado, não desabafo.

**Prints ou gravação de tela** → salvar em `evidencias/mobile/`

---

## Como me mandar o resultado

Copiem o bloco abaixo, preencham e colem aqui na conversa. Pode mandar em
partes, conforme forem terminando — não precisa esperar as três tarefas.

```
WAVE (https://www2.ifal.edu.br/campus/maceio)
  errors:
  contrast_errors:
  alerts:
  features:
  structural_elements:
  aria:
  principais_erros:

ASES (https://www2.ifal.edu.br/campus/maceio)
  nota_geral:
  marcacao_erros:            marcacao_avisos:
  comportamento_erros:       comportamento_avisos:
  conteudo_erros:            conteudo_avisos:
  apresentacao_erros:        apresentacao_avisos:
  multimidia_erros:          multimidia_avisos:
  formularios_erros:         formularios_avisos:

CELULAR COM LEITOR DE TELA
  dispositivo:
  sistema:
  leitor_tela:
  tempo_gasto:
  tarefa_concluida:
  relato:


```

Os prints podem ser anexados aqui na conversa também — eu salvo nas pastas
certas de `evidencias/` e uso como figura no relatório, como fiz com o print do
VLibras.

## O que acontece depois

Eu preencho o `dados/dados_trabalho.json`, rodo
`python3 ferramenta/gerar_documentos.py` e o script confirma
**"Todos os campos preenchidos"**. Os destaques amarelos e vermelhos somem
sozinhos. Aí regero os PDFs com `./ferramenta/gerar_pdf.sh` para vocês
conferirem antes de entregar.

Uma coisa a considerar quando os números do WAVE e do ASES chegarem: o axe-core
não encontrou **nenhuma** violação direta de critério WCAG A/AA nas três
páginas. Se o ASES devolver uma nota baixa, isso não contradiz o axe-core —
significa que as duas ferramentas medem coisas diferentes, e essa divergência
rende uma boa análise na seção 4.11. Não se assustem se os números brigarem.
