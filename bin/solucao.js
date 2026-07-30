#!/usr/bin/env node

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import chalk from 'chalk';
import { clearTerminalForLogo, renderSolucaoLogo } from '../lib/utils/banner.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf8'));

const [,, command, ...args] = process.argv;

const commands = {
  install:            () => import('../lib/commands/install.js'),
  update:             () => import('../lib/commands/update.js'),
  status:             () => import('../lib/commands/status.js'),
  uninstall:          () => import('../lib/commands/uninstall.js'),
  'add-agent':        () => import('../lib/commands/add-agent.js'),
  'add-engine':       () => import('../lib/commands/add-engine.js'),
  'export-diagrams':  () => import('../lib/commands/export-diagrams.js'),
};

if (!command || command === '--help' || command === '-h') {
  clearTerminalForLogo();
  console.log(renderSolucaoLogo(chalk) + `

  solucao v${pkg.version}

  Uso: npx solucao <comando>

  Comandos:
    install            Instala o Solucao no projeto atual
    update             Atualiza os agentes para a última versão
    status             Mostra o estado atual da análise
    uninstall          Remove o Solucao do projeto
    add-agent          Adiciona um agente ao projeto
    add-engine         Adiciona suporte a uma engine
    export-diagrams    Exporta diagramas Mermaid como imagens SVG/PNG
                       Opções: --format=svg|png  --output=<pasta>
                       Requer: npm install -g @mermaid-js/mermaid-cli

  Fluxos principais no chat (após a instalação):
    /solucao          Descobre e documenta um sistema existente
    /solucao-new      Cria PRD e specs para um projeto novo
    /solucao-forward  Implementa ou evolui código a partir das specs
    /solucao-migrate  Planeja a migração de um sistema legado
    /solucao-docs     Gera o mini-site visual da documentação

  Documentação: https://github.com/cildefonso/solucao
  `);
  process.exit(0);
}

if (command === '--version' || command === '-v') {
  console.log(pkg.version);
  process.exit(0);
}

if (!commands[command]) {
  console.error(`\n  Comando desconhecido: "${command}"`);
  console.error('  Execute "npx solucao --help" para ver os comandos disponíveis.\n');
  process.exit(1);
}

const mod = await commands[command]();
await mod.default(args);
