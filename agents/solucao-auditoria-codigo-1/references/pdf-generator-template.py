#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script modelo para geração autônoma do Relatório de Auditoria de Segurança em PDF.
Utiliza ReportLab e Matplotlib em ambiente virtual isolado.
"""

import os
import sys
from io import BytesIO
from datetime import datetime

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas
except ImportError:
    print("[!] Dependências ausentes. Execute em ambiente com: pip install reportlab matplotlib")
    sys.exit(1)

# Paleta Estrita de Cores
COR_CRITICA = colors.HexColor("#B91C1C")
COR_ALTA = colors.HexColor("#EA580C")
COR_MEDIA = colors.HexColor("#D97706")
COR_BAIXA = colors.HexColor("#2563EB")
COR_PONTO_FORTE = colors.HexColor("#059669")
COR_TEXTO = colors.HexColor("#1E293B")
COR_SUBTEXTO = colors.HexColor("#64748B")
COR_FUNDO_CARD = colors.HexColor("#F8FAFC")
COR_BORDA = colors.HexColor("#E2E8F0")

class NumberedCanvas(canvas.Canvas):
    """Canvas customizado para incluir cabeçalho e rodapé com número total de páginas."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_elements(self, page_count):
        if self._pageNumber == 1:
            return  # Não desenhar cabeçalho/rodapé na capa

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COR_SUBTEXTO)

        # Cabeçalho
        self.drawString(2 * cm, A4[1] - 1.5 * cm, "Relatório de Auditoria de Segurança — Código-Fonte e Configurações")
        self.setStrokeColor(COR_BORDA)
        self.setLineWidth(0.5)
        self.line(2 * cm, A4[1] - 1.6 * cm, A4[0] - 2 * cm, A4[1] - 1.6 * cm)

        # Rodapé
        self.line(2 * cm, 1.8 * cm, A4[0] - 2 * cm, 1.8 * cm)
        self.drawString(2 * cm, 1.3 * cm, "CONFIDENCIAL — Uso Interno de Engenharia e Segurança")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 2 * cm, 1.3 * cm, page_str)
        self.restoreState()

def gerar_grafico_rosca(severidades):
    """Gera gráfico de rosca com distribuição de severidades."""
    labels = []
    sizes = []
    color_map = {
        'Crítica': '#B91C1C',
        'Alta': '#EA580C',
        'Média': '#D97706',
        'Baixa': '#2563EB'
    }
    cores = []

    for k, v in severidades.items():
        if v > 0:
            labels.append(f"{k} ({v})")
            sizes.append(v)
            cores.append(color_map.get(k, '#94A3B8'))

    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=200)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.0f%%', startangle=90,
        colors=cores, textprops=dict(color="#1E293B", size=8),
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_weight('bold')
        at.set_color('white')

    ax.axis('equal')
    plt.title("Achados por Severidade", fontsize=10, weight='bold', color="#1E293B", pad=10)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def gerar_grafico_barras(categorias):
    """Gera gráfico de barras horizontais por categoria."""
    nomes = list(categorias.keys())
    qtds = list(categorias.values())
    cores = ['#B91C1C' if q > 0 else '#059669' for q in qtds]

    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=200)
    y_pos = range(len(nomes))
    ax.barh(y_pos, qtds, color=cores, height=0.55, edgecolor='none')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(nomes, fontsize=8, color="#1E293B")
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.tick_params(axis='x', colors='#64748B', labelsize=8)
    ax.set_xlabel("Total de Apontamentos", fontsize=8, color="#64748B")
    plt.title("Apontamentos por Dimensão", fontsize=10, weight='bold', color="#1E293B", pad=10)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def compilar_relatorio_pdf(destino_pdf, dados_auditoria):
    """Monta o documento PDF com base no dicionário de dados da auditoria."""
    os.makedirs(os.path.dirname(os.path.abspath(destino_pdf)), exist_ok=True)
    doc = SimpleDocTemplate(
        destino_pdf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    style_titulo = ParagraphStyle('CapaTitulo', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=COR_TEXTO)
    style_subtitulo = ParagraphStyle('CapaSub', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=COR_SUBTEXTO)
    style_h1 = ParagraphStyle('Heading1Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=COR_TEXTO, spaceAfter=8)
    style_corpo = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=COR_TEXTO)
    style_code = ParagraphStyle('CodeCustom', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10, textColor=COR_TEXTO)

    story = []

    # CAPA
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(f"Relatório de Auditoria de Segurança", style_titulo))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(f"<b>Projeto:</b> {dados_auditoria['projeto']} | <b>Data:</b> {dados_auditoria['data']}", style_subtitulo))
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=3, color=COR_ALTA, spaceBefore=0, spaceAfter=15))
    story.append(Paragraph(f"<b>Escopo Auditado:</b> {dados_auditoria['escopo']}", style_corpo))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(f"<b>Nota Metodológica:</b> {dados_auditoria['nota_metodologica']}", style_corpo))
    story.append(PageBreak())

    # RESUMO EXECUTIVO COM GRÁFICOS
    story.append(Paragraph("1. Resumo Executivo e Gráficos de Postura", style_h1))
    story.append(Paragraph("A análise sistemática avaliou as 5 dimensões críticas de segurança do código-fonte e configurações.", style_corpo))
    story.append(Spacer(1, 0.4 * cm))

    rosca_buf = gerar_grafico_rosca(dados_auditoria['severidades'])
    barras_buf = gerar_grafico_barras(dados_auditoria['categorias'])

    img_rosca = Image(rosca_buf, width=7.5 * cm, height=5.5 * cm)
    img_barras = Image(barras_buf, width=8.5 * cm, height=5.5 * cm)

    tabela_graficos = Table([[img_rosca, img_barras]], colWidths=[8.5 * cm, 8.5 * cm])
    tabela_graficos.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(tabela_graficos)
    story.append(Spacer(1, 0.6 * cm))

    # PONTOS FORTES
    story.append(Paragraph("2. Pontos Fortes e Defesas Validadas", style_h1))
    for pf in dados_auditoria['pontos_fortes']:
        txt = f"<font color='#059669'><b>✔ [APROVADO]</b></font> {pf}"
        story.append(Paragraph(txt, style_corpo))
        story.append(Spacer(1, 0.2 * cm))

    story.append(Spacer(1, 0.6 * cm))

    # ACHADOS DETALHADOS
    story.append(Paragraph("3. Tabela Consolidada de Achados", style_h1))
    tabela_dados = [["ID", "Sev.", "Localização", "Descrição da Vulnerabilidade"]]
    for item in dados_auditoria['achados']:
        tabela_dados.append([
            item['id'],
            item['severidade'],
            item['local'],
            Paragraph(item['descricao'], style_corpo)
        ])

    tabela_achados = Table(tabela_dados, colWidths=[2 * cm, 2 * cm, 5 * cm, 8 * cm])
    tabela_achados.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COR_FUNDO_CARD),
        ('TEXTCOLOR', (0, 0), (-1, 0), COR_TEXTO),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, COR_BORDA),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tabela_achados)
    story.append(PageBreak())

    # SEÇÃO ISSUES PARA O GITHUB
    story.append(Paragraph("4. Pacote de Issues Prontas para o GitHub", style_h1))
    story.append(Paragraph("Copie os blocos abaixo e cole diretamente na aba 'Issues' do repositório.", style_corpo))
    story.append(Spacer(1, 0.4 * cm))

    for idx, iss in enumerate(dados_auditoria['issues'], start=1):
        bloco_texto = f"""--- ISSUE {idx} ---<br/>
<b>### [Segurança] {iss['titulo']}</b><br/>
<b>Labels:</b> {iss['labels']}<br/><br/>
<b>#### Descrição do Problema:</b><br/>{iss['descricao']}<br/><br/>
<b>#### Evidência:</b><br/>- Arquivo: {iss['arquivo']}<br/><br/>
<b>#### Impacto:</b><br/>{iss['impacto']}<br/><br/>
<b>#### Critérios de Aceite:</b><br/>{iss['criterios']}<br/>
--- FIM ISSUE {idx} ---"""

        card_issue = Table([[Paragraph(bloco_texto, style_corpo)]], colWidths=[17 * cm])
        card_issue.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COR_FUNDO_CARD),
            ('BOX', (0, 0), (-1, -1), 1, COR_BORDA),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(card_issue)
        story.append(Spacer(1, 0.4 * cm))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Relatório PDF gerado com sucesso em: {destino_pdf}")

if __name__ == "__main__":
    exemplo_dados = {
        'projeto': 'Exemplo Backend',
        'data': datetime.now().strftime('%d/%m/%Y'),
        'escopo': 'Repositório completo (Controllers, DAOs, Services e Configs)',
        'nota_metodologica': 'Mapeamento das 5 dimensões contra Quarkus 3.30+ e Hibernate Panache.',
        'severidades': {'Crítica': 0, 'Alta': 1, 'Média': 2, 'Baixa': 1},
        'categorias': {
            '1. Banco Sem Tranca': 0,
            '2. Permissão Navegador': 1,
            '3. IDOR': 0,
            '4. Chaves Expostas': 2,
            '5. Inputs/XSS': 1
        },
        'pontos_fortes': [
            'Autenticação OIDC integrada com validação centralizada de tokens.',
            'Queries nativas utilizam parâmetros nomeados contra SQL Injection.'
        ],
        'achados': [
            {
                'id': 'SEC-001',
                'severidade': 'ALTA',
                'local': 'src/main/resources/application.properties:15',
                'descricao': 'Credencial de OIDC com secret default sem validação em tempo de startup.'
            }
        ],
        'issues': [
            {
                'titulo': 'Remover credencial default de OIDC e exigir variável de ambiente',
                'labels': 'security, high-severity',
                'descricao': 'A aplicação inicializa com segredo default hardcoded.',
                'arquivo': 'src/main/resources/application.properties:15',
                'impacto': 'Bypass de autenticação em caso de deploy não configurado.',
                'criterios': '- [ ] Bloquear subida da aplicação se secret for default.<br/>- [ ] Validar no ambiente de testes.'
            }
        ]
    }
    destino = sys.argv[1] if len(sys.argv) > 1 else "relatorio-auditoria-seguranca.pdf"
    compilar_relatorio_pdf(destino, exemplo_dados)
