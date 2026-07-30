import { existsSync, readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, resolve } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { checkExistingInstallation } from '../installer/validator.js';
import { Writer } from '../installer/writer.js';
import { loadManifest, saveManifest, buildManifest } from '../installer/manifest.js';
import { ENGINES } from '../installer/detector.js';
import { applyOrangeTheme, ORANGE_PREFIX } from '../installer/orange-prompts.js';
import { readJsonSafe } from '../utils/json-safe.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..', '..');
const AGENTS_DIR = join(REPO_ROOT, 'agents');

const AGENT_LABELS = {
  'solucao-autonomous':       'Autonomous: runs the full /solucao pipeline without intermediate stops (/solucao-autonomous)',
  'solucao-scout':            'Scout: reconnaissance',
  'solucao-archaeologist':    'Archaeologist: excavation',
  'solucao-detective':        'Detective: interpretation',
  'solucao-architect':        'Architect: architectural synthesis',
  'solucao-writer':           'Writer: spec generation',
  'solucao-reviewer':         'Reviewer: spec review and validation',
  'solucao-visor':            'Visor: UI analysis via screenshots',
  'solucao-data-master':      'Data Master: database analysis',
  'solucao-design-system':    'Design System: design tokens and themes',
  'solucao-agents-help':      'Agents Help: explains agents with analogies',
  'solucao-reconstructor':    'Reconstructor: rebuilds the software from generated specs',
  'solucao-migrate':          'Migrate: orchestrator of the migration team (/solucao-migrate)',
  'solucao-paradigm-advisor': 'Paradigm Advisor: detects paradigm gap between legacy and target stack',
  'solucao-curator':          'Curator: decides what migrates, what gets discarded, what needs human decision',
  'solucao-strategist':       'Strategist: proposes migration strategies (Strangler, Big Bang, Parallel Run, Branch by Abstraction)',
  'solucao-designer':         'Designer: drafts target architecture, domain model, data model and migration plan',
  'solucao-screen-translator': 'Screen Translator: translates legacy screens into executable specs (literal/modernized/hybrid) and emits golden files',
  'solucao-inspector':        'Inspector: defines parity specs and Gherkin scenarios for behavioral equivalence',
  'solucao-n8n':              'N8N Translator: converts N8N workflows (JSON) to SDD specs (/solucao-n8n)',
  'solucao-pricing-profile':  'Pricing Profile: configures the user pricing profile (/solucao-pricing-profile)',
  'solucao-pricing-size':     'Pricing Size: measures structural size of the active feature (/solucao-pricing-size)',
  'solucao-pricing-estimate': 'Pricing Estimate: generates 3 price scenarios (Effort, Value, Market) (/solucao-pricing-estimate)',
  'solucao-debugger':              'Bug: registers and traces a defect, never fixes (/solucao-debugger)',
  'solucao-debugger-fix':          'Bug Fix: lifecycle orchestrator with root cause, change set and spec verdict (/solucao-debugger-fix)',
  'solucao-debugger-debate':       'Bug Debate: multi-agent debate (diagnosis/repair/spec) with isolated judge (/solucao-debugger-debate)',
  'solucao-depth-inspection': 'Depth Inspection: deep sweep of a problematic feature, diagnosis only (/solucao-depth-inspection)',
  'solucao-debugger-graph':        'Bug Graph: regenerates index, sparse matrix, graph and BUG-SPEC traceability views (/solucao-debugger-graph)',
};

export default async function addAgent(args) {
  const { default: chalk } = await import('chalk');
  const { default: inquirer } = await import('inquirer');
  applyOrangeTheme();

  const projectRoot = resolve(process.cwd());

  console.log(chalk.bold('\n  Solucao: Add Agent\n'));

  const existing = checkExistingInstallation(projectRoot);
  if (!existing.installed) {
    console.log(chalk.yellow('  Solucao is not installed in this directory.'));
    console.log('  Run ' + chalk.bold('npx github:cildefonso/solucao install') + ' to install.\n');
    return;
  }

  const state = existing.state;

  // Validate required fields
  if (!Array.isArray(state.engines) || state.engines.length === 0) {
    console.log(chalk.red('  state.json has no configured engines.'));
    console.log('  Run ' + chalk.bold('npx github:cildefonso/solucao install') + ' or ' + chalk.bold('npx solucao add-engine') + ' first.\n');
    return;
  }

  const installedAgents = new Set(state.agents ?? []);
  const installedEngines = ENGINES.filter(e => state.engines.includes(e.id));

  let availableAgents = [];
  try {
    availableAgents = readdirSync(AGENTS_DIR, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name)
      .filter(name => !installedAgents.has(name));
  } catch {
    console.log(chalk.red('  Could not read the agents folder.\n'));
    return;
  }

  if (availableAgents.length === 0) {
    console.log(chalk.hex('#ffa203')('  All available agents are already installed.\n'));
    return;
  }

  const choices = availableAgents.map(id => ({
    name: AGENT_LABELS[id] ?? id,
    value: id,
    checked: true,
  }));

  const { selected } = await inquirer.prompt([{
    prefix: ORANGE_PREFIX,
    type: 'checkbox',
    name: 'selected',
    message: '\nSelect agents to add:\n\n',
    choices,
    validate: (v) => v.length > 0 || 'Select at least one agent.',
  }]);

  const writer = new Writer(projectRoot);

  for (const agent of selected) {
    for (const engine of installedEngines) {
      await writer.installSkill(agent, engine.skillsDir);
      if (engine.universalSkillsDir && engine.universalSkillsDir !== engine.skillsDir) {
        await writer.installSkill(agent, engine.universalSkillsDir);
      }
    }
    console.log(chalk.hex('#ffa203')(`  ✓  ${AGENT_LABELS[agent] ?? agent}`));
  }

  // Atualizar state.json
  const statePath = join(projectRoot, '.solucao', 'state.json');
  const s = readJsonSafe(statePath);
  s.agents = [...new Set([...(s.agents ?? []), ...selected])];
  writeFileSync(statePath, JSON.stringify(s, null, 2), 'utf8');

  writer.saveCreatedFiles();

  // Atualizar manifest com caminhos relativos
  const existingManifest = loadManifest(projectRoot);
  const newManifest = buildManifest(projectRoot, writer.manifestPaths);
  saveManifest(projectRoot, { ...existingManifest, ...newManifest });

  console.log(chalk.bold(`\n  ${selected.length} agent(s) added successfully.\n`));
}
