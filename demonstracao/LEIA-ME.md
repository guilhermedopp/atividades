# Demonstração das ferramentas

Esta pasta **não é a entrega**. Ela mostra o instrumento funcionando de ponta a ponta
sobre um portal fictício de três páginas (`ferramenta/exemplo/portal-demo/`), construído
propositalmente com os defeitos mais comuns de sítios institucionais.

Os dois documentos aqui saíram com **zero marcadores pendentes** e trazem um aviso em
vermelho na capa e no slide de abertura informando que são demonstração.

## Como reproduzir

```bash
cd ferramenta/exemplo/portal-demo && python3 -m http.server 8777 &
cd -
python3 ferramenta/auditor_wcag.py \
  http://localhost:8777/index.html \
  http://localhost:8777/noticias.html \
  http://localhost:8777/contato.html
python3 ferramenta/simulador_mobile.py http://localhost:8777/index.html --aparelho pixel7
cp demonstracao/dados/dados_demonstracao.json dados/
python3 ferramenta/gerar_documentos.py --dados dados_demonstracao.json --saida-dir demonstracao
```

## O que foi realmente medido

| Origem | Situação |
|---|---|
| `auditor_wcag.py` (3 páginas) | medido |
| `simulador_mobile.py` (contraste, foco, alvos de toque, reflow, zoom, leitor de tela) | medido |
| Itens de julgamento humano do checklist | redigidos a partir das medições acima |
| **WAVE e ASES** | **não executados** — exigem URL pública, e o portal de teste roda em localhost |

Na avaliação do site real, os campos do WAVE e do ASES recebem os números lidos
diretamente das duas ferramentas.

## Conteúdo

```
dados/      entradas e saídas usadas nesta demonstração
capturas/   capturas do simulador (412px e reflow em 320px)
```
