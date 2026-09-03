#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Relatorio de Auditoria de Seguranca (Higher Mind / hm-security-report).

Le um arquivo de achados em JSON (contrato em references/04-schema-achados.md)
e produz um PDF A4 em pt-BR com capa, resumo executivo com graficos, pontos
fortes/fracos, tabelas de achados por categoria, recomendacoes priorizadas e a
secao final "ISSUES PARA O GITHUB" pronta para copiar e colar.

Uso:
    python gerar_relatorio.py \
        --achados docs/security-audit/achados.json \
        --saida   docs/security-audit/relatorio-auditoria-seguranca.pdf

O script e deterministico: mesmo JSON => mesmo PDF. Regere a vontade.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.lib.utils import ImageReader  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas as pdfcanvas  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)

# --------------------------------------------------------------------------
# Paleta e tokens visuais (contrato do relatorio - nao alterar sem motivo)
# --------------------------------------------------------------------------
PALETA = {
    "critica": "#B91C1C",
    "alta": "#EA580C",
    "media": "#D97706",
    "baixa": "#2563EB",
    "informativa": "#64748B",
    "forte": "#059669",
}
TINTA = "#0F172A"
GRAFITE = "#334155"
CINZA = "#64748B"
LINHA = "#E2E8F0"
FUNDO_SUAVE = "#F8FAFC"
CAPA_FUNDO = "#0B1220"
CAPA_ACENTO = "#38BDF8"

ORDEM_SEV = ["critica", "alta", "media", "baixa", "informativa"]
ROTULO_SEV = {
    "critica": "Crítica",
    "alta": "Alta",
    "media": "Média",
    "baixa": "Baixa",
    "informativa": "Informativa",
}

CATEGORIAS = {
    "banco-sem-tranca": ("1. Banco sem tranca — isolamento de inquilino/dono", "Isolamento\nde tenant"),
    "permissao-no-navegador": ("2. Permissão definida no navegador", "Autorização\nno servidor"),
    "idor": ("3. IDOR — objeto por ID sem verificação de posse", "IDOR"),
    "chaves-expostas": ("4. Chaves expostas — segredos hardcoded", "Segredos\nexpostos"),
    "xss": ("5. Inputs sem tratamento — XSS e injeção em template", "XSS /\nsanitização"),
}

MARGEM = 2 * cm
LARGURA = A4[0] - 2 * MARGEM  # 17 cm

FONTE = "Helvetica"
FONTE_B = "Helvetica-Bold"
FONTE_I = "Helvetica-Oblique"
MONO = "Courier"
MONO_B = "Courier-Bold"


# --------------------------------------------------------------------------
# Fontes: usa as TTF que acompanham o matplotlib (sempre presentes, acentuadas)
# --------------------------------------------------------------------------
def registrar_fontes() -> None:
    global FONTE, FONTE_B, FONTE_I, MONO, MONO_B
    base = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    familias = {
        "HM": (
            "DejaVuSans.ttf",
            "DejaVuSans-Bold.ttf",
            "DejaVuSans-Oblique.ttf",
            "DejaVuSans-BoldOblique.ttf",
        ),
        "HMMono": (
            "DejaVuSansMono.ttf",
            "DejaVuSansMono-Bold.ttf",
            "DejaVuSansMono-Oblique.ttf",
            "DejaVuSansMono-BoldOblique.ttf",
        ),
    }
    try:
        for familia, (r, b, i, bi) in familias.items():
            pdfmetrics.registerFont(TTFont(familia, str(base / r)))
            pdfmetrics.registerFont(TTFont(f"{familia}-B", str(base / b)))
            pdfmetrics.registerFont(TTFont(f"{familia}-I", str(base / i)))
            pdfmetrics.registerFont(TTFont(f"{familia}-BI", str(base / bi)))
            pdfmetrics.registerFontFamily(
                familia,
                normal=familia,
                bold=f"{familia}-B",
                italic=f"{familia}-I",
                boldItalic=f"{familia}-BI",
            )
        FONTE, FONTE_B, FONTE_I = "HM", "HM-B", "HM-I"
        MONO, MONO_B = "HMMono", "HMMono-B"
    except Exception as erro:  # fallback: fontes base do PDF
        print(f"[aviso] fontes DejaVu indisponiveis ({erro}); usando Helvetica/Courier", file=sys.stderr)


# --------------------------------------------------------------------------
# Estilos
# --------------------------------------------------------------------------
def montar_estilos() -> dict:
    e = {}
    e["capa_kicker"] = ParagraphStyle(
        "capa_kicker", fontName=FONTE_B, fontSize=9, leading=12,
        textColor=colors.HexColor(CAPA_ACENTO), spaceAfter=14,
    )
    e["capa_titulo"] = ParagraphStyle(
        "capa_titulo", fontName=FONTE_B, fontSize=26, leading=31, textColor=colors.white, spaceAfter=6,
    )
    e["capa_sub"] = ParagraphStyle(
        "capa_sub", fontName=FONTE, fontSize=12, leading=17,
        textColor=colors.HexColor("#94A3B8"), spaceAfter=20,
    )
    e["capa_rotulo"] = ParagraphStyle(
        "capa_rotulo", fontName=FONTE_B, fontSize=7.5, leading=10, textColor=colors.HexColor(CAPA_ACENTO),
    )
    e["capa_texto"] = ParagraphStyle(
        "capa_texto", fontName=FONTE, fontSize=8.8, leading=13.5, textColor=colors.HexColor("#CBD5E1"),
    )
    e["h1"] = ParagraphStyle("h1", fontName=FONTE_B, fontSize=15, leading=19, textColor=colors.HexColor(TINTA))
    e["h2"] = ParagraphStyle(
        "h2", fontName=FONTE_B, fontSize=11, leading=15,
        textColor=colors.HexColor(TINTA), spaceBefore=10, spaceAfter=4,
    )
    e["h3"] = ParagraphStyle("h3", fontName=FONTE_B, fontSize=9, leading=12.5, textColor=colors.HexColor(GRAFITE))
    e["corpo"] = ParagraphStyle(
        "corpo", fontName=FONTE, fontSize=9, leading=13.5, textColor=colors.HexColor(GRAFITE), spaceAfter=5,
    )
    e["legenda"] = ParagraphStyle(
        "legenda", fontName=FONTE, fontSize=7.5, leading=10.5, textColor=colors.HexColor(CINZA),
    )
    e["celula"] = ParagraphStyle("celula", fontName=FONTE, fontSize=8, leading=11.5, textColor=colors.HexColor(GRAFITE))
    e["celula_b"] = ParagraphStyle("celula_b", parent=e["celula"], fontName=FONTE_B, textColor=colors.HexColor(TINTA))
    e["celula_mono"] = ParagraphStyle(
        "celula_mono", fontName=MONO, fontSize=7.2, leading=10, textColor=colors.HexColor(TINTA), wordWrap="CJK",
    )
    e["cabecalho_tabela"] = ParagraphStyle(
        "cabecalho_tabela", fontName=FONTE_B, fontSize=7.5, leading=10, textColor=colors.white,
    )
    e["chip"] = ParagraphStyle(
        "chip", fontName=FONTE_B, fontSize=6.6, leading=8.4, textColor=colors.white, alignment=TA_CENTER,
    )
    e["codigo"] = ParagraphStyle("codigo", fontName=MONO, fontSize=6.9, leading=9.4, textColor=colors.HexColor("#1E293B"))
    e["issue"] = ParagraphStyle("issue", fontName=MONO, fontSize=6.9, leading=9.6, textColor=colors.HexColor("#1E293B"))
    return e


# --------------------------------------------------------------------------
# Utilitarios
# --------------------------------------------------------------------------
def limpar(texto) -> str:
    return escape(str(texto or "")).replace("\n", "<br/>")


def quebrar_codigo(trecho: str, largura: int = 104, max_linhas: int = 26) -> str:
    linhas = []
    for bruta in str(trecho or "").replace("\t", "    ").rstrip().split("\n"):
        bruta = bruta.rstrip()
        if not bruta:
            linhas.append("")
            continue
        linhas.extend(
            textwrap.wrap(
                bruta, width=largura, subsequent_indent="  ",
                break_long_words=True, break_on_hyphens=False,
            )
            or [""]
        )
    if len(linhas) > max_linhas:
        linhas = linhas[:max_linhas] + [f"... (+{len(linhas) - max_linhas} linhas — ver arquivo)"]
    return "\n".join(linhas)


def rotulo_categoria(slug: str, curto: bool = False) -> str:
    if slug in CATEGORIAS:
        return CATEGORIAS[slug][1] if curto else CATEGORIAS[slug][0]
    return str(slug or "outros").replace("-", " ").replace("_", " ").strip().capitalize()


def sev(achado: dict) -> str:
    s = str(achado.get("severidade", "informativa")).strip().lower()
    return s if s in ORDEM_SEV else "informativa"


def alvo(achado: dict) -> str:
    arquivo = str(achado.get("arquivo", "")).strip()
    linhas = str(achado.get("linhas", "")).strip()
    return f"{arquivo}:{linhas}" if linhas else arquivo


# --------------------------------------------------------------------------
# Graficos
# --------------------------------------------------------------------------
def grafico_rosca(contagem: dict, caminho: Path) -> Path:
    rotulos, valores, cores = [], [], []
    for s in ORDEM_SEV:
        n = contagem.get(s, 0)
        if n:
            rotulos.append(f"{ROTULO_SEV[s]} — {n}")
            valores.append(n)
            cores.append(PALETA[s])
    total = sum(valores)
    if not valores:
        valores, rotulos, cores = [1], ["Nenhum achado"], [PALETA["forte"]]

    fig, ax = plt.subplots(figsize=(3.4, 3.2), dpi=220)
    fig.patch.set_alpha(0)
    fatias, _ = ax.pie(
        valores, colors=cores, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.40, edgecolor="white", linewidth=2.0),
    )
    ax.text(0, 0.10, str(total), ha="center", va="center", fontsize=24, fontweight="bold", color=TINTA)
    ax.text(0, -0.24, "achados", ha="center", va="center", fontsize=9, color=CINZA)
    ax.legend(
        fatias, rotulos, loc="upper center", bbox_to_anchor=(0.5, 0.04), ncol=2,
        frameon=False, fontsize=9, labelcolor=GRAFITE, handlelength=0.9, columnspacing=1.0,
    )
    ax.set_aspect("equal")
    fig.savefig(caminho, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return caminho


def grafico_barras(por_categoria: dict, caminho: Path) -> Path:
    cats = [c for c in por_categoria]
    if not cats:
        cats = ["sem-achados"]
        por_categoria = {"sem-achados": {}}
    fig, ax = plt.subplots(figsize=(5.0, max(2.2, 0.52 * len(cats) + 1.0)), dpi=220)
    fig.patch.set_alpha(0)
    y = list(range(len(cats)))
    esquerda = [0.0] * len(cats)
    for s in ORDEM_SEV:
        vals = [por_categoria[c].get(s, 0) for c in cats]
        if not any(vals):
            continue
        ax.barh(
            y, vals, left=esquerda, color=PALETA[s], height=0.52,
            label=ROTULO_SEV[s], edgecolor="white", linewidth=0.8,
        )
        esquerda = [e + v for e, v in zip(esquerda, vals)]
    for i, total in enumerate(esquerda):
        if total:
            ax.text(total + 0.09, i, str(int(total)), va="center", ha="left",
                    fontsize=9, color=GRAFITE, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels([rotulo_categoria(c, curto=True) for c in cats], fontsize=8.6, color=GRAFITE)
    ax.invert_yaxis()
    ax.set_xlim(0, max(1.0, max(esquerda) * 1.20))
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(LINHA)
    ax.tick_params(axis="x", colors=CINZA, labelsize=8.6)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", color=LINHA, linewidth=0.7)
    ax.set_axisbelow(True)
    if any(any(v.values()) for v in por_categoria.values()):
        ax.legend(
            frameon=False, fontsize=8.6, ncol=5, loc="upper center",
            bbox_to_anchor=(0.5, 1.16), labelcolor=GRAFITE, handlelength=0.9,
        )
    fig.savefig(caminho, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return caminho


def imagem(caminho: Path, largura_alvo: float):
    leitor = ImageReader(str(caminho))
    lp, ap = leitor.getSize()
    return Image(str(caminho), width=largura_alvo, height=largura_alvo * ap / lp)


# --------------------------------------------------------------------------
# Componentes de layout
# --------------------------------------------------------------------------
def chip(texto: str, cor: str, est, largura: float = 2.0 * cm):
    t = Table([[Paragraph(texto, est["chip"])]], colWidths=[largura])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(cor)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("ROUNDEDCORNERS", [3, 3, 3, 3]),
            ]
        )
    )
    return t


def titulo_secao(texto: str, est, numero: str = None):
    rotulo = f"{numero}. {texto}" if numero else texto
    return KeepTogether(
        [
            Spacer(1, 4),
            HRFlowable(width="100%", thickness=2, color=colors.HexColor(TINTA), spaceAfter=6),
            Paragraph(limpar(rotulo), est["h1"]),
            Spacer(1, 6),
        ]
    )


def bloco_codigo(trecho: str, est, largura: float):
    t = Table([[XPreformatted(escape(quebrar_codigo(trecho)), est["codigo"])]], colWidths=[largura])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(FUNDO_SUAVE)),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor(LINHA)),
                ("LINEBEFORE", (0, 0), (0, -1), 2.2, colors.HexColor("#94A3B8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def estilo_tabela(cor_cabecalho: str = TINTA) -> TableStyle:
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(cor_cabecalho)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor(LINHA)),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFDFF")]),
        ]
    )


# --------------------------------------------------------------------------
# Canvas com paginacao "X de Y" + cabecalho/rodape
# --------------------------------------------------------------------------
class CanvasNumerado(pdfcanvas.Canvas):
    titulo_rodape = "Relatório de Auditoria de Segurança"
    titulo_cabecalho = "Relatório de Auditoria de Segurança"
    subtitulo_cabecalho = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._paginas = []

    def showPage(self):  # noqa: N802 (API do reportlab)
        self._paginas.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._paginas)
        for estado in self._paginas:
            self.__dict__.update(estado)
            self._rodape(total)
            super().showPage()
        super().save()

    def _rodape(self, total: int):
        if self._pageNumber <= 1:  # capa nao leva rodape
            return
        self.saveState()
        self.setStrokeColor(colors.HexColor(LINHA))
        self.setLineWidth(0.5)
        self.line(MARGEM, 1.65 * cm, A4[0] - MARGEM, 1.65 * cm)
        self.setFont(FONTE, 7.2)
        self.setFillColor(colors.HexColor(CINZA))
        self.drawString(MARGEM, 1.20 * cm, self.titulo_rodape)
        self.drawRightString(A4[0] - MARGEM, 1.20 * cm, f"Página {self._pageNumber} de {total}")
        self.restoreState()


def desenhar_capa(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(CAPA_FUNDO))
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor(CAPA_ACENTO))
    canvas.rect(0, A4[1] - 0.42 * cm, A4[0], 0.42 * cm, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor("#1E293B"))
    canvas.setLineWidth(0.6)
    canvas.line(2.4 * cm, 2.2 * cm, A4[0] - 2.4 * cm, 2.2 * cm)
    canvas.setFont(FONTE, 7.5)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(2.4 * cm, 1.65 * cm, "Documento confidencial — distribuição restrita")
    canvas.restoreState()


def desenhar_corpo(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONTE, 7.2)
    canvas.setFillColor(colors.HexColor(CINZA))
    canvas.drawString(MARGEM, A4[1] - 1.35 * cm, getattr(canvas, "titulo_cabecalho", ""))
    canvas.drawRightString(A4[0] - MARGEM, A4[1] - 1.35 * cm, getattr(canvas, "subtitulo_cabecalho", ""))
    canvas.setStrokeColor(colors.HexColor(LINHA))
    canvas.setLineWidth(0.5)
    canvas.line(MARGEM, A4[1] - 1.55 * cm, A4[0] - MARGEM, A4[1] - 1.55 * cm)
    canvas.restoreState()


# --------------------------------------------------------------------------
# Secoes do relatorio
# --------------------------------------------------------------------------
def secao_capa(dados: dict, est) -> list:
    projeto = dados.get("projeto", "projeto")
    data = dados.get("data") or dt.date.today().isoformat()
    escopo = dados.get("escopo") or []
    stack = dados.get("stack") or {}
    nota = str(dados.get("nota_metodologica", "")).strip()

    fluxo = [
        Spacer(1, 3.0 * cm),
        Paragraph("AUDITORIA DE SEGURANÇA DE APLICAÇÃO", est["capa_kicker"]),
        Paragraph(f"Relatório de Auditoria<br/>de Segurança — {limpar(projeto)}", est["capa_titulo"]),
        Paragraph(
            "Cinco falhas críticas: isolamento de dados, autorização no servidor, "
            "IDOR, segredos expostos e sanitização de entrada",
            est["capa_sub"],
        ),
        HRFlowable(width="38%", thickness=2, color=colors.HexColor(CAPA_ACENTO), spaceAfter=18, hAlign="LEFT"),
    ]

    linhas_meta = [
        [Paragraph("DATA", est["capa_rotulo"]), Paragraph(limpar(data), est["capa_texto"])],
        [
            Paragraph("STACK", est["capa_rotulo"]),
            Paragraph(limpar(" · ".join(f"{k}: {v}" for k, v in stack.items() if v)) or "—", est["capa_texto"]),
        ],
        [
            Paragraph("ESCOPO", est["capa_rotulo"]),
            Paragraph(limpar("; ".join(escopo)) if escopo else "—", est["capa_texto"]),
        ],
    ]
    if nota:
        resumo = nota if len(nota) <= 700 else nota[:697].rsplit(" ", 1)[0] + "..."
        linhas_meta.append([Paragraph("MÉTODO", est["capa_rotulo"]), Paragraph(limpar(resumo), est["capa_texto"])])

    tabela = Table(linhas_meta, colWidths=[2.3 * cm, A4[0] - 4.8 * cm - 2.3 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#1E293B")),
            ]
        )
    )
    fluxo.append(tabela)
    return fluxo


def secao_metodologia(dados: dict, est) -> list:
    fluxo = [titulo_secao("Escopo e metodologia", est)]
    nota = str(dados.get("nota_metodologica", "")).strip()
    if nota:
        fluxo.append(Paragraph(limpar(nota), est["corpo"]))

    stack = dados.get("stack") or {}
    if stack:
        fluxo.append(Paragraph("Stack detectada", est["h2"]))
        linhas = [
            [Paragraph(limpar(k.capitalize()), est["celula_b"]), Paragraph(limpar(v), est["celula"])]
            for k, v in stack.items()
            if v
        ]
        t = Table(linhas, colWidths=[4.0 * cm, LARGURA - 4.0 * cm])
        t.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor(LINHA)),
                ]
            )
        )
        fluxo += [t, Spacer(1, 8)]

    mapeamento = dados.get("mapeamento_categorias") or []
    if mapeamento:
        fluxo.append(Paragraph("Mapeamento das categorias para esta stack", est["h2"]))
        linhas = [
            [
                Paragraph("Categoria", est["cabecalho_tabela"]),
                Paragraph("Equivalente nesta stack", est["cabecalho_tabela"]),
                Paragraph("Como foi verificado", est["cabecalho_tabela"]),
            ]
        ]
        for m in mapeamento:
            linhas.append(
                [
                    Paragraph(limpar(rotulo_categoria(m.get("categoria", ""))), est["celula_b"]),
                    Paragraph(limpar(m.get("equivalente_stack", "—")), est["celula"]),
                    Paragraph(limpar(m.get("como_verificado", "—")), est["celula"]),
                ]
            )
        t = Table(linhas, colWidths=[4.6 * cm, 5.0 * cm, LARGURA - 9.6 * cm], repeatRows=1)
        t.setStyle(estilo_tabela())
        fluxo += [t, Spacer(1, 8)]

    cobertura = dados.get("cobertura") or {}
    if cobertura:
        fluxo.append(Paragraph("Cobertura da auditoria", est["h2"]))
        itens = []
        for k, v in cobertura.items():
            valor = ", ".join(map(str, v)) if isinstance(v, list) else v
            itens.append(f"<b>{limpar(k.replace('_', ' ').capitalize())}:</b> {limpar(valor)}")
        fluxo.append(Paragraph("<br/>".join(itens), est["corpo"]))
    return fluxo


def secao_resumo(dados: dict, contagem: dict, por_categoria: dict, dir_assets: Path, est) -> list:
    total = sum(contagem.values())
    fluxo = [titulo_secao("Resumo executivo", est)]

    resumo_txt = dados.get("resumo_executivo")
    if resumo_txt:
        fluxo.append(Paragraph(limpar(resumo_txt), est["corpo"]))

    cabecalho = (
        [Paragraph("Severidade", est["cabecalho_tabela"])]
        + [Paragraph(ROTULO_SEV[s], est["cabecalho_tabela"]) for s in ORDEM_SEV]
        + [Paragraph("Total", est["cabecalho_tabela"])]
    )
    valores = (
        [Paragraph("Achados", est["celula_b"])]
        + [Paragraph(str(contagem.get(s, 0)), est["celula"]) for s in ORDEM_SEV]
        + [Paragraph(f"<b>{total}</b>", est["celula"])]
    )
    t = Table([cabecalho, valores], colWidths=[3.0 * cm] + [(LARGURA - 3.0 * cm) / 6.0] * 6)
    estilo = estilo_tabela()
    for i, s in enumerate(ORDEM_SEV, start=1):
        estilo.add("TEXTCOLOR", (i, 1), (i, 1), colors.HexColor(PALETA[s]))
        estilo.add("FONTNAME", (i, 1), (i, 1), FONTE_B)
    t.setStyle(estilo)
    fluxo += [t, Spacer(1, 14)]

    rosca = grafico_rosca(contagem, dir_assets / "grafico-severidade.png")
    barras = grafico_barras(por_categoria, dir_assets / "grafico-categoria.png")

    esquerda = [Paragraph("Distribuição por severidade", est["h3"]), Spacer(1, 4), imagem(rosca, 6.0 * cm)]
    direita = [Paragraph("Achados por categoria", est["h3"]), Spacer(1, 4), imagem(barras, LARGURA - 6.8 * cm)]
    grade = Table([[esquerda, direita]], colWidths=[6.6 * cm, LARGURA - 6.6 * cm])
    grade.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    fluxo += [grade, Spacer(1, 6)]

    nao_aplicaveis = dados.get("categorias_nao_aplicaveis") or []
    if nao_aplicaveis:
        fluxo.append(Paragraph("Categorias não aplicáveis a esta stack", est["h2"]))
        linhas = [[Paragraph("Categoria", est["cabecalho_tabela"]), Paragraph("Motivo", est["cabecalho_tabela"])]]
        for na in nao_aplicaveis:
            linhas.append(
                [
                    Paragraph(limpar(rotulo_categoria(na.get("categoria", ""))), est["celula_b"]),
                    Paragraph(limpar(na.get("motivo", "—")), est["celula"]),
                ]
            )
        t = Table(linhas, colWidths=[5.6 * cm, LARGURA - 5.6 * cm], repeatRows=1)
        t.setStyle(estilo_tabela(CINZA))
        fluxo.append(t)
    return fluxo


def secao_fortes_fracos(dados: dict, est) -> list:
    fluxo = [titulo_secao("Pontos fortes e pontos fracos", est)]
    fortes = dados.get("pontos_fortes") or []
    fracos = dados.get("pontos_fracos") or []

    fluxo.append(Paragraph("O que está protegido (verificado no código)", est["h2"]))
    if fortes:
        linhas = [
            [
                Paragraph("Status", est["cabecalho_tabela"]),
                Paragraph("Controle verificado", est["cabecalho_tabela"]),
                Paragraph("Evidência", est["cabecalho_tabela"]),
            ]
        ]
        for p in fortes:
            linhas.append(
                [
                    chip("OK", PALETA["forte"], est, largura=1.5 * cm),
                    Paragraph(limpar(p.get("titulo", "—")), est["celula_b"]),
                    Paragraph(limpar(p.get("evidencia", "—")), est["celula"]),
                ]
            )
        t = Table(linhas, colWidths=[1.9 * cm, 5.1 * cm, LARGURA - 7.0 * cm], repeatRows=1)
        t.setStyle(estilo_tabela(PALETA["forte"]))
        fluxo += [t, Spacer(1, 10)]
    else:
        fluxo.append(Paragraph("Nenhum controle verificado como íntegro nesta auditoria.", est["corpo"]))

    fluxo.append(Paragraph("Riscos centrais", est["h2"]))
    if fracos:
        for p in fracos:
            if isinstance(p, dict):
                texto = f"<b>{limpar(p.get('titulo', ''))}</b> — {limpar(p.get('descricao', ''))}"
            else:
                texto = limpar(p)
            fluxo.append(Paragraph(f"• {texto}", est["corpo"]))
    else:
        fluxo.append(Paragraph("Nenhum risco central registrado.", est["corpo"]))
    return fluxo


def cartao_achado(a: dict, est) -> list:
    s = sev(a)
    largura_interna = LARGURA - 0.8 * cm
    topo = Table(
        [
            [
                chip(ROTULO_SEV[s].upper(), PALETA[s], est, largura=2.1 * cm),
                Paragraph(f"<b>{limpar(a.get('id', ''))}</b> — {limpar(a.get('titulo', 'Achado'))}", est["celula_b"]),
            ]
        ],
        colWidths=[2.3 * cm, largura_interna - 2.3 * cm],
    )
    topo.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    partes = [
        topo,
        Paragraph(f"<font face='{MONO}' size='7.4'>{limpar(alvo(a))}</font>", est["legenda"]),
        Spacer(1, 5),
    ]
    if a.get("trecho"):
        partes += [bloco_codigo(a["trecho"], est, largura_interna), Spacer(1, 6)]
    for rotulo, chave in (
        ("Por que é explorável", "por_que_exploravel"),
        ("Impacto", "impacto"),
        ("Condições de exploração", "condicoes_exploracao"),
        ("Correção", "correcao"),
    ):
        valor = a.get(chave)
        if valor:
            partes.append(Paragraph(f"<b>{rotulo}:</b> {limpar(valor)}", est["celula"]))
            partes.append(Spacer(1, 3))

    cartao = Table([[partes]], colWidths=[LARGURA])
    cartao.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor(LINHA)),
                ("LINEBEFORE", (0, 0), (0, -1), 3.0, colors.HexColor(PALETA[s])),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return [cartao, Spacer(1, 9)]


def secao_achados(achados: list, est) -> list:
    fluxo = [titulo_secao("Achados detalhados por categoria", est)]
    if not achados:
        fluxo.append(Paragraph("Nenhum achado registrado.", est["corpo"]))
        return fluxo

    extras = [c for c in dict.fromkeys(a.get("categoria", "outros") for a in achados) if c not in CATEGORIAS]
    for cat in list(CATEGORIAS.keys()) + extras:
        do_grupo = [a for a in achados if a.get("categoria") == cat]
        if not do_grupo:
            continue
        do_grupo.sort(key=lambda a: (ORDEM_SEV.index(sev(a)), str(a.get("id", ""))))
        fluxo.append(Paragraph(limpar(rotulo_categoria(cat)), est["h2"]))
        linhas = [
            [
                Paragraph("Severidade", est["cabecalho_tabela"]),
                Paragraph("Arquivo:linha", est["cabecalho_tabela"]),
                Paragraph("Descrição", est["cabecalho_tabela"]),
            ]
        ]
        for a in do_grupo:
            linhas.append(
                [
                    chip(ROTULO_SEV[sev(a)].upper(), PALETA[sev(a)], est, largura=1.9 * cm),
                    Paragraph(limpar(alvo(a)), est["celula_mono"]),
                    Paragraph(f"<b>{limpar(a.get('id', ''))}</b> {limpar(a.get('titulo', '—'))}", est["celula"]),
                ]
            )
        t = Table(linhas, colWidths=[2.3 * cm, 5.4 * cm, LARGURA - 7.7 * cm], repeatRows=1)
        t.setStyle(estilo_tabela())
        fluxo += [t, Spacer(1, 10)]
        for a in do_grupo:
            fluxo += cartao_achado(a, est)
    return fluxo


def secao_recomendacoes(dados: dict, est) -> list:
    fluxo = [titulo_secao("Recomendações priorizadas", est)]
    recs = dados.get("recomendacoes") or []
    if not recs:
        fluxo.append(Paragraph("Nenhuma recomendação registrada.", est["corpo"]))
        return fluxo
    linhas = [
        [
            Paragraph("Prio.", est["cabecalho_tabela"]),
            Paragraph("Ação", est["cabecalho_tabela"]),
            Paragraph("Achados", est["cabecalho_tabela"]),
            Paragraph("Esforço", est["cabecalho_tabela"]),
        ]
    ]
    for r in recs:
        linhas.append(
            [
                Paragraph(limpar(r.get("prioridade", "—")), est["celula_b"]),
                Paragraph(limpar(r.get("acao", "—")), est["celula"]),
                Paragraph(limpar(", ".join(r.get("achados", []) or [])) or "—", est["celula_mono"]),
                Paragraph(limpar(r.get("esforco", "—")), est["celula"]),
            ]
        )
    t = Table(linhas, colWidths=[1.7 * cm, LARGURA - 7.2 * cm, 3.3 * cm, 2.2 * cm], repeatRows=1)
    t.setStyle(estilo_tabela())
    fluxo.append(t)
    return fluxo


# --------------------------------------------------------------------------
# Issues do GitHub
# --------------------------------------------------------------------------
def issue_automatica(a: dict, numero: int) -> dict:
    s = sev(a)
    criterios = a.get("criterios_aceite") or [
        "Correção aplicada no arquivo e linhas indicados.",
        "Teste automatizado cobre a tentativa de acesso indevido e falha antes da correção.",
        "Nenhuma regressão nos fluxos legítimos.",
    ]
    trecho = quebrar_codigo(a.get("trecho", ""), largura=96, max_linhas=20)
    corpo = (
        "## Problema\n\n"
        f"{a.get('por_que_exploravel', a.get('titulo', ''))}\n\n"
        f"**Categoria:** {rotulo_categoria(a.get('categoria', 'outros'))}  \n"
        f"**Severidade:** {ROTULO_SEV[s]}\n\n"
        "## Evidência\n\n"
        f"`{alvo(a)}`\n\n"
        "```\n"
        f"{trecho}\n"
        "```\n\n"
        "## Impacto\n\n"
        f"{a.get('impacto', '—')}\n\n"
        "## Condições de exploração\n\n"
        f"{a.get('condicoes_exploracao', 'Nenhuma condição especial: explorável no estado atual do código.')}\n\n"
        "## Sugestão de correção\n\n"
        f"{a.get('correcao', '—')}\n\n"
        "## Critérios de aceite\n\n"
        + "\n".join(f"- [ ] {c}" for c in criterios)
    )
    return {
        "numero": numero,
        "titulo": f"[Segurança] {a.get('titulo', 'Falha de segurança')}",
        "labels": ["security", f"severidade:{s}"],
        "corpo_markdown": corpo,
    }


def montar_issues(dados: dict, achados: list) -> list:
    issues = dados.get("issues")
    if issues:
        for i, issue in enumerate(issues, start=1):
            issue.setdefault("numero", i)
        return issues
    acionaveis = [a for a in achados if sev(a) != "informativa" and not a.get("nao_acionavel")]
    acionaveis.sort(key=lambda a: (ORDEM_SEV.index(sev(a)), str(a.get("id", ""))))
    return [issue_automatica(a, i) for i, a in enumerate(acionaveis, start=1)]


def secao_issues(issues: list, est) -> list:
    fluxo = [
        titulo_secao("Issues para o GitHub", est),
        Paragraph(
            "Cada bloco abaixo é o texto completo de uma issue, em Markdown, pronto para copiar e colar. "
            "Os delimitadores marcam o início e o fim de cada issue.",
            est["corpo"],
        ),
        Spacer(1, 6),
    ]
    if not issues:
        fluxo.append(Paragraph("Nenhuma issue acionável gerada.", est["corpo"]))
        return fluxo

    for issue in issues:
        n = issue.get("numero")
        labels = ", ".join(issue.get("labels") or [])
        texto = (
            f"--- ISSUE {n} ---\n"
            f"Título: {issue.get('titulo', '')}\n"
            f"Labels: {labels}\n\n"
            f"{str(issue.get('corpo_markdown', '')).strip()}\n"
            f"--- FIM ISSUE {n} ---"
        )
        # XPreformatted solto (sem Table) para que o bloco possa quebrar entre
        # paginas: envolver em Table criaria um flowable indivisivel e deixaria
        # meia pagina vazia a cada issue.
        fluxo += [
            XPreformatted(escape(quebrar_codigo(texto, largura=102, max_linhas=400)), est["issue"]),
            Spacer(1, 6),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(LINHA), spaceAfter=10),
        ]
    return fluxo


# --------------------------------------------------------------------------
# Orquestracao
# --------------------------------------------------------------------------
def validar(dados: dict) -> list:
    problemas = []
    if not dados.get("projeto"):
        problemas.append("campo obrigatorio ausente: projeto")
    for a in dados.get("achados") or []:
        ident = a.get("id", "<sem id>")
        if not a.get("arquivo"):
            problemas.append(f"{ident}: sem 'arquivo'")
        if not a.get("linhas"):
            problemas.append(f"{ident}: sem 'linhas' (numero exato e obrigatorio)")
        if str(a.get("severidade", "")).lower() not in ORDEM_SEV:
            problemas.append(f"{ident}: severidade invalida '{a.get('severidade')}'")
        if not a.get("por_que_exploravel"):
            problemas.append(f"{ident}: sem 'por_que_exploravel'")
    return problemas


def gerar(caminho_json: Path, caminho_pdf: Path, estrito: bool = True) -> Path:
    dados = json.loads(caminho_json.read_text(encoding="utf-8"))
    problemas = validar(dados)
    if problemas:
        print("[erro] achados.json invalido:" if estrito else "[aviso] achados.json com pendencias:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
        if estrito:
            raise SystemExit(2)

    registrar_fontes()
    est = montar_estilos()

    achados = list(dados.get("achados") or [])
    contagem = {}
    por_categoria = {cat: {} for cat in CATEGORIAS}
    for a in achados:
        s = sev(a)
        contagem[s] = contagem.get(s, 0) + 1
        cat = a.get("categoria", "outros")
        por_categoria.setdefault(cat, {})
        por_categoria[cat][s] = por_categoria[cat].get(s, 0) + 1

    caminho_pdf.parent.mkdir(parents=True, exist_ok=True)
    dir_assets = caminho_pdf.parent / "_assets"
    dir_assets.mkdir(parents=True, exist_ok=True)

    projeto = dados.get("projeto", "projeto")
    titulo = f"Relatório de Auditoria de Segurança — {projeto}"
    CanvasNumerado.titulo_rodape = titulo
    CanvasNumerado.titulo_cabecalho = titulo
    CanvasNumerado.subtitulo_cabecalho = dados.get("data") or dt.date.today().isoformat()

    doc = BaseDocTemplate(
        str(caminho_pdf),
        pagesize=A4,
        title=titulo,
        author="Auditoria de Segurança — hm-security-report",
        subject="Auditoria de segurança de aplicação",
        leftMargin=MARGEM,
        rightMargin=MARGEM,
        topMargin=MARGEM,
        bottomMargin=MARGEM,
    )
    frame_capa = Frame(
        2.4 * cm, 2.4 * cm, A4[0] - 4.8 * cm, A4[1] - 4.8 * cm, id="capa",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    frame_corpo = Frame(
        MARGEM, MARGEM + 0.35 * cm, LARGURA, A4[1] - 2 * MARGEM - 0.9 * cm, id="corpo",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="capa", frames=[frame_capa], onPage=desenhar_capa),
            PageTemplate(id="corpo", frames=[frame_corpo], onPage=desenhar_corpo),
        ]
    )

    fluxo = []
    fluxo += secao_capa(dados, est)
    fluxo += [NextPageTemplate("corpo"), PageBreak()]
    fluxo += secao_metodologia(dados, est)
    fluxo += [Spacer(1, 10)]
    fluxo += secao_resumo(dados, contagem, por_categoria, dir_assets, est)
    fluxo += [Spacer(1, 14)]
    fluxo += secao_fortes_fracos(dados, est)
    fluxo += [PageBreak()]
    fluxo += secao_achados(achados, est)
    fluxo += [Spacer(1, 14)]
    fluxo += secao_recomendacoes(dados, est)
    fluxo += [PageBreak()]
    fluxo += secao_issues(montar_issues(dados, achados), est)

    doc.build(fluxo, canvasmaker=CanvasNumerado)
    print(f"[ok] PDF gerado: {caminho_pdf}")
    print(f"[ok] graficos:   {dir_assets}")
    return caminho_pdf


def principal(argv=None) -> int:
    p = argparse.ArgumentParser(description="Gera o relatorio de auditoria de seguranca em PDF.")
    p.add_argument("--achados", default="docs/security-audit/achados.json", help="JSON de achados")
    p.add_argument("--saida", default="docs/security-audit/relatorio-auditoria-seguranca.pdf", help="PDF de saida")
    p.add_argument("--sem-validacao-estrita", action="store_true", help="Gera mesmo com pendencias no JSON")
    args = p.parse_args(argv)

    caminho_json = Path(args.achados)
    if not caminho_json.exists():
        print(f"[erro] arquivo de achados nao encontrado: {caminho_json}", file=sys.stderr)
        return 2
    gerar(caminho_json, Path(args.saida), estrito=not args.sem_validacao_estrita)
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
