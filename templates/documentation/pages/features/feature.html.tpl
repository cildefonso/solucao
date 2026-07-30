<!--
  Template: features/<spec-id>.html
  Produtor: solucao-docs-storyteller
  Page ID: feature-<id>
  Categoria solucao: diagram
  Dados consumidos: _solucao_sdd/<spec>/requirements.md + design.md + tasks.md

  Padrão: "How a Feature Works" (TL;DR + accordion + snippets em abas).

  Marcadores:
  - FEATURE_TLDR: 2 a 4 linhas resumindo o que a feature faz
  - FEATURE_ACCORDION: seções colapsáveis (Requisitos, Design, Tasks, Code Snippets)
  - FEATURE_TABS: abas com trechos de código relevantes
-->

<!-- PAYLOAD_START -->
<article class="solucao-doc-feature">
    <section class="solucao-doc-feature-tldr">
        <h2>TL;DR</h2>
        <p><!-- FEATURE_TLDR --></p>
    </section>

    <section class="solucao-doc-feature-accordion">
        <!-- FEATURE_ACCORDION -->
        <details open>
            <summary>Requisitos</summary>
            <div data-section="requirements"><!-- FEATURE_REQUIREMENTS --></div>
        </details>
        <details>
            <summary>Design</summary>
            <div data-section="design"><!-- FEATURE_DESIGN --></div>
        </details>
        <details>
            <summary>Tasks</summary>
            <div data-section="tasks"><!-- FEATURE_TASKS --></div>
        </details>
    </section>

    <section class="solucao-doc-feature-tabs" hidden>
        <h2>Snippets relevantes</h2>
        <!-- FEATURE_TABS -->
    </section>
</article>
<!-- PAYLOAD_END -->
