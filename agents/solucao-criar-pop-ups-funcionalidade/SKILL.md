---
name: solucao-criar-pop-ups-funcionalidade
description: "Implementa no frontend Angular legado um pop-up acessível para selecionar um item quando a funcionalidade atual retornar múltiplos resultados. Antes de iniciar, solicita ao usuário o arquivo principal, o HTML de referência visual, a mensagem que dispara o comportamento e os campos do filtro da funcionalidade atual que executará o pop-up. Use quando o usuário mencionar múltiplos resultados, seleção de item, campos de filtro, pop-up ou modal."
---
# Angular: criar pop-ups de funcionalidade

## Objetivo

Alterar a funcionalidade Angular `consultar-beneficios` para que, quando uma pesquisa por CPF retornar mais de um benefício, o sistema abra um pop-up de seleção. Depois que o usuário selecionar um benefício, o fluxo deve continuar usando o benefício escolhido, sem exigir uma nova consulta manual por NB ou NIT.

## Arquivo principal informado

Antes de inspecionar o projeto, solicitar ao usuário o caminho do **Arquivo principal informado**. Não assumir um caminho padrão e não iniciar alterações enquanto o caminho não for fornecido.

Pergunta obrigatória:

> Informe o caminho do arquivo principal da funcionalidade que deve receber o pop-up.

Depois da resposta:

1. validar que o arquivo informado existe;
2. usar esse arquivo como ponto de partida da inspeção;
3. identificar os arquivos relacionados (TypeScript, estilos, service, modelos e testes) a partir dele;
4. se o caminho não existir ou não for acessível, informar a limitação e solicitar um caminho válido ou o conteúdo do arquivo.

O caminho abaixo é apenas um exemplo para esta funcionalidade e nunca deve ser presumido:

```text
C:\desenv\XPTO-frontend\src\app\features\atual-funcionalidade\nova-funcionalidade
.html
```

## Arquivo Referência visual/HTML informada

Antes de inspecionar ou alterar a interface, solicitar ao usuário o caminho do **Arquivo Referência visual/HTML informada**. Não assumir um arquivo de referência e não iniciar a implementação visual do pop-up enquanto esse caminho não for fornecido.

Pergunta obrigatória:

> Informe o caminho do arquivo de referência visual/HTML que deve orientar a implementação do pop-up.

Depois da resposta:

1. validar que o arquivo informado existe e está acessível;
2. revisar sua estrutura, estilos e padrões visuais antes de implementar o pop-up;
3. usar esse arquivo como referência de UI, sem copiar conteúdo ou estrutura inexistente para o projeto;
4. se o caminho não existir ou não for acessível, informar a limitação e solicitar um caminho válido ou o conteúdo do arquivo.

O caminho abaixo é apenas um exemplo para esta funcionalidade e nunca deve ser presumido:

```text
C:\desenv\XPTO-frontend\src\app\features\nova-funcionalidade\index.html
```

## Mensagem atual que dispara o novo comportamento

Antes de implementar a regra de abertura do pop-up, solicitar ao usuário a **Mensagem atual que dispara o novo comportamento**. Não assumir uma mensagem padrão.

Pergunta obrigatória:

> Informe a mensagem atualmente apresentada que deve disparar o novo comportamento do pop-up.

Depois da resposta:

1. localizar a mensagem no arquivo principal, no fluxo de consulta e/ou no contrato da API;
2. confirmar se ela representa um caso funcional de múltiplos resultados;
3. usar a mensagem apenas como compatibilidade quando a API não fornecer uma coleção estruturada;
4. se a mensagem não for localizada, informar a limitação e solicitar a origem do comportamento ou um exemplo de resposta da API.

A mensagem abaixo é apenas um exemplo para esta funcionalidade e nunca deve ser presumida:

```text
Mais de um benefício encontrado para o CPF informado. Consulte por NB ou NIT.
```

O arquivo principal, o arquivo de referência visual e a mensagem de disparo são entradas obrigatórias. Antes de editar, validá-los no ambiente e no fluxo funcional. Se algum não estiver disponível, informar a limitação e solicitar o caminho, conteúdo ou contexto correspondente, sem inventar a estrutura real.

## Resultado esperado

Quando houver exatamente um benefício:

1. manter o comportamento atual;
2. carregar ou navegar para os dados desse benefício.

Quando houver mais de um benefício:

1. não exibir a mensagem como erro impeditivo;
2. abrir um pop-up/modal;
3. listar todos os benefícios retornados;
4. permitir selecionar exatamente um item;
5. permitir confirmar ou cancelar;
6. continuar o fluxo com o benefício confirmado;
7. preservar CPF, NB, NIT e demais identificadores disponíveis no retorno.

Quando nenhum benefício for encontrado:

1. manter o tratamento funcional já existente;
2. não abrir o modal.

## Fluxo obrigatório

Usar os seguintes parâmetros durante todo este fluxo:

- **[FUNCIONALIDADE_ATUAL]**: nome da funcionalidade informado pelo usuário ou identificado a partir do arquivo principal;
- **[CAMPOS_FILTRO]**: campos do filtro da funcionalidade atual, informados pelo usuário;
- **[ARQUIVO_PRINCIPAL]**, **[HTML_REFERENCIA]** e **[MENSAGEM_DISPARO]**: entradas obrigatórias já solicitadas nesta skill.

Antes de continuar, solicitar os parâmetros ausentes:

> Informe o nome da funcionalidade atual e os campos utilizados no filtro que executa a consulta.

Não usar nomes, campos, rotas, mensagens, modelos ou regras de uma funcionalidade anterior como padrão. Todas as etapas abaixo devem ser adaptadas aos parâmetros fornecidos pelo usuário e ao código real de **[FUNCIONALIDADE_ATUAL]**.

### 1. Inspecionar o projeto

Após obter e validar os parâmetros obrigatórios, localizar e revisar, no mínimo:

- o arquivo principal informado pelo usuário;
- o componente TypeScript relacionado a **[ARQUIVO_PRINCIPAL]**;
- arquivo de estilos do componente;
- service, facade ou use case acionado pelos **[CAMPOS_FILTRO]**;
- interfaces de request e response;
- módulo Angular ou configuração `standalone`;
- biblioteca de modal já adotada no projeto;
- testes existentes;
- arquivo de referência visual/HTML informado pelo usuário.

Não assumir Angular Material, Bootstrap, PrimeNG ou design system específico. Reutilizar a solução já adotada no projeto. Se não houver modal existente, implementar um componente Angular próprio e acessível.

### 2. Identificar o contrato real da API

Antes de escrever o código, descobrir no response:

- campo que contém a coleção de itens retornados;
- identificador técnico e campos necessários para selecionar um item;
- campos do item que correspondem aos **[CAMPOS_FILTRO]**, quando aplicável;
- campos apresentados no **[HTML_REFERENCIA]**;
- dados necessários para continuar o fluxo após a seleção;
- estrutura usada para erros funcionais.

Não detectar múltiplos itens apenas pelo texto da mensagem quando a coleção estiver disponível. A condição principal deve ser baseada na quantidade do array retornado.

A mensagem pode ser usada como compatibilidade temporária somente se o backend legado não devolver a coleção de forma estruturada. Nesse caso, registrar a limitação.

### 3. Definir o modelo de seleção

Criar ou reutilizar uma interface fortemente tipada. Exemplo adaptável:

```typescript
export interface ItemSelecionavel {
  id?: string;
  // Declarar os campos reais de [FUNCIONALIDADE_ATUAL]
}
```

Os nomes finais devem corresponder ao contrato real encontrado no projeto.

### 4. Implementar o componente do pop-up

Preferir componente dedicado, por exemplo:

```text
<funcionalidade-atual>/
├── <componente-principal>.html
├── <componente-principal>.ts
├── <componente-principal>.scss
└── selecionar-item-dialog/
  ├── selecionar-item-dialog.component.html
  ├── selecionar-item-dialog.component.ts
  ├── selecionar-item-dialog.component.scss
  └── selecionar-item-dialog.component.spec.ts
```

O pop-up deve conter os campos, rótulos, ordem, agrupamentos e elementos visuais presentes no **Arquivo Referência visual/HTML informada** fornecido pelo usuário. Antes de implementar, inventariar esses elementos no HTML de referência e mapear cada campo para o contrato real da API.

Além dos elementos do HTML de referência, garantir:

- lista ou tabela responsiva quando a referência apresentar uma coleção de itens;
- seleção exclusiva por radio button, linha selecionável ou mecanismo equivalente presente na referência;
- ações de cancelar e confirmar/continuar conforme a nomenclatura e o comportamento da referência;
- ação de confirmação inicialmente desabilitada enquanto não houver seleção;
- fechamento por `Escape`, se compatível com a biblioteca;
- foco inicial no título ou primeiro elemento interativo;
- devolução do objeto selecionado ao componente chamador.

Não adicionar campos de domínio fixos apenas por este documento. Exibir os campos quando estiverem no **[HTML_REFERENCIA]** e forem fornecidos pelo contrato da API. Caso algum campo da referência não esteja disponível no retorno, preservar o layout e apresentar um valor de ausência adequado, sem inventar dados.

### 5. Alterar o fluxo da funcionalidade

A lógica deve seguir este padrão conceitual:

```typescript
private tratarResultado(resultado: RespostaDaFuncionalidade): void {
  const itens = resultado.itens ?? [];

  if (itens.length === 0) {
    this.tratarNenhumResultado(resultado);
    return;
  }

  if (itens.length === 1) {
    this.processarItemSelecionado(itens[0]);
    return;
  }

  this.abrirSelecaoDeItem(itens);
}
```

Depois da confirmação:

```typescript
private processarItemSelecionado(item: ItemSelecionavel): void {
  // Reutilizar o fluxo existente de [FUNCIONALIDADE_ATUAL].
}
```

Não duplicar a lógica acionada pelos **[CAMPOS_FILTRO]**. Extrair o processamento atual para um método reutilizável e chamá-lo tanto no caso de um único item quanto após a seleção no modal.

### 6. Preservar o comportamento existente

- Não quebrar os fluxos existentes executados pelos **[CAMPOS_FILTRO]**.
- Preservar as validações, máscaras e regras específicas desses campos.
- Não alterar contratos de service sem necessidade.
- Não duplicar subscriptions.
- Não introduzir subscribe aninhado se o projeto usa RxJS.
- Manter loading, tratamento de erro e finalização.
- Evitar abrir mais de um modal para a mesma resposta.
- Limpar seleção ao iniciar uma nova consulta.

### 7. Acessibilidade e responsividade

Garantir:

- `role="dialog"` e `aria-modal="true"` quando modal próprio;
- título associado por `aria-labelledby`;
- labels acessíveis para radio buttons;
- navegação por teclado;
- foco visível;
- retorno de foco ao elemento que abriu o modal;
- tabela com scroll horizontal em telas pequenas;
- botões com texto explícito;
- estados não informados apenas por cor.

### 8. Tratamento de dados e segurança

- Não registrar valores dos **[CAMPOS_FILTRO]** ou identificadores sensíveis em logs de produção.
- Não inserir valores dos filtros em mensagens de erro desnecessárias.
- Escapar conteúdo apresentado pelo template Angular.
- Não usar `innerHTML` para renderizar dados da API.
- Não persistir a seleção em `localStorage` ou `sessionStorage` sem requisito explícito.

### 9. Testes obrigatórios

Criar ou atualizar testes, adaptados a **[FUNCIONALIDADE_ATUAL]** e aos **[CAMPOS_FILTRO]**, para:

1. nenhum item retornado;
2. exatamente um item retornado;
3. mais de um item retornado;
4. abertura do modal;
5. lista completa apresentada;
6. botão Continuar desabilitado sem seleção;
7. seleção de um item;
8. confirmação usando o item correto;
9. cancelamento sem continuar o fluxo;
10. preservação das consultas realizadas pelos campos do filtro;
11. fechamento e limpeza ao iniciar nova consulta;
12. erro técnico da API;
13. loading encerrado em sucesso e erro;
14. comportamento com campos opcionais ausentes.

### 10. Validação antes da entrega

Executar os comandos compatíveis com o projeto, preferencialmente:

```bash
npm test -- --watch=false
npm run lint
npm run build
```

Se o projeto usar Angular CLI diretamente:

```bash
npx ng test --watch=false
npx ng build
```

Usar apenas scripts realmente existentes no `package.json`. Registrar comandos, resultados e limitações. Não afirmar sucesso de testes que não foram executados.

## Critérios de aceite

- Pesquisa por CPF com um benefício continua funcionando.
- Pesquisa por CPF com múltiplos benefícios abre o pop-up.
- Todos os benefícios retornados aparecem como opções.
- Apenas um benefício pode ser selecionado.
- Continuar fica desabilitado até existir seleção.
- Confirmar executa o fluxo com o benefício escolhido.
- Cancelar não executa consulta de detalhe.
- A mensagem antiga deixa de bloquear o usuário quando a lista de benefícios estiver disponível.
- Consultas por NB e NIT permanecem funcionais.
- Pop-up é responsivo e utilizável por teclado.
- Testes, lint e build são executados quando disponíveis.

## Arquivos de saída

Entregar:

1. arquivos Angular completos alterados;
2. novos componentes completos;
3. testes completos;
4. resumo das mudanças;
5. evidências de comandos e resultados;
6. lista de premissas e limitações;
7. solicitar ao usuário o local da criação da nova funcionalidade ou criar no projeto corrente.

## Regras de qualidade

- Retornar arquivos completos, não somente fragments ou diffs, salvo pedido contrário.
- Seguir o padrão de nomenclatura e arquitetura já presente no repositório.
- Não inventar imports, tipos, selectors ou APIs.
- Confirmar versões no `package.json` antes de usar recursos específicos do Angular.
- Não substituir componentes corporativos existentes por bibliotecas novas sem necessidade.
- Corrigir erros de compilação encontrados durante a implementação.
