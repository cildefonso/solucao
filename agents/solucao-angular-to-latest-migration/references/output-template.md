# Relatório de migração Angular

## 1. Identificação da execução
- Projeto:
- Repositório:
- Branch:
- Commit inicial:
- Commit final:
- Responsável:
- Início:
- Conclusão:
- Ambiente:
- Sistema operacional:
- Shell:
- Status: `NÃO INICIADO | EM EXECUÇÃO | BLOQUEADO | CONCLUÍDO`

## 2. Resumo executivo
- Objetivo:
- Escopo:
- Angular de origem:
- Angular de destino:
- Resultado geral:
- Alterações principais:
- Riscos:
- Bloqueadores:
- Pendências:
- Recomendação:
- Evidências:

## 3. Versões detectadas
### Estado inicial
- Angular Core/CLI/Material/CDK:
- Node.js/npm/TypeScript/RxJS/Zone.js:
- Gerenciador, lockfile e registry:
### Estado final
- Angular Core/CLI/Material/CDK:
- Node.js/npm/TypeScript/RxJS/Zone.js:
- Gerenciador, lockfile e registry:
### Comandos
```bash
# Comandos de verificação
```
### Resultados
```text
# Saídas sanitizadas
```
### Evidências
- Identificador:
- Localização:
- Commit/pipeline:

## 4. Destino estável e fontes
- Versão estável:
- Data da consulta:
- Fonte oficial:
- Versões de pré-lançamento descartadas:
- Justificativa:
- Comandos:
- Resultados:
- Evidências:

## 5. Matriz de compatibilidade
Para cada componente:
- Componente:
- Versão inicial:
- Versão suportada:
- Versão aplicada:
- Compatibilidade: `COMPATÍVEL | INCOMPATÍVEL | PARCIAL | NÃO APLICÁVEL`
- Risco: `BLOQUEADOR | ALTO | MÉDIO | BAIXO | INFORMATIVO`
- Ação:
- Comando:
- Resultado:
- Evidência:

## 6. Diagnóstico e inventário
- Workspace e projetos:
- Standalone/NgModules:
- SSR/hydration/PWA:
- Module Federation/builders/webpack:
- Bibliotecas internas:
- Autenticação e autorização:
- Pipeline/container/servidor web:
- SonarQube/SAST/SCA:
- Registry/proxy/certificados:
### Comandos
```bash
# Diagnóstico
```
### Resultados
```text
# Resultados sanitizados
```
### Evidências
- Arquivos:
- Logs:
- Relatórios:

## 7. Riscos e bloqueadores
Para cada item:
- ID:
- Descrição/categoria/severidade:
- Major, dependência ou arquivo:
- Causa raiz e impacto:
- Mitigação e responsável:
- Status: `ABERTO | MITIGADO | ACEITO | RESOLVIDO`
- Resultado:
- Evidência:

## 8. Etapas por major
Repetir para cada transição real até o destino estável detectado.
### Angular X → Y
- Data:
- Node.js/TypeScript:
- Versão inicial/final:
- Status:
#### Comandos
```bash
# Ordem real de execução
```
#### Resultados
```text
# Saídas, códigos de retorno e erros
```
#### Migrations automáticas
- Migration/arquivos/resultado/evidência:
#### Correções manuais
- Arquivo/motivo/risco:
- Antes/depois:
- Comando e resultado da validação:
- Impacto/rollback/evidência:
#### Validações
- Instalação/lint/testes/cobertura/E2E:
- Build DES/PROD/runtime:
- Resultado geral:
#### Evidências
- Commit/diff/log/relatório/artefato/pipeline/print:

## 9. Pipeline e deploy
- Arquivo e imagem Node.js antes/depois:
- Instalação/build/cache:
- Output antes/depois:
- Artefato/variáveis/secrets:
- Docker/nginx/rollback:
- Comandos:
- Resultados:
- Evidências:

## 10. Testes e builds
Para cada verificação:
- ID e tipo:
- Comando/data/ambiente:
- Código de saída, quando aplicável:
- Status: `APROVADO | REPROVADO | NÃO EXECUTADO | NÃO APLICÁVEL`
- Resumo, testes e cobertura fornecidos pela ferramenta:
- Erros/alertas:
- Evidência:

## 11. Vulnerabilidades
Para cada item:
- Pacote/severidade/origem:
- Direta ou transitiva:
- Versão afetada/corrigida:
- Comando/resultado:
- Impacto/risco/decisão/status:
- Evidência:
### Consolidado
- Antes/depois/críticas introduzidas/riscos aceitos:

## 12. Pendências
- ID/descrição/motivo/impacto/prioridade:
- Responsável/ação/critério/status:
- Evidência atual:

## 13. Rollback
- Branch/tag/commit/lockfile:
- Imagem e artefato anteriores:
- Pipeline anterior:
- Condições de acionamento:
### Comandos
```bash
# Comandos seguros e específicos
```
### Teste
- Testado: `SIM | NÃO`
- Ambiente/resultado/limitações/evidência:

## 14. Checklist de homologação
- [ ] Versões compatíveis
- [ ] `npm ci`, lint, testes e builds aprovados
- [ ] Integração e E2E aprovados, quando existentes
- [ ] Runtime e fluxos críticos validados
- [ ] Pipeline e artefato aprovados
- [ ] Vulnerabilidades avaliadas
- [ ] Configurações corporativas preservadas
- [ ] Documentação, rollback e evidências completos

## 15. Commits sugeridos
- Etapa/mensagem/arquivos/resultado/evidências:
```text
chore(angular): migrate from Angular X to Angular Y
```

## 16. Critérios de aceite
Para cada critério:
- Critério/método/comando:
- Esperado/obtido:
- Status: `ATENDIDO | NÃO ATENDIDO | PARCIAL | NÃO APLICÁVEL`
- Evidência/observações:

## 17. Recomendação para pull request
- Status: `ABRIR | NÃO ABRIR | ABRIR COMO DRAFT`
- Justificativa/branches/commits:
- Riscos/pendências/rollback/validadores:
- Evidências:

## 18. Registro consolidado de comandos
Para cada comando:
- Sequência/etapa/diretório/comando:
- Data/código de saída/resultado:
- Log ou evidência/observações:

## 19. Registro consolidado de resultados
- Instalação/lint/testes/cobertura:
- Integração/E2E:
- Build DES/PROD/runtime:
- Pipeline/deploy/homologação:
- Resultado geral:

## 20. Matriz de evidências por etapa
Ajustar as linhas de transição à versão de origem lida no `package.json` da aplicação: começar pela major de origem e remover as transições anteriores a ela.

| Etapa | Critério | Comando | Esperado | Obtido | Status | Evidência | Responsável | Data/hora | Observações |
|---|---|---|---|---|---|---|---|---|---|
| Diagnóstico | Versões e ambiente identificados | `node --version`; `npm --version`; `npx ng version` | Diagnóstico registrado |  | `PENDENTE` | `EVD-DIAG-001` |  |  |  |
| Inventário | Dependências e arquivos críticos identificados | `npm ls --depth=0` | Inventário concluído |  | `PENDENTE` | `EVD-INV-001` |  |  |  |
| Compatibilidade | Stack suportada | Conforme análise | Matriz aprovada |  | `PENDENTE` | `EVD-COMP-001` |  |  |  |
| Angular 16 → 17 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-16-17-001` |  |  |  |
| Angular 17 → 18 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-17-18-001` |  |  |  |
| Angular 18 → 19 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-18-19-001` |  |  |  |
| Angular 19 → 20 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-19-20-001` |  |  |  |
| Angular 20 → 21 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-20-21-001` |  |  |  |
| Angular 21 → 22 | Validação integral | Conforme registro | Etapa aprovada |  | `PENDENTE` | `EVD-21-22-001` |  |  | Usar somente se aplicável ao destino |
| Pipeline | Pipeline atualizado | Conforme CI/CD | Aprovado |  | `PENDENTE` | `EVD-PIPE-001` |  |  |  |
| Build PROD | Artefato esperado | `npm run build -- --configuration production` | Código zero |  | `PENDENTE` | `EVD-BUILD-001` |  |  |  |
| Segurança | Riscos avaliados | Ferramenta definida | Sem crítica introduzida |  | `PENDENTE` | `EVD-SEC-001` |  |  |  |
| Regressão | Fluxos críticos | Plano de testes | Aprovados |  | `PENDENTE` | `EVD-REG-001` |  |  |  |
| Rollback | Restauração validada | Plano de rollback | Viável |  | `PENDENTE` | `EVD-RBK-001` |  |  |  |
| Homologação | Aceite atendido | Checklist | Aprovada |  | `PENDENTE` | `EVD-HOM-001` |  |  |  |

Regras: usar `PENDENTE`, `EM EXECUÇÃO`, `APROVADO`, `REPROVADO`, `BLOQUEADO` ou `NÃO APLICÁVEL`; não aprovar sem evidência; registrar comandos sanitizados; adicionar/remover majors conforme o destino; justificar itens não aplicáveis.

## 21. Índice de evidências
Para cada evidência:
- Identificador/título/tipo:
- Etapa/descrição:
- Localização ou referência:
- Data/hora/responsável:
- Código de saída, quando aplicável:
- Resultado esperado/obtido/status:
- Hash, quando aplicável:
- Evidência primária ou secundária:
- Dados sensíveis removidos: `SIM | NÃO | NÃO APLICÁVEL`
