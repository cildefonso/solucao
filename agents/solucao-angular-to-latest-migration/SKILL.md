---
name: solucao-angular-to-latest-migration
description: Migração incremental, auditável e reversível de projetos Angular para a última versão estável, a partir da versão de origem lida no package.json da aplicação (path solicitado ao usuário), incluindo compatibilidade, testes, pipeline, evidências e rollback.
---

# Migração Angular para a última versão estável

## Objetivo
Migrar uma aplicação Angular, a partir da versão de origem identificada no `package.json` da aplicação, para a última versão estável oficial, preservando regras de negócio, segurança, testes, build, pipeline e rollback.

## Regras obrigatórias
1. Confirmar a versão estável e a matriz Angular, Node.js, TypeScript, RxJS e Zone.js em fontes oficiais.
2. Migrar uma major por vez, usando o patch mais recente de cada major intermediária.
3. Executar migrations oficiais do Angular CLI.
4. Não avançar com erro de instalação, compilação, lint, teste ou build.
5. Não usar `--force`, `--legacy-peer-deps` ou `npm audit fix --force` como solução permanente.
6. Não remover testes, reduzir strictness ou introduzir `any` para ocultar erros.
7. Preservar `.npmrc`, registry, proxy, certificados, secrets e políticas corporativas.
8. Separar atualização obrigatória de modernizações opcionais.
9. Não executar operações Git destrutivas.
10. Não declarar sucesso sem comando, resultado e evidência verificável.

## Fontes oficiais
- `https://angular.dev/reference/versions`
- `https://angular.dev/update-guide`
- `https://angular.dev/reference/releases`
- `https://www.npmjs.com/package/@angular/core`

## Fluxo

### 0. Path da aplicação e versão de origem
1. Antes de qualquer outra etapa, solicitar ao usuário o path absoluto da aplicação Angular a migrar. Não assumir o diretório atual nem um path de outro projeto sem confirmação. Se a ferramenta de perguntas estiver disponível, usá-la; caso contrário, perguntar diretamente no chat.
2. Confirmar que o path existe e contém `package.json` e `angular.json`. Se não contiver, informar o que faltou e pedir um path válido.
3. Ler a versão de origem no `package.json` da aplicação, em `dependencies["@angular/core"]` (conferir também `@angular/cli` e `@angular/compiler-cli` em `devDependencies`). Se o valor for um intervalo (`^`, `~`), confirmar a versão efetivamente instalada no lockfile (`package-lock.json`, `yarn.lock` ou `pnpm-lock.yaml`) ou em `node_modules/@angular/core/package.json`.
4. Registrar a versão de origem (ex.: `16.2.0`) e usá-la em todas as etapas seguintes, no estado (`templates/migration-state.json`, campo `sourceAngular`) e nas evidências. Se as versões dos pacotes `@angular/*` divergirem entre si, reportar como risco antes de prosseguir.
5. Se a versão de origem já for a última estável, informar o usuário e encerrar sem migrar. Se for anterior à 16, avisar que a skill foi desenhada a partir da 16 e pedir confirmação antes de continuar.
6. Executar todos os comandos e scripts (`scripts/preflight.sh`, `scripts/validate.sh`) a partir do path informado.

### 1. Preservação
```bash
git status
git branch --show-current
git remote -v
git log -1 --oneline
```
Sugerir branch `chore/migrate-angular-<origem>-to-latest` (ex.: `chore/migrate-angular-16-to-latest`) e tag `backup-before-angular-migration`, sem sobrescrever nomes existentes.

### 2. Diagnóstico
Executar `scripts/preflight.sh` e analisar `package.json`, lockfile, `angular.json`, `tsconfig*.json`, `.npmrc`, código de bootstrap, environments, testes, Material/CDK, SSR, PWA, Module Federation, builders, Docker, nginx, pipeline, SonarQube, SAST e SCA.

### 3. Destino
Identificar dinamicamente a última versão estável, partindo da versão de origem lida na etapa 0, selecionar versões suportadas e homologadas de Node.js e TypeScript e definir as transições entre majors.

### 4. Atualização por major
Para a major `N`:
```bash
npx @angular/cli@N update @angular/core@N @angular/cli@N
```
Se Material estiver presente:
```bash
npx @angular/cli@N update @angular/material@N
```
Revisar migrations, diff, peer dependencies, APIs removidas e ferramentas de teste.

### 5. Validação
Detectar scripts antes de executá-los. Usar `scripts/validate.sh`. Validar instalação limpa, lint, testes, cobertura, E2E, build de desenvolvimento, build de produção e runtime, quando aplicáveis.

### 6. Pipeline e deploy
Validar imagem Node.js, `npm ci`, cache, registry, certificados, diretório `dist`, pasta `browser`, Dockerfile, nginx, artefatos, ambientes, quality gates e rollback.

### 7. Evidências
Usar integralmente `references/output-template.md`. Toda etapa deve conter comandos, códigos de saída quando aplicáveis, resultados, status e identificadores de evidência.

## Tratamento de erros
Interromper a progressão, registrar comando e ambiente, preservar a mensagem, identificar causa raiz, corrigir com menor risco, apresentar diff, validar novamente e prosseguir somente após sucesso.

## Critérios de conclusão
Concluir apenas com versões compatíveis, instalação limpa, lint, testes e builds aprovados, runtime validado, pipeline aprovado, ausência de vulnerabilidade crítica introduzida, configurações corporativas preservadas, matriz de evidências preenchida e rollback documentado.
