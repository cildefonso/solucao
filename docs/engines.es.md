# Motores compatibles

Solucao funciona con los principales motores de IA del mercado. El instalador detecta automáticamente cuáles están presentes en el entorno, pero puedes agregar más en cualquier momento con `npx solucao add-engine`.

---

## Compatibilidad

| Motor | Archivo creado | Skills path | Cómo activar |
|-------|---------------|-------------|--------------|
| **Claude Code** ⭐ | `CLAUDE.md` | `.claude/skills/solucao-*/` y `.agents/skills/solucao-*/` | `/solucao` |
| **Codex** ⭐ | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Cursor** ⭐ | `.cursorrules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Gemini CLI** | `GEMINI.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Windsurf** | `.windsurfrules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Antigravity** | `AGENTS.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Kiro** | (ninguno) | `.kiro/skills/solucao-*/` y `.agents/skills/solucao-*/` | `/solucao` |
| **Opencode** | `AGENTS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Cline** | `.clinerules` | `.agents/skills/solucao-*/` | `/solucao` |
| **Roo Code** | `.roorules` | `.agents/skills/solucao-*/` | `/solucao` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.agents/skills/solucao-*/` | `/solucao` |
| **Aider** | `CONVENTIONS.md` | `.agents/skills/solucao-*/` | `solucao` |
| **Amazon Q Developer** | `.amazonq/rules/solucao.md` | `.agents/skills/solucao-*/` | `/solucao` |

---

## Claude Code

El motor más probado y con mejor soporte. Usa slash commands nativos, lo que hace la activación intuitiva. Solucao crea los archivos en `.claude/skills/` y en `.agents/skills/` (para compatibilidad con otros motores que puedan agregarse después).

---

## Codex

Totalmente compatible. Como Codex no usa slash commands, la activación es por el nombre del agente directamente: `solucao`, `solucao-scout`, etc. El archivo `AGENTS.md` en la raíz del proyecto sirve como punto de entrada.

---

## Cursor

Compatible vía `.cursorrules`. Cursor lee las reglas de ese archivo y los agentes quedan disponibles como skills.

---

## Gemini CLI y Windsurf

Soporte completo. Los agentes viven en `.agents/skills/` y se acceden mediante los mecanismos nativos de cada motor.

---

## Antigravity

Plataforma de desarrollo agéntico de Google, lanzada en noviembre de 2025. Lee `AGENTS.md` nativamente (mismo archivo de Codex). Si Codex ya está instalado en el proyecto, el `AGENTS.md` existente se reutiliza sin duplicación. Comando CLI: `agy`.

---

## Kiro

IDE agéntico de Amazon. Kiro descubre skills nativamente en `.kiro/skills/`, sin necesidad de steering documents. El instalador coloca los agentes en `.kiro/skills/` (y también en `.agents/skills/` para compatibilidad con otros motores). La activación es vía `/solucao` o auto-discovery por la descripción del skill.

---

## Opencode

Agente de codificación open source para terminal (SST). Lee `AGENTS.md` nativamente, misma convención de Codex. Comando CLI: `opencode`. Como Codex, la activación es por el nombre del agente: `solucao`.

---

## Cline y Roo Code

Extensiones de VS Code con soporte a reglas personalizadas vía `.clinerules` y `.roorules` respectivamente. El patrón es idéntico a Cursor y Windsurf: archivo de reglas en la raíz del proyecto que instruye al agente al activar `/solucao`.

---

## GitHub Copilot

Usa `.github/copilot-instructions.md` como archivo de instrucciones personalizadas, leído automáticamente por Copilot en cada sesión. El instalador crea el archivo dentro de `.github/` (que puede ya existir en el proyecto).

---

## Aider

Agente de codificación para terminal. El entry file `CONVENTIONS.md` en la raíz se pasa vía `--read CONVENTIONS.md` o se configura en `.aider.conf.yml`. Como Codex y Opencode, la activación es por nombre: `solucao`.

---

## Amazon Q Developer

CLI de IA de AWS. Usa reglas en `.amazonq/rules/` para instruir al agente por proyecto. El instalador crea `.amazonq/rules/solucao.md` sin interferir con otras reglas que puedas tener en esa carpeta.

---

## Múltiples motores en el mismo proyecto

Puedes tener todos los motores instalados al mismo tiempo. Los agentes en `.agents/skills/` son compartidos por todos. El instalador crea los archivos de entrada específicos de cada motor sin conflicto entre ellos.

Si trabajas en equipo y cada persona usa un motor diferente, funciona con normalidad: cada uno usa el archivo de entrada de su motor, pero todos los agentes están en el mismo lugar.
