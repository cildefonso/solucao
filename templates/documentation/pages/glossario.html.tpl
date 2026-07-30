<!--
  Template: glossario.html
  Produtor: solucao-docs-storyteller
  Page ID: glossario
  Categoria solucao: diagram
  Dados consumidos: assets/data/soul.json (derivado de .solucao/soul.md)

  Marcadores:
  - GLOSSARY_SEARCH: input de busca cliente-side
  - GLOSSARY_CARDS: cards de conceitos
  - SCRIPTS: inline JS para busca e filtro
-->

<!-- PAYLOAD_START -->
<section class="solucao-doc-glossary">
    <header class="solucao-doc-glossary-header">
        <label for="glossary-search" class="visually-hidden">Buscar conceito</label>
        <input
            type="search"
            id="glossary-search"
            placeholder="Buscar conceito..."
            autocomplete="off"
        >
        <!-- GLOSSARY_SEARCH -->
    </header>
    <div class="solucao-doc-glossary-grid" id="glossary-grid">
        <!-- GLOSSARY_CARDS -->
    </div>
</section>
<!-- PAYLOAD_END -->
