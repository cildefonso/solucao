<!--
  Template: timeline.html
  Produtor: solucao-docs-analyst
  Skill invocada: highcharts-visualizer (Highcharts Timeline)
  Page ID: timeline
  Categoria solucao: diagram
  Dados consumidos: assets/data/timeline.json (derivado de .solucao/chronicle.md)

  Marcadores:
  - HEAD_EXTRAS: <script src="assets/vendor/highcharts.js"></script>
                 + <script src="assets/vendor/highcharts-accessibility.js"></script>
                 + <script src="assets/vendor/highcharts-timeline.js"></script>
                 (todos baixados pelo Publisher via vendor-pins.yaml,
                  highcharts@11.4.8)
  - CHART_TIMELINE: container da timeline
  - EVENT_DETAILS: painel lateral com detalhes do evento clicado
  - SCRIPTS: monta a timeline a partir de window.RV_DATA.timeline (sem fetch local)
-->

<!-- PAYLOAD_START -->
<section class="solucao-doc-timeline" data-layout="split">
    <div class="solucao-doc-timeline-stage">
        <div id="chart-timeline"><!-- CHART_TIMELINE --></div>
    </div>
    <aside class="solucao-doc-timeline-details" aria-live="polite">
        <h2>Detalhes do evento</h2>
        <div id="event-details">
            <!-- EVENT_DETAILS -->
            <p class="solucao-doc-empty-hint">Clique em um evento na timeline para ver detalhes.</p>
        </div>
    </aside>
</section>
<!-- PAYLOAD_END -->
