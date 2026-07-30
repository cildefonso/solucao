# Engines suportadas

O Solucao funciona com as principais engines de IA do mercado. O instalador detecta automaticamente quais estão presentes no ambiente, mas você pode adicionar mais a qualquer momento com `npx solucao add-engine`.

---

## Compatibilidade

| Engine | Arquivo criado | Skills path | Como ativar |
|--------|---------------|-------------|-------------|
| **Claude Code** ⭐ | `CLAUDE.md` | `.claude/skills/solucao-*/` e `.agents/skills/solucao-*/` | `/solucao` |
| **Codex** ⭐ | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Cursor** ⭐ | `.cursorrules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Gemini CLI** | `GEMINI.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Windsurf** | `.windsurfrules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Antigravity** | `AGENTS.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Kiro** | (nenhum) | `.kiro/skills/solucao-*/` e `.agents/skills/solucao-*/` | `/solucao` |
| **Opencode** | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Cline** | `.clinerules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Roo Code** | `.roorules` | `.agents/skills/solucao-*/` | `/solucao` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Aider** | `CONVENTIONS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Amazon Q Developer** | `.amazonq/rules/solucao.md` | `.agents/skills/solucao-*/` | `/solucao` |

---

## Claude Code

A engine mais testada e com melhor suporte. Usa slash commands nativos, o que torna a ativação intuitiva. O Solucao cria os arquivos em `.claude/skills/` e em `.agents/skills/` (para compatibilidade com outras engines que possam ser adicionadas depois).

---

## Codex

Totalmente compatível. Como o Codex não usa slash commands, a ativação é pelo nome do agente diretamente: `solucao`, `solucao-scout`, etc. O arquivo `AGENTS.md` na raiz do projeto serve como ponto de entrada.

---

## Cursor

Compatível via `.cursorrules`. O Cursor lê as regras desse arquivo e os agentes ficam disponíveis como skills.

---

## Gemini CLI e Windsurf

Suporte completo. Os agentes ficam em `.agents/skills/` e são acessados via os mecanismos nativos de cada engine.

---

## Antigravity

Plataforma de desenvolvimento agêntico do Google, lançada em novembro de 2025. Lê `AGENTS.md` nativamente (mesmo arquivo do Codex). Se Codex já estiver instalado no projeto, o `AGENTS.md` existente é reaproveitado sem duplicação. Comando CLI: `agy`.

---

## Kiro

IDE agêntico da Amazon. O Kiro descobre skills nativamente em `.kiro/skills/`, sem necessidade de steering documents. O instalador coloca os agentes em `.kiro/skills/` (e também em `.agents/skills/` para compatibilidade com outras engines). A ativação é via `/solucao` ou auto-discovery pela descrição do skill.

---

## Opencode

Agente de codificação open source para terminal (SST). Lê `AGENTS.md` nativamente, mesma convenção do Codex. Comando CLI: `opencode`. Como Codex, a ativação é pelo nome do agente: `solucao`.

---

## Cline e Roo Code

Extensions de VS Code com suporte a regras personalizadas via `.clinerules` e `.roorules` respectivamente. O padrão é idêntico ao Cursor e Windsurf: arquivo de regras na raiz do projeto que instrui o agente ao ativar `/solucao`.

---

## GitHub Copilot

Usa `.github/copilot-instructions.md` como arquivo de instruções customizadas, lido automaticamente pelo Copilot em toda sessão. O instalador cria o arquivo dentro de `.github/` (que pode já existir no projeto).

---

## Aider

Agente de codificação para terminal. O entry file `CONVENTIONS.md` na raiz é passado via `--read CONVENTIONS.md` ou configurado em `.aider.conf.yml`. Como Codex e Opencode, a ativação é pelo nome: `solucao`.

---

## Amazon Q Developer

CLI de IA da AWS. Usa regras em `.amazonq/rules/` para instruir o agente por projeto. O instalador cria `.amazonq/rules/solucao.md` sem interferir em outras regras que você já tenha nessa pasta.

---

## Múltiplas engines no mesmo projeto

Você pode ter todas as engines instaladas ao mesmo tempo. Os agentes em `.agents/skills/` são compartilhados por todas. O instalador cria os arquivos de entrada específicos de cada engine sem conflito entre eles.

Se você trabalha em equipe e cada pessoa usa uma engine diferente, isso funciona normalmente: cada um usa o arquivo de entrada da sua engine, mas todos os agentes estão no mesmo lugar.
