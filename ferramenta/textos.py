# -*- coding: utf-8 -*-
"""Textos corridos do relatório e da apresentação.

Os trechos com \x00...\x01 são preenchidos automaticamente a partir de
dados/dados_trabalho.json; quando o dado ainda não existe, aparecem
destacados como [PREENCHER: ...].
"""


def V(valor, dica):
    """Retorna o valor ou um marcador de preenchimento destacavel."""
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return "\x00[PREENCHER: %s]\x01" % dica
    return str(valor)


def introducao(d):
    s = d["site"]
    return [
        "A acessibilidade web é a propriedade que permite que pessoas com deficiência "
        "percebam, compreendam, naveguem, interajam e contribuam com a Web (W3C, 2018). "
        "Segundo o Censo Demográfico de 2022 do IBGE, cerca de 14,4 milhões de brasileiros "
        "com dois anos ou mais possuem algum tipo de deficiência, contingente para o qual a "
        "barreira digital se traduz, na prática, em exclusão do acesso a serviços, a "
        "informação pública e ao exercício da cidadania.",

        "No Brasil, a acessibilidade digital não é apenas uma boa prática de engenharia de "
        "software: é uma obrigação legal. O Decreto n. 5.296/2004 determina a acessibilidade "
        "dos portais da administração pública, e a Lei Brasileira de Inclusão (Lei n. "
        "13.146/2015), em seu artigo 63, estende a exigência aos sítios de empresas com sede "
        "ou representação comercial no país. Do ponto de vista técnico, esse dever se "
        "materializa em dois documentos normativos complementares: as Diretrizes de "
        "Acessibilidade para o Conteúdo da Web (WCAG) 2.1, publicadas pelo W3C em 2018, e o "
        "Modelo de Acessibilidade em Governo Eletrônico (eMAG) 3.1, de 2014, que adapta a "
        "WCAG ao contexto do governo brasileiro.",

        "O presente relatório apresenta a avaliação de acessibilidade web do "
        + V(s.get("nome"), "nome do site avaliado") + ", disponível em "
        + V(s.get("url"), "URL do site") + ". A avaliação combinou três abordagens "
        "complementares - inspeção manual por checklist, avaliação automatizada por "
        "ferramentas especializadas e teste de uso real com leitor de tela em dispositivo "
        "móvel -, estratégia recomendada pela literatura porque ferramentas automáticas "
        "detectam, isoladamente, apenas parte dos problemas de acessibilidade, restando a "
        "inspeção humana os critérios de natureza semântica e subjetiva.",
    ]


def objetivo_geral(d):
    s = d["site"]
    return ("Avaliar o nível de conformidade de acessibilidade do "
            + V(s.get("nome_curto"), "nome curto do site") + " (" + V(s.get("url"), "URL")
            + ") frente as Diretrizes de Acessibilidade para o Conteúdo da Web (WCAG) 2.1 "
            "e as recomendações do eMAG 3.1, identificando as barreiras que impedem o uso "
            "pleno do sítio por pessoas com deficiência e propondo correções técnicas "
            "viáveis para cada problema encontrado.")


OBJETIVOS_ESPECIFICOS = [
    "Inspecionar manualmente o sítio a partir de um checklist de 15 itens essenciais de "
    "acessibilidade, mapeando cada item aos critérios de sucesso da WCAG 2.1 e as "
    "recomendações do eMAG 3.1;",
    "Submeter as páginas selecionadas a avaliadores automáticos (WAVE e ASES), obtendo o "
    "diagnóstico quantitativo dos erros presentes no código-fonte;",
    "Confrontar os resultados manuais e automáticos, distinguindo falhas de marcação de "
    "falhas de experiência de uso;",
    "Vivenciar a navegação no sítio por meio de smartphone com leitor de tela ativado, "
    "registrando as barreiras percebidas na execução de uma tarefa real;",
    "Determinar o nível de conformidade (A, AA ou AAA) alcancado pelo sítio e elaborar "
    "recomendações de correção priorizadas por severidade.",
]


def metodologia(d):
    s = d["site"]
    paginas = s.get("paginas_avaliadas") or []
    lista = "; ".join(paginas) if paginas else "\x00[PREENCHER: páginas avaliadas]\x01"
    return [
        ("A avaliação seguiu um desenho metodologico em quatro etapas sequenciais, aplicado "
         "sobre um recorte de " + str(len(paginas) or 3) + " páginas representativas do sítio: "
         + lista + ". O recorte privilegiou a página inicial, uma página de listagem de "
         "conteúdo e uma página transacional (com formulário), de modo a cobrir os três "
         "padrões de interação presentes no portal."),

        ("Etapa 1 - Inspeção manual por checklist. Aplicou-se um checklist de 15 itens "
         "essenciais de acessibilidade, consolidado a partir do material de referência "
         "indicado pela disciplina e mapeado, item a item, aos critérios de sucesso da WCAG "
         "2.1 e as recomendações do eMAG 3.1. Cada item foi verificado com o sítio aberto no "
         "navegador Google Chrome, com auxílio das ferramentas de desenvolvedor (F12) para "
         "leitura do código-fonte. A inspeção contemplou testes de operação exclusivamente "
         "por teclado (Tab, Shift+Tab, Enter, Espaco e Esc), verificação de zoom em 200% e "
         "simulação de escala de cinza para checar dependência de cor."),

        ("Etapa 2 - Avaliação automatizada. As mesmas páginas foram submetidas a dois "
         "avaliadores: o WAVE (WebAIM), de referência internacional, que reporta erros "
         "diretamente sobre a renderização da página; e o ASES (Avaliador e Simulador de "
         "Acessibilidade de Sítios), mantido pelo Governo Federal, que emite nota de 0 a 100 "
         "segundo as recomendações do eMAG. Adicionalmente, desenvolveu-se um auditor próprio "
         "em Python (ferramenta/auditor_wcag.py), que percorre o HTML e verifica de forma "
         "programática os nove itens automatizáveis do checklist, servindo de conferência "
         "cruzada aos dois avaliadores."),

        ("Etapa 3 - Tarefa complementar com leitor de tela. Um dos avaliadores acessou o "
         "sítio por smartphone com o leitor de tela nativo ativado e tentou executar uma "
         "tarefa real de ponta a ponta, sem visualizar a tela. Registraram-se o tempo gasto, "
         "a conclusão ou não da tarefa e as barreiras percebidas."),

        ("Etapa 4 - Consolidação e análise de conformidade. Os achados foram agrupados por "
         "critério de sucesso da WCAG 2.1 e classificados por severidade. Aplicou-se entao a "
         "regra de conformidade do W3C, segundo a qual um sítio só atinge determinado nível "
         "se satisfizer integralmente todos os critérios daquele nível e dos anteriores - "
         "basta uma falha de Nível A para que a página não seja conforme em nenhum nível."),
    ]


def analise_conformidade(d):
    c = d.get("conformidade", {})
    return [
        ("A WCAG 2.1 organiza seus 78 critérios de sucesso em três níveis cumulativos. O "
         "Nível A reúne os requisitos mínimos, cuja ausência torna o conteúdo inacessível "
         "para grupos inteiros de usuários. O Nível AA acrescenta os requisitos que removem "
         "as barreiras mais significativas e constitui o patamar exigido da administração "
         "pública brasileira e adotado como referência pela legislação de diversos países. O "
         "Nível AAA compreende o refinamento máximo, nem sempre aplicável a todo tipo de "
         "conteúdo."),

        ("A regra de conformidade é estrita e não admite compensação: a página só é conforme "
         "em determinado nível se atender integralmente a todos os critérios daquele nível e "
         "dos níveis anteriores. Uma única falha de Nível A, portanto, impede a conformidade "
         "mesmo que todos os demais critérios estejam satisfeitos."),

        ("Aplicada essa regra aos resultados consolidados, o nível de conformidade atingido "
         "pelo sítio avaliado foi: " + V(c.get("nivel_atingido"),
         "nível atingido: 'Não conforme', 'A', 'AA' ou 'AAA'") + ". Foram identificadas "
         + V(c.get("criterios_a_falhos"), "quantidade de critérios de Nível A não atendidos")
         + " falha(s) em critérios de Nível A e "
         + V(c.get("criterios_aa_falhos"), "quantidade de critérios de Nível AA não atendidos")
         + " falha(s) em critérios de Nível AA."),
    ]


def conclusao(d):
    s = d["site"]
    c = d.get("conformidade", {})
    return [
        ("A avaliação do " + V(s.get("nome_curto"), "nome curto do site") + " evidenciou o "
         "descompasso, recorrente em sítios institucionais brasileiros, entre a aparência "
         "cuidada da interface e a qualidade da marcação que a sustenta. Problemas que passam "
         "despercebidos ao usuário vidente - uma imagem sem atributo alt, um campo de busca "
         "sem rótulo, um cabeçalho usado por efeito visual e não por hierarquia - convertem-se "
         "em bloqueios absolutos para quem depende de tecnologia assistiva."),

        ("A triangulação metodológica mostrou-se decisiva. Os avaliadores automáticos "
         "quantificaram com precisão as falhas de código, mas não julgam se um texto "
         "alternativo descreve adequadamente a imagem, nem se a ordem de foco faz sentido "
         "para quem navega. A inspeção manual e, sobretudo, o teste com leitor de tela em "
         "dispositivo móvel revelaram barreiras de uso que nenhuma métrica automatizada "
         "poderia ter apontado, confirmando a orientação do W3C de que a avaliação "
         "automática cobre apenas parte dos critérios de sucesso."),

        ("O diagnóstico final aponta para o nível de conformidade "
         + V(c.get("nivel_atingido"), "nível atingido") + ". As correções recomendadas na "
         "seção anterior são, em sua maioria, de baixo custo de implementação: tratam-se "
         "majoritariamente de ajustes de marcação HTML - inclusão de atributos alt, "
         "associação de labels a campos, correção da hierarquia de cabeçalhos e adoção de "
         "elementos semânticos de região - que não exigem redesenho visual nem reescrita da "
         "aplicação. A desproporção entre o baixo esforço técnico das correções e o alto "
         "impacto que produzem na vida dos usuários e, talvez, a lição mais importante deste "
         "trabalho."),

        ("Conclui-se que acessibilidade não é um requisito acessório a ser considerado ao "
         "final do desenvolvimento, mas uma qualidade que precisa ser projetada desde a "
         "concepção da interface. Recomenda-se, por fim, que avaliações como a aqui "
         "realizada sejam incorporadas ao ciclo de manutenção do sítio, e não tratadas como "
         "diagnóstico pontual, uma vez que cada nova publicação de conteúdo pode reintroduzir "
         "barreiras já corrigidas."),
    ]


RECOMENDACOES = [
    ("Crítica", "Imagens sem texto alternativo",
     "Incluir o atributo alt em todas as imagens informativas, com descrição sucinta do "
     "conteúdo ou da função; usar alt=\"\" nas puramente decorativas.", "WCAG 1.1.1 (A)"),
    ("Crítica", "Campos de formulário sem rótulo",
     "Associar um elemento <label for=\"id\"> a cada campo, ou, quando o rótulo visível for "
     "inviavel, aplicar aria-label. Placeholder não substitui rótulo.", "WCAG 3.3.2 / 4.1.2 (A)"),
    ("Crítica", "Hierarquia de cabeçalhos incorreta",
     "Definir um único <h1> por página e encadear os demais níveis sem saltos, usando "
     "cabeçalhos por estrutura e não por efeito visual.", "WCAG 1.3.1 (A)"),
    ("Alta", "Ausência de regiões semânticas",
     "Substituir <div> genericas por <header>, <nav>, <main>, <footer> e <aside>, permitir "
     "que o leitor de tela ofereca navegação por regiões.", "WCAG 1.3.1 (A)"),
    ("Alta", "Links com texto não descritivo",
     "Reescrever rótulos como 'clique aqui' e 'saiba mais' de modo que descrevam o destino "
     "mesmo fora de contexto.", "WCAG 2.4.4 (A)"),
    ("Alta", "Contraste insuficiente",
     "Ajustar a paleta para razão mínima de 4,5:1 em texto normal e 3:1 em texto grande e "
     "componentes de interface.", "WCAG 1.4.3 / 1.4.11 (AA)"),
    ("Media", "Foco de teclado não visível",
     "Remover declaracoes 'outline: none' sem substituto e definir estilo de :focus-visible "
     "com contraste adequado.", "WCAG 2.4.7 (AA)"),
    ("Media", "Ausência de link de salto",
     "Inserir, como primeiro elemento focável, um link 'Ir para o conteúdo principal' "
     "apontando para o <main>.", "WCAG 2.4.1 (A)"),
    ("Media", "Conteúdo em movimento sem controle",
     "Disponibilizar botão de pausa acessível por teclado em carrosséis e animações com "
     "duracao superior a cinco segundos.", "WCAG 2.2.2 (A)"),
    ("Baixa", "Bloqueio de zoom em dispositivos móveis",
     "Remover user-scalable=no e maximum-scale=1 da meta viewport, permitir ampliacao de "
     "até 200%.", "WCAG 1.4.4 (AA)"),
]


REFERENCIAS = [
    "BRASIL. Decreto n. 5.296, de 2 de dezembro de 2004. Regulamenta as Leis n. 10.048/2000 e "
    "n. 10.098/2000. Brasília: Presidência da República, 2004.",

    "BRASIL. Lei n. 13.146, de 6 de julho de 2015. Institui a Lei Brasileira de Inclusão da "
    "Pessoa com Deficiência (Estatuto da Pessoa com Deficiência). Brasília: Presidência da "
    "República, 2015.",

    "BRASIL. Ministério do Planejamento, Orçamento e Gestão. eMAG - Modelo de Acessibilidade "
    "em Governo Eletrônico, versão 3.1. Brasília, 2014. Disponível em: "
    "https://emag.governoeletronico.gov.br/. Acesso em: \x02DATA\x02.",

    "BRASIL. Governo Federal. ASES - Avaliador e Simulador de Acessibilidade de Sítios. "
    "Disponível em: https://asesweb.governoeletronico.gov.br/. Acesso em: \x02DATA\x02.",

    "CEWEB.BR. Cartilha de Acessibilidade na Web - Fascículo III: Metodologias e ferramentas "
    "de avaliação. São Paulo: Comitê Gestor da Internet no Brasil, 2019. Disponível em: "
    "https://ceweb.br/guias/cartilha-de-acessibilidade-na-web-fasciculo-iii/. Acesso em: \x02DATA\x02.",

    "CEWEB.BR. Cartilha de Acessibilidade na Web - Fascículo IV: O papel dos usuários na "
    "avaliação de acessibilidade. São Paulo: Comitê Gestor da Internet no Brasil, 2020. "
    "Disponível em: https://ceweb.br/cartilhas/cartilha-w3cbr-acessibilidade-web-fasciculo-IV/. "
    "Acesso em: \x02DATA\x02.",

    "IBGE. Censo Demográfico 2022: Pessoas com deficiência. Rio de Janeiro: Instituto "
    "Brasileiro de Geografia e Estatística, 2023.",

    "MWPT. 15 checklists de acessibilidade essenciais para quem desenvolve canais digitais. "
    "Disponível em: https://mwpt.com.br/15-checklists-de-acessibilidade-essenciais-para-quem-"
    "desenvolve-canais-digitais/. Acesso em: \x02DATA\x02.",

    "W3C. Web Content Accessibility Guidelines (WCAG) 2.1. W3C Recommendation, 5 jun. 2018. "
    "Disponível em: https://www.w3.org/TR/WCAG21/. Acesso em: \x02DATA\x02.",

    "W3C BRASIL. Diretrizes de Acessibilidade para Conteúdo Web (WCAG) 2.1 - tradução "
    "autorizada para o português do Brasil. Disponível em: "
    "https://www.w3c.br/traducoes/wcag/wcag21-pt-BR/. Acesso em: \x02DATA\x02.",

    "WEBAIM. WAVE Web Accessibility Evaluation Tool. Utah State University. Disponível em: "
    "https://wave.webaim.org/. Acesso em: \x02DATA\x02.",
]
