---
name: solucao-image-to-responsive-web-zip
description: Converte uma imagem ou captura de tela de interface em um ZIP completo com HTML, CSS, JavaScript e assets. Inclui reprodução visual responsiva, componentes funcionais, validação estrutural e revisão orientada a risco antes da entrega.
---

# Image to Responsive Web ZIP

## Objetivo

Receber uma imagem de referência e entregar, na mesma resposta, um projeto web executável e editável em ZIP, com HTML5 semântico, CSS responsivo, JavaScript local, assets tratados, validação automatizada e revisão dos arquivos com maior risco de erro.

## Entrada

- Path completo da imagem de referência (PNG, JPG, JPEG ou WEBP).
- Path completo do diretório onde o projeto e o ZIP final devem ser salvos.
- Opcionalmente: tecnologia, resolução, comportamento ou nível de fidelidade desejado.

Se a tecnologia não for informada, usar HTML5, CSS3 e JavaScript sem frameworks e sem dependências externas.

### Coleta obrigatória dos paths

- Antes de iniciar a conversão, confirmar que foram informados tanto o path da imagem quanto o path de destino.
- Se um ou ambos estiverem ausentes, perguntar ao usuário pelos paths que faltam e aguardar a resposta antes de inspecionar ou criar arquivos.
- Aceitar paths absolutos locais; verificar que a imagem existe, tem formato suportado e pode ser lida, e que o diretório de destino pode ser criado ou gravado.
- Se algum path não existir ou não puder ser acessado, explicar qual falhou e pedir ao usuário um path válido. Não escolher um arquivo ou diretório substituto por conta própria.
- Usar o path de destino informado como diretório de entrega e manter nele somente o ZIP final, conforme a etapa de empacotamento.

## Estrutura padrão

```text
projeto/
├── index.html
├── README.md
└── assets/
    ├── css/styles.css
    ├── js/app.js
    └── images/
```

## Fluxo obrigatório

### 1. Inspecionar a imagem

1. Usar o path da imagem fornecido pelo usuário e validar que o arquivo existe e pode ser lido.
2. Registrar dimensões e formato.
3. Examinar cabeçalho, navegação, banner, textos, formulários, cards, tabelas, gráficos, acordeões, rodapé, cores, tipografia, bordas, sombras e espaçamentos.
4. Identificar comportamentos prováveis e estados responsivos.
5. Não inventar integrações reais nem dados sensíveis.

### 2. Planejar

Definir:

- HTML semântico;
- tokens CSS;
- breakpoints para desktop, tablet e celular;
- componentes interativos;
- assets que podem ser recortados;
- requisitos de acessibilidade;
- estratégia de validação e revisão de risco.

### 3. Preparar o projeto

- Trabalhar em diretório temporário.
- Manter somente o ZIP final no diretório de entrega.
- Usar nomes de arquivos descritivos, minúsculos e caminhos relativos.

### 4. Gerar assets

- Recortar somente fotografias, banners, logotipos ou elementos reutilizáveis.
- Não usar a captura completa como página de fundo.
- Recriar controles e layout com HTML/CSS.
- Preservar proporção e evitar redimensionamento destrutivo.
- Preferir PNG para conteúdo gráfico/textual e JPEG/WebP para fotografias quando apropriado.
- Se a qualidade de um recorte for baixa, registrar a limitação no README.

### 5. Criar HTML

O arquivo `index.html` deve:

- usar `lang="pt-BR"`, salvo pedido diferente;
- conter `meta charset` e `meta viewport`;
- usar `header`, `nav`, `main`, `section`, `form`, `table` e `footer` quando aplicável;
- associar `label` a campos;
- usar textos legíveis da referência;
- usar IDs únicos;
- possuir âncoras com destinos existentes;
- referenciar CSS, JS e imagens por caminhos relativos;
- funcionar localmente.

### 6. Criar CSS

O CSS deve:

- usar variáveis em `:root`;
- reproduzir proporções, cores e hierarquia visual;
- usar Grid e Flexbox;
- incluir breakpoints para tablet e celular;
- tratar overflow de tabelas e conteúdos largos;
- manter foco visível;
- respeitar `prefers-reduced-motion`;
- evitar dependências de CDN;
- evitar dimensões rígidas que quebrem o layout.

### 7. Criar JavaScript funcional

Quando compatível com a imagem, implementar:

- menu móvel;
- máscara e validação de formulário;
- limpeza de campos;
- abas e acordeões;
- filtros locais;
- modais;
- downloads locais demonstrativos;
- toast ou mensagem de feedback.

Regras:

- Não depender de backend.
- Não executar chamadas externas.
- Confirmar que cada seletor usado existe no HTML.
- Confirmar que o JavaScript passa em `node --check` quando Node.js estiver disponível.
- Ao gerar JavaScript por Python, usar strings raw ou escaping correto para regex como `\D` e `\d`, evitando warnings de escape na etapa geradora.

### 8. Criar README

Documentar:

- objetivo;
- estrutura;
- execução;
- funcionalidades;
- dados simulados;
- ausência de backend;
- limitações de fidelidade e resolução dos assets;
- compatibilidade esperada dos recursos CSS usados.

### 9. Validar estrutura e links

Executar `scripts/validate_project.py <pasta>` e depois `scripts/validate_project.py <zip>`.

A validação deve conferir:

- integridade do ZIP;
- arquivos obrigatórios;
- IDs duplicados;
- referências `src` e `href`;
- âncoras internas;
- URLs de assets no CSS;
- seletores simples de ID usados no JavaScript;
- sintaxe JavaScript;
- integridade e dimensões das imagens;
- presença de `meta viewport` e media queries;
- ausência de caminhos absolutos locais;
- ausência de arquivos temporários no ZIP.

### 10. Revisar arquivos com maior risco de erro

Após a validação automática, executar uma revisão dirigida e registrar o resultado em `RISK-REVIEW.md` dentro do projeto.

#### Risco alto: `assets/js/app.js`

Verificar:

- sintaxe;
- seletores sem elementos correspondentes;
- listeners duplicados;
- acesso a elementos nulos;
- regex e escapes;
- manipulação incorreta de `hidden`, `aria-expanded` e classes;
- downloads e modais;
- dependências externas acidentais.

#### Risco alto: `index.html`

Verificar:

- tags não fechadas;
- IDs duplicados;
- labels e campos;
- links internos quebrados;
- caminhos de assets;
- ordem de carregamento do JavaScript;
- semântica e acessibilidade básica.

#### Risco médio: `assets/css/styles.css`

Verificar:

- `url(...)` quebrados;
- overflow horizontal;
- breakpoints ausentes ou conflitantes;
- contraste e foco;
- regras rígidas incompatíveis com celular;
- compatibilidade de recursos como `conic-gradient`;
- imagens esticadas ou pixelizadas.

#### Risco médio: assets de imagem

Verificar:

- corrupção;
- formato real versus extensão;
- dimensões muito pequenas para displays de alta densidade;
- proporção;
- peso excessivo;
- cortes com textos ou bordas indesejadas.

#### Risco baixo: README e empacotamento

Verificar:

- instruções corretas;
- ausência de segredos;
- arquivos temporários;
- nível extra de diretório no ZIP;
- nome final coerente.

### 11. Classificar e corrigir riscos

Classificar cada achado:

- **Alto:** impede execução, quebra navegação ou produz erro de JavaScript.
- **Médio:** prejudica responsividade, compatibilidade, acessibilidade ou qualidade visual.
- **Baixo:** documentação, nomenclatura ou melhoria não bloqueante.

Corrigir automaticamente riscos altos e médios sempre que possível. Executar novamente toda a validação após cada correção relevante. Não entregar o ZIP com erro alto conhecido.

### 12. Compactar e verificar

- Nome padrão: `<nome-da-tela>-responsive.zip`.
- Não incluir a pasta temporária como nível extra.
- Abrir o ZIP após a criação e validar seu conteúdo.
- Manter no diretório de entrega somente o ZIP solicitado.

## Critérios de aceite

- ZIP íntegro.
- Zero links ou assets locais quebrados.
- Zero IDs duplicados.
- JavaScript sem erro de sintaxe.
- Imagens válidas.
- Layout responsivo.
- `RISK-REVIEW.md` incluído.
- Nenhum risco alto conhecido pendente.

## Resposta final

Responder objetivamente com:

1. link do ZIP;
2. conteúdo principal;
3. funcionalidades;
4. resumo da validação;
5. riscos ou limitações remanescentes.
