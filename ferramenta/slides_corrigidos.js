// Slides corrigidos para o deck do Kelven.
// Tokens amostrados por pixel do PDF original para casar exatamente.
const pptxgen = require("pptxgenjs");

const BG = "071A2F", CARD = "0B2B45", CARD2 = "0A2842";
const CIANO = "4BD1E4", CLARO = "F7FBFD", BRANCO = "FFFFFF";
const VERM = "FF6B6B", AMAR = "F5C85B", VERDE = "4ED68E";
const MUTED = "6B8AA6", LINHA = "16486A";
const FONTE = "Calibri";
const W = 13.333, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.defineSlideMaster({ title: "BASE", background: { color: BG } });

// Moldura repetida em todos os slides do deck original.
function chrome(s, secao, titulo, numero) {
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: W, h: 0.085, fill: { color: CIANO } });
  s.addText(secao, {
    x: 0.55, y: 0.38, w: 6, h: 0.28, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 10.5, bold: true, color: CIANO, charSpacing: 2.2,
  });
  s.addText(titulo, {
    x: 0.55, y: 0.72, w: 12.2, h: 0.95, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 32, bold: true, color: BRANCO, fit: "shrink",
  });
  s.addText("AVALIAÇÃO DE ACESSIBILIDADE WEB · WCAG 2.1", {
    x: 0.4, y: 7.02, w: 7, h: 0.28, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 8.5, bold: true, color: MUTED, charSpacing: 0.8,
  });
  s.addText("IFAL · CAMPUS MACEIÓ", {
    x: 8.4, y: 7.02, w: 4.2, h: 0.28, isTextBox: true, margin: 0, align: "right",
    fontFace: FONTE, fontSize: 8.5, bold: true, color: MUTED, charSpacing: 0.8,
  });
  s.addText(String(numero), {
    x: 12.75, y: 7.02, w: 0.45, h: 0.28, isTextBox: true, margin: 0, align: "right",
    fontFace: FONTE, fontSize: 9, color: MUTED,
  });
}

function card(s, x, y, w, h, cor) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.06, fill: { color: cor || CARD },
  });
}

// Bloco de número grande com rótulo ao lado, como nos slides 7 e 9 do original.
function stat(s, x, y, w, h, valor, rotulo, cor) {
  card(s, x, y, w, h);
  s.addText(valor, {
    x: x + 0.35, y: y + 0.12, w: 2.3, h: h - 0.24, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 30, bold: true, color: cor, valign: "middle",
  });
  s.addText(rotulo, {
    x: x + 2.75, y: y + 0.12, w: w - 3.05, h: h - 0.24, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 14, bold: true, color: CLARO, valign: "middle",
  });
}

// ─────────────────────────────────────────────────── slide novo: WAVE e ASES
const sA = pres.addSlide({ masterName: "BASE" });
chrome(sA, "05 · AVALIADORES OFICIAIS", "O que o WAVE e o ASES apontaram", 8);

// ASES à esquerda
card(sA, 0.55, 1.95, 6.0, 4.75);
sA.addText("ASES · GOVERNO FEDERAL · eMAG 3.1", {
  x: 0.9, y: 2.2, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 10.5, bold: true, color: CIANO, charSpacing: 1.4,
});
sA.addText("90,48%", {
  x: 0.9, y: 2.6, w: 5.3, h: 0.95, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 54, bold: true, color: VERDE,
});
sA.addText("de aderência ao modelo brasileiro", {
  x: 0.9, y: 3.5, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 13, color: CLARO,
});
sA.addShape(pres.ShapeType.rect, { x: 0.9, y: 3.95, w: 5.3, h: 0.014, fill: { color: LINHA } });

const secoes = [
  ["Marcação", "29", "236"], ["Comportamento", "0", "5"],
  ["Conteúdo / Informação", "11", "69"], ["Apresentação / Design", "0", "0"],
  ["Multimídia", "0", "0"], ["Formulários", "0", "0"],
];
const COL_SEC = 0.9, COL_ERR = 4.25, COL_AVI = 5.25, LARG_NUM = 0.85;
[["Seção do eMAG", COL_SEC, 3.3, "left"], ["Erros", COL_ERR, LARG_NUM, "right"],
 ["Avisos", COL_AVI, LARG_NUM, "right"]].forEach(([t, x, w, al]) => {
  sA.addText(t, { x, y: 4.12, w, h: 0.26, isTextBox: true, margin: 0, align: al,
                  fontFace: FONTE, fontSize: 10.5, bold: true, color: MUTED });
});
secoes.forEach((r, i) => {
  const y = 4.44 + i * 0.32;
  sA.addText(r[0], { x: COL_SEC, y, w: 3.3, h: 0.3, isTextBox: true, margin: 0,
                     fontFace: FONTE, fontSize: 12, color: CLARO });
  sA.addText(r[1], { x: COL_ERR, y, w: LARG_NUM, h: 0.3, isTextBox: true, margin: 0,
                     align: "right", fontFace: FONTE, fontSize: 12, bold: true,
                     color: r[1] === "0" ? MUTED : VERM });
  sA.addText(r[2], { x: COL_AVI, y, w: LARG_NUM, h: 0.3, isTextBox: true, margin: 0,
                     align: "right", fontFace: FONTE, fontSize: 12, bold: true,
                     color: r[2] === "0" ? MUTED : AMAR });
});
sA.addText("Total: 40 erros · 310 avisos", {
  x: 0.9, y: 6.36, w: 5.3, h: 0.28, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 11.5, bold: true, color: CLARO,
});

// WAVE à direita
card(sA, 6.8, 1.95, 6.0, 2.85);
sA.addText("WAVE · WebAIM", {
  x: 7.15, y: 2.2, w: 5.3, h: 0.3, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 10.5, bold: true, color: CIANO, charSpacing: 1.4,
});
const wave = [
  ["4", "erros", VERM], ["21", "contraste", VERM], ["32", "alertas", AMAR],
  ["16", "recursos", VERDE], ["42", "estruturais", CIANO], ["0", "ARIA", MUTED],
];
wave.forEach((it, i) => {
  const col = i % 3, lin = Math.floor(i / 3);
  sA.addText(it[0], {
    x: 7.15 + col * 1.8, y: 2.62 + lin * 0.95, w: 1.7, h: 0.5, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 26, bold: true, color: it[2],
  });
  sA.addText(it[1], {
    x: 7.15 + col * 1.8, y: 3.08 + lin * 0.95, w: 1.7, h: 0.28, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 11.5, color: CLARO,
  });
});

card(sA, 6.8, 5.05, 6.0, 1.65, CARD2);
sA.addText("ATENÇÃO NA LEITURA", {
  x: 7.15, y: 5.28, w: 5.3, h: 0.28, isTextBox: true, margin: 0,
  fontFace: FONTE, fontSize: 10, bold: true, color: AMAR, charSpacing: 1.4,
});
sA.addText(
  "Os 4 erros do WAVE não estão no código do IFAL: vêm da Barra do Governo Federal, " +
  "injetada por barra.brasil.gov.br, que tem 1 imagem sem alt e 2 âncoras vazias.",
  { x: 7.15, y: 5.6, w: 5.3, h: 0.95, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 12, color: CLARO }
);
sA.addNotes(
  "Slide novo. O deck não trazia nenhum número do WAVE nem do ASES, embora a equipe " +
  "tenha rodado os dois — e a professora pediu explicitamente o uso de avaliador. " +
  "A nota de 90,48% convive com 310 avisos porque o ASES pondera por gravidade e a " +
  "maior parte dos avisos cai na recomendação 1.1, de peso menor."
);

// ─────────────────────────────────────────────────────── slide 9 corrigido
const s9 = pres.addSlide({ masterName: "BASE" });
chrome(s9, "07 · MOBILE", "Quando a tela fica estreita, o problema aparece", 9);

card(s9, 0.55, 1.95, 5.5, 4.75);
s9.addImage({
  path: "/home/user/atividades/evidencias/telas/08-reflow-320px.png",
  x: 2.51, y: 2.2, w: 1.58, h: 3.95,
});
s9.addText(
  [
    { text: "330 px de conteúdo", options: { bold: true, color: VERM } },
    { text: "  em uma tela de 320 px  →  rolagem horizontal", options: { color: CLARO } },
  ],
  { x: 0.85, y: 6.2, w: 4.9, h: 0.35, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 13, align: "center" }
);

stat(s9, 6.35, 1.95, 6.45, 1.05, "23", "alvos interativos < 24×24 px", AMAR);
stat(s9, 6.35, 3.18, 6.45, 1.05, "4", "reprovações de contraste confirmadas", VERM);
stat(s9, 6.35, 4.41, 6.45, 1.05, "1,66:1", "pior razão medida na tela", VERM);
stat(s9, 6.35, 5.64, 6.45, 1.05, "412×915", "viewport do Pixel 7 emulado", CIANO);
s9.addNotes(
  "Números conferidos contra o relatório. As reprovações de contraste são 4, medidas por " +
  "amostragem de pixels; a pior é 1,66:1 nos botões do banner. A versão anterior deste " +
  "slide trazia 7/51 e 1:1, que eram falsos positivos de um método que supunha o fundo " +
  "subindo a árvore do DOM."
);

// ─────────────────────────────────────────────────────── slide 13 corrigido
const s13 = pres.addSlide({ masterName: "BASE" });
chrome(s13, "11 · FECHAMENTO", "O que fica desta avaliação?", 13);

const fechos = [
  ["01", "Aparência ≠ acessibilidade",
   "As barreiras estão na marcação e são invisíveis para quem enxerga a página."],
  ["02", "Automação ≠ experiência",
   "As ferramentas quantificam o código; só o teste humano revela o uso real."],
  ["03", "Correções viáveis",
   "Botão de pausa, um h1 por página e ajuste de paleta: baixo custo, alto impacto."],
  ["04", "Acessibilidade contínua",
   "Cada publicação pode reintroduzir barreiras; reavaliar periodicamente."],
];
fechos.forEach((f, i) => {
  const x = 0.55 + i * 3.16;
  card(s13, x, 1.95, 2.96, 3.85);
  s13.addText(f[0], {
    x: x + 0.3, y: 2.2, w: 2.4, h: 0.32, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 13, bold: true, color: CIANO,
  });
  s13.addText(f[1], {
    x: x + 0.3, y: 2.6, w: 2.4, h: 0.85, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 18, bold: true, color: BRANCO,
  });
  s13.addText(f[2], {
    x: x + 0.3, y: 3.52, w: 2.4, h: 1.7, isTextBox: true, margin: 0,
    fontFace: FONTE, fontSize: 12.5, color: CLARO,
  });
});
card(s13, 0.55, 6.05, 12.25, 0.68, CARD2);
s13.addText(
  "Acessibilidade se projeta desde o início — corrigir depois custa mais.",
  { x: 0.55, y: 6.05, w: 12.25, h: 0.68, isTextBox: true, margin: 0, align: "center",
    valign: "middle", fontFace: FONTE, fontSize: 15, bold: true, color: CIANO }
);
s13.addNotes(
  "O sinal de diferente estava com resíduo de fonte no deck original: 'Visual ≠] acessível'."
);

pres.writeFile({ fileName: "/home/user/atividades/apresentacao/SLIDES_CORRIGIDOS.pptx" })
  .then((f) => console.log("gerado:", f));
