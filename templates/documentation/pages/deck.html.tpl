<!--
  Template: deck.html
  Produtor: solucao-docs-storyteller
  Page ID: deck
  Categoria solucao: diagram
  Dados consumidos: assets/data/soul.json + features-index.json + (opcional) metrics.json

  Marcadores:
  - DECK_SLIDES: 6 a 10 slides (capa, conceitos, módulos, métricas, features, encerramento)
  - SCRIPTS: navegação por setas + fullscreen + indicador

  Mínimo viável (greenfield): 4 slides (capa, glossário, 1 feature destaque, encerramento).
-->

<!-- PAYLOAD_START -->
<section class="solucao-doc-deck" data-mode="presentation">
    <ol class="solucao-doc-deck-slides" id="deck-slides">
        <!-- DECK_SLIDES -->
    </ol>
    <nav class="solucao-doc-deck-nav" aria-label="Navegação do deck">
        <button type="button" data-action="prev" aria-label="Slide anterior">&larr;</button>
        <span class="solucao-doc-deck-counter" data-current="1" data-total="0">1 / 0</span>
        <button type="button" data-action="next" aria-label="Próximo slide">&rarr;</button>
        <button type="button" data-action="fullscreen" aria-label="Tela cheia">⛶</button>
    </nav>
</section>
<!-- PAYLOAD_END -->
