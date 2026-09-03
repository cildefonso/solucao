#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador do PDF de auditoria (Higher Mind / hm-security-report).

Nao existe entrega sem verificacao. Este script:
  1. confere que o PDF abre, quantas paginas tem e qual o titulo/metadata;
  2. detecta paginas em branco ou quase vazias (defeito de quebra de fluxo);
  3. detecta texto que transbordou as margens (defeito de tabela larga demais);
  4. confirma que os graficos foram embutidos (imagens por pagina);
  5. confirma que todas as secoes obrigatorias existem;
  6. rasteriza cada pagina em PNG para inspecao visual pelo agente.

Uso:
    python verificar_relatorio.py --pdf docs/security-audit/relatorio-auditoria-seguranca.pdf

Saida: relatorio no stdout + PNGs em <pasta-do-pdf>/_verificacao/pagina-NN.png
Codigo de saida 0 = sem defeitos; 1 = defeitos encontrados; 2 = erro de execucao.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARGEM_PT = 56.7  # 2 cm em pontos
TOLERANCIA_PT = 6.0  # folga antes de acusar transbordo


def verificar(caminho_pdf: Path, dpi: int = 110, rasterizar: bool = True) -> int:
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
    except ImportError:
        try:
            import fitz  # nome legado
        except ImportError:
            print("[erro] PyMuPDF nao instalado. Rode: pip install pymupdf", file=sys.stderr)
            return 2

    if not caminho_pdf.exists():
        print(f"[erro] PDF nao encontrado: {caminho_pdf}", file=sys.stderr)
        return 2

    doc = fitz.open(str(caminho_pdf))
    defeitos = []
    dir_saida = caminho_pdf.parent / "_verificacao"
    if rasterizar:
        dir_saida.mkdir(parents=True, exist_ok=True)

    print(f"Arquivo ......: {caminho_pdf}")
    print(f"Tamanho ......: {caminho_pdf.stat().st_size / 1024:.1f} KB")
    print(f"Paginas ......: {doc.page_count}")
    print(f"Titulo .......: {doc.metadata.get('title', '')}")
    print(f"Autor ........: {doc.metadata.get('author', '')}")
    print("-" * 74)
    print(f"{'Pag':>4}  {'Chars':>6}  {'Imgs':>4}  {'Larg x Alt (pt)':>18}  Observacao")

    total_imagens = 0
    for indice, pagina in enumerate(doc, start=1):
        texto = pagina.get_text("text").strip()
        imagens = pagina.get_images(full=True)
        total_imagens += len(imagens)
        caixa = pagina.rect
        observacoes = []

        # 1. pagina vazia / quase vazia (a capa e legitimamente curta)
        if indice > 1 and len(texto) < 60 and not imagens:
            observacoes.append("PAGINA QUASE VAZIA")
            defeitos.append(f"pagina {indice}: quase vazia ({len(texto)} chars, 0 imagens)")

        if indice > 1:
            # 2. transbordo horizontal do conteudo
            for bloco in pagina.get_text("blocks"):
                x0, x1 = bloco[0], bloco[2]
                if x1 > caixa.width - MARGEM_PT + TOLERANCIA_PT or x0 < MARGEM_PT - TOLERANCIA_PT:
                    observacoes.append("TRANSBORDO HORIZONTAL")
                    defeitos.append(f"pagina {indice}: bloco fora das margens (x0={x0:.0f}, x1={x1:.0f})")
                    break
            # 3. texto invadindo o rodape
            for bloco in pagina.get_text("blocks"):
                if bloco[3] > caixa.height - 22:
                    observacoes.append("TEXTO SOBRE O RODAPE")
                    defeitos.append(f"pagina {indice}: texto invade o rodape (y1={bloco[3]:.0f})")
                    break

        print(
            f"{indice:>4}  {len(texto):>6}  {len(imagens):>4}  "
            f"{caixa.width:>7.1f} x {caixa.height:<7.1f}  {'; '.join(dict.fromkeys(observacoes)) or 'ok'}"
        )

        if rasterizar:
            pix = pagina.get_pixmap(dpi=dpi)
            pix.save(str(dir_saida / f"pagina-{indice:02d}.png"))

    print("-" * 74)

    # 4. graficos presentes
    if total_imagens < 2:
        defeitos.append(f"graficos ausentes: apenas {total_imagens} imagem(ns) embutida(s), esperado >= 2")

    # 5. secoes obrigatorias presentes
    texto_completo = "\n".join(p.get_text("text") for p in doc)
    obrigatorias = [
        "Escopo e metodologia",
        "Resumo executivo",
        "Pontos fortes",
        "Achados detalhados",
        "Recomendações priorizadas",
        "Issues para o GitHub",
    ]
    for secao in obrigatorias:
        if secao.lower() not in texto_completo.lower():
            defeitos.append(f"secao ausente no PDF: '{secao}'")

    # 6. paginacao aplicada
    if doc.page_count > 1 and "Página 2 de" not in texto_completo:
        defeitos.append("rodape de paginacao ausente ('Pagina X de Y')")

    doc.close()

    if rasterizar:
        print(f"PNGs de verificacao: {dir_saida}")
    if defeitos:
        print(f"\n[FALHA] {len(defeitos)} defeito(s):")
        for d in defeitos:
            print(f"  - {d}")
        return 1
    print("\n[OK] Nenhum defeito estrutural detectado. Inspecione os PNGs para o julgamento visual.")
    return 0


def principal(argv=None) -> int:
    p = argparse.ArgumentParser(description="Verifica o PDF do relatorio de auditoria.")
    p.add_argument("--pdf", default="docs/security-audit/relatorio-auditoria-seguranca.pdf")
    p.add_argument("--dpi", type=int, default=110, help="resolucao da rasterizacao")
    p.add_argument("--sem-raster", action="store_true", help="nao gerar PNGs")
    args = p.parse_args(argv)
    return verificar(Path(args.pdf), dpi=args.dpi, rasterizar=not args.sem_raster)


if __name__ == "__main__":
    raise SystemExit(principal())
