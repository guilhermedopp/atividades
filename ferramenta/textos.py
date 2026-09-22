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
        + V(s.get("url"), "URL do site") + ". A avaliação combinou quatro frentes "
        "complementares - inspeção manual por checklist, auditoria do código-fonte das "
        "páginas servidas, avaliação automatizada por ferramentas especializadas (axe-core, "
        "WAVE e ASES) e teste de uso real com leitor de tela em dispositivo móvel -, estratégia recomendada pela literatura porque ferramentas automáticas "
        "detectam, isoladamente, apenas parte dos problemas de acessibilidade, restando à "
        "inspeção humana os critérios de natureza semântica e subjetiva.",
    ]


def objetivo_geral(d):
    s = d["site"]
    return ("Avaliar o nível de conformidade de acessibilidade do "
            + V(s.get("nome_curto"), "nome curto do site") + " (" + V(s.get("url"), "URL")
            + ") frente às Diretrizes de Acessibilidade para o Conteúdo da Web (WCAG) 2.1 "
            "e às recomendações do eMAG 3.1, identificando as barreiras que impedem o uso "
            "pleno do sítio por pessoas com deficiência e propondo correções técnicas "
            "viáveis para cada problema encontrado.")


OBJETIVOS_ESPECIFICOS = [
    "Inspecionar manualmente o sítio a partir de um checklist de 15 itens essenciais de "
    "acessibilidade, mapeando cada item aos critérios de sucesso da WCAG 2.1 e às "
    "recomendações do eMAG 3.1;",
    "Submeter as páginas selecionadas a avaliadores automáticos (WAVE, ASES e axe-core), "
    "obtendo o "
    "diagnóstico quantitativo dos erros presentes no código-fonte;",
    "Confrontar os resultados manuais e automáticos, distinguindo falhas de marcação de "
    "falhas de experiência de uso;",
    "Vivenciar a navegação no sítio por meio de smartphone com leitor de tela ativado, "
    "registrando as barreiras percebidas na execução de uma tarefa real;",
    "Determinar o nível de conformidade (A, AA ou AAA) alcançado pelo sítio e elaborar "
    "recomendações de correção priorizadas por severidade.",
]


def metodologia(d):
    s = d["site"]
    paginas = s.get("paginas_avaliadas") or []
    lista = "; ".join(paginas) if paginas else "\x00[PREENCHER: páginas avaliadas]\x01"
    return [
        ("A avaliação seguiu um desenho metodológico em quatro etapas sequenciais, aplicado "
         "sobre um recorte de " + str(len(paginas) or 3) + " páginas representativas do sítio: "
         + lista + ". O recorte privilegiou a página inicial, uma página de listagem de "
         "conteúdo e a página institucional de contato, de modo a cobrir os três "
         "padrões de interação presentes no portal."),

        ("Etapa 1 - Inspeção manual por checklist. Aplicou-se um checklist de 15 itens "
         "essenciais de acessibilidade, consolidado a partir do material de referência "
         "indicado pela disciplina e mapeado, item a item, aos critérios de sucesso da WCAG "
         "2.1 e às recomendações do eMAG 3.1. Cada item foi verificado com o sítio aberto no "
         "navegador Google Chrome, com auxílio das ferramentas de desenvolvedor (F12) para "
         "leitura do código-fonte. A inspeção contemplou testes de operação exclusivamente "
         "por teclado (Tab, Shift+Tab, Enter, Espaço e Esc), verificação de zoom em 200% e "
         "simulação de escala de cinza para checar dependência de cor."),

        ("Etapa 2 - Avaliação automatizada. As mesmas páginas foram submetidas a três "
         "avaliadores de motores distintos: o WAVE (WebAIM), de referência internacional, "
         "que reporta erros diretamente sobre a renderização da página; o ASES (Avaliador e "
         "Simulador de Acessibilidade de Sítios), mantido pelo Governo Federal, que emite "
         "nota de 0 a 100 segundo as recomendações do eMAG; e o axe-core 4.10.2, da Deque "
         "Systems, executado sobre a página renderizada em Chromium. São motores "
         "independentes — o WAVE tem motor próprio, o axe-core é o que o Lighthouse do "
         "Google Chrome utiliza —, o que torna a convergência entre eles um indício mais "
         "forte do que a repetição de uma mesma ferramenta. Adicionalmente, desenvolveu-se "
         "um auditor próprio em Python (ferramenta/auditor_wcag.py), que percorre o HTML e "
         "verifica de forma programática os nove itens automatizáveis do checklist, "
         "servindo de conferência cruzada aos três avaliadores."),

        ("Etapa 3 - Tarefa complementar com leitor de tela. Um dos avaliadores acessou o "
         "sítio por smartphone com o leitor de tela nativo ativado e tentou executar uma "
         "tarefa real de ponta a ponta, sem visualizar a tela. Registraram-se o tempo gasto, "
         "a conclusão ou não da tarefa e as barreiras percebidas."),

        ("Etapa 4 - Consolidação e análise de conformidade. Os achados foram agrupados por "
         "critério de sucesso da WCAG 2.1 e classificados por severidade. Aplicou-se então a "
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
         "nível atingido: 'Não conforme', 'A', 'AA' ou 'AAA'") + "."),

        ("Não foram atendidos, em Nível A, os seguintes critérios de sucesso: "
         + V(c.get("criterios_a_falhos"), "critérios de Nível A não atendidos")),

        ("Em Nível AA, não foram atendidos os critérios: "
         + V(c.get("criterios_aa_falhos"), "critérios de Nível AA não atendidos")),
    ]


def conclusao(d):
    s = d["site"]
    c = d.get("conformidade", {})
    return [
        ("A avaliação do " + V(s.get("nome_curto"), "nome curto do site") + " produziu um "
         "resultado menos simples do que o esperado. A base técnica herdada do Plone com a "
         "Identidade Digital do Governo cumpre bem o essencial: idioma declarado, títulos "
         "únicos, campos com rótulo associado, imagens com atributo alt, quatro atalhos de "
         "salto e indicador de foco em todos os 118 pontos de parada do teclado. O avaliador "
         "axe-core não encontrou uma única violação direta de critério de sucesso nas três "
         "páginas analisadas. As barreiras concentram-se, em vez disso, em um componente "
         "específico e em detalhes de apresentação que nenhuma verificação superficial "
         "revelaria."),

        ("A triangulação metodológica mostrou-se decisiva. Os avaliadores automáticos "
         "quantificaram com precisão as falhas de código, mas não julgam se um texto "
         "alternativo descreve adequadamente a imagem, nem se a ordem de foco faz sentido "
         "para quem navega. O caso do contraste é exemplar: o axe-core devolveu dezenas de "
         "ocorrências como indecidíveis, por serem textos desenhados sobre fotografias, e a "
         "falha mais grave - botões a 1,66:1 - só apareceu ao medir os pixels efetivamente "
         "pintados na tela. Do mesmo modo, a ausência de controle de pausa no banner exigiu "
         "a leitura do código-fonte do script que o governa. Isso confirma a orientação do "
         "W3C de que a avaliação automática cobre apenas parte dos critérios de sucesso."),

        ("O diagnóstico final aponta para o nível de conformidade "
         + V(c.get("nivel_atingido"), "nível atingido") + ". As correções recomendadas na "
         "seção anterior são, em sua maioria, de baixo custo de implementação: um botão de "
         "pausa no banner rotativo, um segundo indicador não cromático para o slide ativo, "
         "a troca da cor dos botões numéricos, a declaração de um <h1> por página e a "
         "marcação dos menus como região de navegação - ajustes pontuais que não exigem "
         "redesenho visual nem reescrita da aplicação. A desproporção entre o baixo esforço técnico das correções e o alto "
         "impacto que produzem na vida dos usuários é, talvez, a lição mais importante deste "
         "trabalho."),

        ("Conclui-se que acessibilidade não é um requisito acessório a ser considerado ao "
         "final do desenvolvimento, mas uma qualidade que precisa ser projetada desde a "
         "concepção da interface. Recomenda-se, por fim, que avaliações como a aqui "
         "realizada sejam incorporadas ao ciclo de manutenção do sítio, e não tratadas como "
         "diagnóstico pontual, uma vez que cada nova publicação de conteúdo pode reintroduzir "
         "barreiras já corrigidas."),
    ]


# Recomendações derivadas das medições desta avaliação, ordenadas pelo efeito
# sobre a conformidade: primeiro o que impede o Nível A, depois o Nível AA.
RECOMENDACOES = [
    ("Crítica", "Banner rotativo sem controle de pausa",
     "O script banner_rotativo.js troca de slide a cada 4000 ms e se reagenda "
     "indefinidamente. Incluir um botão de pausar/retomar alcançável por teclado e "
     "anunciado ao leitor de tela, ou suprimir o avanço automático. Enquanto não "
     "houver esse controle, o portal não atinge sequer o Nível A.", "WCAG 2.2.2 (A)"),

    ("Crítica", "Slide ativo identificado apenas pela cor",
     "No banner, o slide em exibição é sinalizado somente pela cor de fundo do botão "
     "numérico (âmbar contra verde). Acrescentar um segundo indicador não cromático "
     "— contorno, mudança de forma ou aria-current=\"true\" — para que a informação "
     "não dependa da percepção de cor.", "WCAG 1.4.1 (A)"),

    ("Alta", "Contraste insuficiente nos controles do banner",
     "Os botões numéricos usam azul rgb(44,103,205) sobre verde rgb(14,86,31), razão "
     "de 1,66:1, e 3,0:1 quando o slide está ativo. Adotar texto branco ou de "
     "luminância equivalente, atingindo ao menos 4,5:1.", "WCAG 1.4.3 (AA)"),

    ("Alta", "Página inicial e página de contato sem <h1>",
     "A página inicial reúne 15 cabeçalhos sem nenhum <h1>, e a página de contato não "
     "possui cabeçalho algum. Declarar um <h1> único por página, correspondente ao "
     "título principal, para dar ponto de partida à navegação por cabeçalhos.",
     "WCAG 1.3.1 / 2.4.6 (A/AA)"),

    ("Alta", "Ausência de região de navegação no código do campus",
     "O portal declara role=\"banner\", role=\"main\" e role=\"contentinfo\", mas nenhum "
     "<nav> ou role=\"navigation\". A única região de navegação que o WAVE encontra na "
     "página é injetada pelo script da Barra de Identidade do Governo Federal e "
     "delimita os links do gov.br. Marcar o menu principal e o menu lateral do campus "
     "como regiões de navegação, o que também elimina os blocos de conteúdo que o "
     "axe-core apontou fora de qualquer região.", "WCAG 1.3.1 (A)"),

    ("Média", "Indicador de foco pouco perceptível sobre fundo branco",
     "O contorno de foco rgb(241,202,127) atinge 5,81:1 sobre o verde do cabeçalho, "
     "mas apenas 1,56:1 sobre o branco da área de conteúdo, onde está a maior parte "
     "dos links. Escurecer o contorno ou acrescentar um traço externo de apoio para "
     "garantir 3:1 em qualquer fundo.", "WCAG 1.4.11 (AA)"),

    ("Média", "Alvos de toque abaixo do mínimo",
     "Na emulação do Pixel 7, 23 dos 58 elementos interativos medem menos de 24 por "
     "24 pixels, entre eles os próprios controles do banner (22x20). Ampliar a área "
     "clicável por meio de preenchimento, sem necessariamente aumentar o texto.",
     "WCAG 2.5.8 (AA, WCAG 2.2)"),

    ("Média", "Layout quebra com espaçamento de texto ampliado",
     "Ao aplicar entrelinha 1,5, espaçamento entre letras de 0,12em e entre palavras "
     "de 0,16em, três elementos têm o conteúdo cortado por overflow oculto. "
     "Substituir alturas fixas por alturas mínimas nos blocos afetados.",
     "WCAG 1.4.12 (AA)"),

    ("Média", "Texto alternativo redundante",
     "Em quatro imagens da página inicial o atributo alt repete literalmente o texto "
     "do link vizinho, levando o leitor de tela a anunciar a mesma informação duas "
     "vezes. Usar alt=\"\" nessas imagens, já que o link adjacente cumpre a função "
     "descritiva.", "WCAG 1.1.1 (A)"),

    ("Baixa", "URL crua como texto de link",
     "Na página institucional de Acessibilidade, dois links exibem o endereço "
     "completo como texto visível, que o leitor de tela soletra caractere a "
     "caractere. Substituir pelo nome do documento de destino.", "WCAG 2.4.4 (A)"),

    ("Baixa", "Página de Acessibilidade desatualizada",
     "A página foi modificada pela última vez em 2020, descreve apenas três dos sete "
     "atalhos existentes, expande a sigla WCAG incorretamente como \"World Content "
     "Accessibility Guide\" e não declara nível de conformidade. Mais grave: não "
     "menciona Libras nem o VLibras em nenhum momento, embora o portal ofereça o "
     "tradutor em todas as páginas — quem procura o recurso não é informado de que "
     "ele existe. Registrou-se ainda que o script collective.lazysizes referenciado "
     "pelas páginas responde HTTP 404. Atualizar o conteúdo, anunciar o VLibras e "
     "publicar a declaração de conformidade prevista pelo eMAG.",
     "eMAG 3.1"),

    ("Baixa", "Marcação provisória da Barra do Governo em estado degradado",
     "Enquanto o barra.brasil.gov.br/barra.js não carrega, o portal exibe o bloco "
     "provisório <div id=\"barra-brasil\" style=\"background:#7F7F7F\"> com o texto "
     "\"Atualize sua Barra de Governo\". Esse bloco tem largura fixa e, em tela de 320 "
     "pixels, é o único elemento a transbordar — o conteúdo passa a ocupar 330 pixels "
     "e surge rolagem horizontal; seu texto branco sobre o cinza #7F7F7F mede 4,0:1. "
     "Com o script carregado nada disso ocorre, de modo que não há falha de "
     "conformidade a registrar; o defeito pertence ao estado degradado, que se "
     "manifesta sempre que o domínio federal está indisponível ou bloqueado na rede "
     "do usuário. Dar ao bloco provisório largura fluida e contraste suficiente.",
     "WCAG 1.4.10 / 1.4.3 (AA), apenas em estado degradado"),
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

    "BRASIL. Ministério da Gestão e da Inovação em Serviços Públicos. VLibras - suíte de "
    "ferramentas de tradução automática do Português para a Libras. Disponível em: "
    "https://www.gov.br/governodigital/pt-br/vlibras. Acesso em: \x02DATA\x02.",

    "CEWEB.BR. Cartilha de Acessibilidade na Web - Fascículo III: Metodologias e ferramentas "
    "de avaliação. São Paulo: Comitê Gestor da Internet no Brasil, 2019. Disponível em: "
    "https://ceweb.br/guias/cartilha-de-acessibilidade-na-web-fasciculo-iii/. Acesso em: \x02DATA\x02.",

    "CEWEB.BR. Cartilha de Acessibilidade na Web - Fascículo IV: O papel dos usuários na "
    "avaliação de acessibilidade. São Paulo: Comitê Gestor da Internet no Brasil, 2020. "
    "Disponível em: https://ceweb.br/cartilhas/cartilha-w3cbr-acessibilidade-web-fasciculo-IV/. "
    "Acesso em: \x02DATA\x02.",

    "DEQUE SYSTEMS. axe-core: accessibility engine for automated Web UI testing, versão "
    "4.10.2. Disponível em: https://github.com/dequelabs/axe-core. Acesso em: \x02DATA\x02.",

    "IBGE. Censo Demográfico 2022: Pessoas com deficiência. Rio de Janeiro: Instituto "
    "Brasileiro de Geografia e Estatística, 2023.",

    "MWPT. 15 checklists de acessibilidade essenciais para quem desenvolve canais digitais. "
    "Disponível em: https://mwpt.com.br/15-checklists-de-acessibilidade-essenciais-para-quem-"
    "desenvolve-canais-digitais/. Acesso em: \x02DATA\x02.",

    "W3C. Web Content Accessibility Guidelines (WCAG) 2.1. W3C Recommendation, 5 jun. 2018. "
    "Disponível em: https://www.w3.org/TR/WCAG21/. Acesso em: \x02DATA\x02.",

    "W3C. Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 5 out. 2023. "
    "Disponível em: https://www.w3.org/TR/WCAG22/. Acesso em: \x02DATA\x02.",

    "W3C BRASIL. Diretrizes de Acessibilidade para Conteúdo Web (WCAG) 2.1 - tradução "
    "autorizada para o português do Brasil. Disponível em: "
    "https://www.w3c.br/traducoes/wcag/wcag21-pt-BR/. Acesso em: \x02DATA\x02.",

    "WEBAIM. WAVE Web Accessibility Evaluation Tool. Utah State University. Disponível em: "
    "https://wave.webaim.org/. Acesso em: \x02DATA\x02.",
]
