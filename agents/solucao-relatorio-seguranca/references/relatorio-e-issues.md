# Relatório e issues — contrato de dados e especificação

Carregue nas FASES 6 e 7 de `/hm-security-report`.

O relatório **não é escrito à mão**. Você escreve `achados.json`; `gerar_relatorio.py` projeta o PDF a partir dele. Isso garante que o documento entregue e a lista do chat nunca divirjam, e que o relatório possa ser regerado depois de uma correção sem refazer a auditoria.

---

## 1. Contrato do `achados.json`

Molde preenchido: `assets/achados.exemplo.json`. Codificação UTF-8. Datas em ISO `YYYY-MM-DD`.

### Cabeçalho

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `projeto` | string | **sim** | Nome real do projeto; entra no título e no cabeçalho de todas as páginas |
| `data` | string ISO | não | Ausente = data de hoje |
| `escopo` | array de string | sim na prática | O que foi auditado, com números ("backend/ (41 handlers)") |
| `stack` | objeto | sim na prática | Chaves livres: `linguagem`, `framework`, `orm`, `auth`, `frontend`, `deploy` |
| `nota_metodologica` | string | sim na prática | Como cada categoria foi mapeada para esta stack; declare explicitamente se houve amostragem |
| `mapeamento_categorias` | array | sim na prática | `{categoria, equivalente_stack, como_verificado}` |
| `cobertura` | objeto | sim na prática | Chaves livres; valores string ou array. É a prova numérica da auditoria |
| `resumo_executivo` | string | não | 3–4 frases. O que um CTO precisa saber em 20 segundos |

### `achados[]`

| Campo | Obrigatório | Regra |
|---|---|---|
| `id` | sim | `F-01`, `F-02`... Estável: recomendações e issues referenciam por ele |
| `categoria` | sim | `banco-sem-tranca`, `permissao-no-navegador`, `idor`, `chaves-expostas`, `xss` |
| `titulo` | sim | Uma linha, descritiva, sem jargão vago ("Listagem de contratos ignora a organização") |
| `severidade` | **validado** | `critica`, `alta`, `media`, `baixa`, `informativa` — sem acento, minúsculo |
| `arquivo` | **validado** | Caminho relativo à raiz do repositório |
| `linhas` | **validado** | `"48"` ou `"48-53"`. Número exato, nunca aproximado |
| `trecho` | sim na prática | Código **literal**, copiado. Segredos reais mascarados |
| `por_que_exploravel` | **validado** | O mecanismo, não o rótulo. Quem explora, com qual requisição |
| `impacto` | sim na prática | Consequência de negócio, não técnica |
| `condicoes_exploracao` | sim na prática | Flags, config, variável ausente. "Nenhuma" quando for direto |
| `correcao` | sim na prática | Concreta e específica ao código |
| `criterios_aceite` | não | Lista verificável; se ausente, a issue automática usa um padrão |
| `nao_acionavel` | não | `true` exclui o achado da geração automática de issues |

Os quatro campos marcados **validado** são checados pelo gerador: falta de qualquer um **aborta** a geração com código 2 e lista as pendências. É proposital — o portão anti-especulação vive no código, não na boa vontade.

### Seções qualitativas

- `pontos_fortes[]` — `{titulo, evidencia, arquivos[]}`. A `evidencia` cita arquivo e linhas. É a prova de cobertura.
- `pontos_fracos[]` — `{titulo, descricao}` (aceita string simples). São os riscos centrais, não a repetição da lista de achados.
- `categorias_nao_aplicaveis[]` — `{categoria, motivo}`. Preencha em vez de forçar achado.
- `recomendacoes[]` — `{prioridade, acao, achados[], esforco}`. `P1` = antes de qualquer exposição externa.
- `issues[]` — vazio para geração automática (ver adiante).

---

## 2. Especificação do PDF

Fixada em `gerar_relatorio.py`; altere só com motivo.

**Formato.** A4, margens 2 cm. Cabeçalho com nome do relatório e data; rodapé com nome e "Página X de Y". A capa não leva cabeçalho nem rodapé.

**Paleta (contrato, não sugestão):**

| Uso | Cor |
|---|---|
| Crítica | `#B91C1C` |
| Alta | `#EA580C` |
| Média | `#D97706` |
| Baixa | `#2563EB` |
| Informativa | `#64748B` |
| Ponto forte | `#059669` |

**Seções, nesta ordem:** capa (fundo escuro, título, data, escopo, stack, método) → escopo e metodologia (stack, mapeamento por categoria, cobertura) → resumo executivo (tabela por severidade, rosca por severidade, barras empilhadas por categoria) → pontos fortes e fracos → achados detalhados por categoria (tabela `Severidade | Arquivo:linha | Descrição` + cartão por achado com trecho, explorabilidade, impacto, condições e correção) → recomendações priorizadas → issues para o GitHub.

**Tipografia.** DejaVu Sans / DejaVu Sans Mono, embutidas via matplotlib — sempre presentes e com acentuação completa. Fallback silencioso para Helvetica/Courier.

---

## 3. Portão de verificação

```bash
.venv-audit/Scripts/python docs/security-audit/verificar_relatorio.py --pdf docs/security-audit/relatorio-auditoria-seguranca.pdf
```

Reprova automaticamente: página quase vazia, bloco fora das margens, texto sobre o rodapé, menos de dois gráficos embutidos, seção obrigatória ausente, paginação ausente. Saída 0 = limpo, 1 = defeitos, 2 = erro.

O que a máquina **não** julga e você precisa olhar nos PNGs de `_verificacao/`: legibilidade dos rótulos dos gráficos, tabela apertada demais, quebra de página infeliz no meio de um cartão, sobra grosseira de espaço. Corrija antes de entregar.

---

## 4. Issues para o GitHub

Deixe `issues: []` e o gerador cria uma issue por achado acionável (exclui `informativa` e `nao_acionavel`), ordenadas por severidade. Preencha `issues[]` manualmente quando quiser **agrupar**.

**Quando agrupar:** achados triviais do mesmo tema e mesma correção — três defaults de segredo em compose, Helm e CI viram uma issue "Remover defaults de segredo e validar no startup". **Quando não agrupar:** severidades diferentes, arquivos sem relação, ou correções independentes. Uma issue crítica nunca é diluída dentro de um lote.

Formato de cada bloco no PDF — delimitado para copiar e colar inteiro:

```
--- ISSUE 1 ---
Título: [Segurança] <descrição curta da falha>
Labels: security, severidade:critica

## Problema
<por que é explorável — o mecanismo>

## Evidência
`caminho/do/arquivo.ext:48-53`
<trecho de código>

## Impacto
<consequência de negócio>

## Condições de exploração
<flags, config, ou "Nenhuma">

## Sugestão de correção
<concreta, específica ao código>

## Critérios de aceite
- [ ] <verificável>
- [ ] <teste que falha antes da correção>
--- FIM ISSUE 1 ---
```

Estrutura de `issues[]` quando manual: `{numero, titulo, labels[], corpo_markdown}`. `corpo_markdown` é inserido literalmente entre os delimitadores.

**Critério de aceite bom vs ruim.** Ruim: "corrigir a falha". Bom: "teste de integração com dois inquilinos comprova que A não enxerga registros de B, e o teste falha se o predicado for removido". O critério tem que ser verificável por alguém que não participou da auditoria.
