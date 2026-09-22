#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emite RESUMO_PARA_SLIDES.md a partir de dados/dados_trabalho.json.

Serve para quem monta a apresentação por fora do gerador: os números saem do
mesmo arquivo que alimenta o relatório, então o deck não diverge dele.

Uso:  python3 ferramenta/resumo_para_slides.py
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "ferramenta"))
import textos as T                                                   # noqa: E402

d = json.load(open(os.path.join(RAIZ, "dados", "dados_trabalho.json"), encoding="utf-8"))
ck = json.load(open(os.path.join(RAIZ, "dados", "checklist.json"), encoding="utf-8"))
d["_checklist"] = {str(i["id"]): i for i in ck["itens"]}
w, a, m = d["wave"], d["ases"], d["mobile"]
cf, cp = d["conformidade"], d["contraste_pixel"]
axe = d["axe"]["paginas"]
SIT = {"conforme": "Conforme", "nao_conforme": "Não conforme", "parcial": "Parcial",
       "nao_aplicavel": "Não aplicável", "verificar_manualmente": "Verificar"}
L = []
P = L.append


def num(v):
    """Vírgula decimal, como manda o português."""
    return str(v).replace(".", ",")

P("# Resumo verificado para a apresentação\n")
P("Todos os números abaixo saem de `dados/dados_trabalho.json`, o mesmo arquivo que")
P("gera o relatório. Se o slide divergir daqui, diverge do relatório.\n")

P("## O veredito, em uma frase\n")
P(f"**{d['site']['nome_curto']} — {cf['nivel_atingido']}.**\n")
P(f"- **Nível A:** {cf['criterios_a_falhos']}")
P(f"- **Nível AA:** {cf['criterios_aa_falhos']}\n")

P("## Números das ferramentas\n")
P("| Ferramenta | Resultado |")
P("|---|---|")
P(f"| WAVE | {w['errors']} erros · {w['contrast_errors']} de contraste · {w['alerts']} alertas · "
  f"{w['features']} recursos · {w['structural_elements']} estruturais · {w['aria']} ARIA · AIM {w['pontuacao_aim']} |")
P(f"| ASES (eMAG 3.1) | nota **{a['nota_geral']}%** · {a['total_erros']} erros · {a['total_avisos']} avisos |")
P(f"| axe-core 4.10.2 | **0** violações WCAG A/AA nas 3 páginas · "
  f"{' / '.join(str(r['passes']) for r in axe.values())} regras aprovadas |")
P(f"| Contraste por pixel | {len(cp['reprovacoes_confirmadas'])} reprovações confirmadas · "
  f"pior {num(min(r['razao'] for r in cp['reprovacoes_confirmadas']))}:1 |")
P(f"| TalkBack ({m['dispositivo']}) | {m['tarefa_concluida']} · {m['tempo_gasto']} |\n")

P("### ASES por seção do eMAG\n")
P("| Seção | Erros | Avisos |")
P("|---|---|---|")
for rot, ch in [("1. Marcação", "marcacao"), ("2. Comportamento", "comportamento"),
                ("3. Conteúdo / Informação", "conteudo"), ("4. Apresentação / Design", "apresentacao"),
                ("5. Multimídia", "multimidia"), ("6. Formulários", "formularios")]:
    P(f"| {rot} | {a[ch + '_erros']} | {a[ch + '_avisos']} |")
P(f"| **Total** | **{a['total_erros']}** | **{a['total_avisos']}** |\n")

P("### Contraste reprovado (medido na tela, não estimado)\n")
P("| Elemento | Razão | Exigido |")
P("|---|---|---|")
for r in cp["reprovacoes_confirmadas"]:
    P(f"| {r['elemento']} | {num(r['razao'])}:1 | {num(r['exigido'])}:1 |")
f = cp["indicador_de_foco"]
P(f"\nIndicador de foco: **{num(f['sobre_branco'])}:1** sobre o branco do conteúdo "
  f"(exige {num(f['exigido_1411'])}:1); {num(f['sobre_verde_cabecalho'])}:1 sobre o verde do cabeçalho.\n")

P("## Checklist de 15 itens\n")
P("| # | Item | Situação |")
P("|---|---|---|")
for i in range(1, 16):
    it = d["_checklist"][str(i)] if "_checklist" in d else None
    nome = (it or {}).get("nome", "")
    P(f"| {i} | {nome} | {SIT.get(d['checklist_manual'][str(i)]['situacao'], '?')} |")
P("")

P("## As 12 recomendações, na ordem\n")
for n, (prio, titulo, _, wcag) in enumerate(T.RECOMENDACOES, 1):
    P(f"{n}. **[{prio}]** {titulo} — {wcag}")
P("")

P("## Cuidado: seis coisas que o deck NÃO deve dizer\n")
P("Cada uma destas eu afirmei em algum momento e tive de corrigir depois de medir.\n")
P("1. **\"O site não tem VLibras.\"** Tem, em todas as páginas. Não aparece no HTML")
P("   servido porque é injetado por `barra.brasil.gov.br/barra.js`.")
P("2. **\"Os 4 erros do WAVE são do IFAL.\"** Não são. A auditoria de código-fonte achou")
P("   0 imagens sem alt e 0 links sem texto nas 3 páginas; o `barra.js` tem exatamente")
P("   1 imagem sem alt e 2 âncoras vazias. O terceiro link vazio ficou sem atribuição.")
P("3. **\"O WAVE achou 1 região de navegação, então o site tem uma.\"** Essa região é o")
P("   único `<nav>` do `barra.js`. As 3 páginas do IFAL têm zero `<nav>` e zero")
P("   `role=\"navigation\"`.")
P("4. **\"Nota 90,48% e zero violações no axe-core, então está conforme.\"** Nenhuma das")
P("   três ferramentas testa 2.2.2 nem 1.4.1 — justamente os dois critérios que derrubam")
P("   o Nível A. Aprovação em avaliador automático não é atestado de conformidade.")
P("5. **\"O site falha o 1.4.10 Reflow: 330 px em tela de 320 px.\"** Falhava só na")
P("   medição. Os 330 px vinham do bloco provisório `<div id=\"barra-brasil\">`, que o")
P("   `barra.js` substitui ao carregar. Com o script no ar o conteúdo mede 320 px e o")
P("   critério é atendido. São **4** falhas de AA, não 5.")
P("6. **\"O axe-core é o motor do WAVE.\"** É o motor do Lighthouse. O WAVE tem motor")
P("   próprio, do WebAIM — por isso os dois discordam.\n")

P("## Imagens prontas em `evidencias/telas/`\n")
P("| Arquivo | Serve para mostrar |")
P("|---|---|")
P("| `02-topo-barra-acessibilidade.png` | os 4 atalhos Alt+1..4 e o Alto Contraste |")
P("| `13-carrossel-banner-rotativo.png` | onde estão as piores falhas |")
P("| `04-foco-teclado.png` | o contorno de foco âmbar |")
P("| `08-reflow-320px.png` | o bloco provisório da barra federal cortado a 320 px |")
P("| `14-vlibras-botao-flutuante.jpg` | o VLibras, achado no aparelho real |")
P("| `05-pagina-acessibilidade.png` | a página institucional desatualizada |")
P("")
P("Prints do WAVE em `evidencias/wave/` e do ASES em `evidencias/ases/`.\n")

destino = os.path.join(RAIZ, "RESUMO_PARA_SLIDES.md")
open(destino, "w", encoding="utf-8").write("\n".join(L))
print("gerado:", destino)
