#!/usr/bin/env bash
#
# bind-to-extraction.sh
# Helper que lê _solucao_sdd/ e devolve um JSON com as fontes canônicas que os skills forward devem consultar como contexto.
# Diferencial SOLUCAO: skills forward jamais partem do zero, sempre amarram raciocínio nos artefatos da pipeline solucao.
#
# Uso:
#   bind-to-extraction.sh [--json] [--for <comando>]
#
# Argumentos:
#   --for requisitos   Lista arquiteto, dominio, inventario, principios
#   --for plano           Lista arquiteto, c4-contexto, maquina-estado, dependencies, code-analysis, principios
#   --for pendencia          Lista arquiteto, code-analysis
#   --for auditoria          Lista arquiteto, dominio
#   --for codificacao         Lista arquiteto, dominio, code-analysis (para gerar legacy-impact)
#   sem --for            Lista todos os arquivos presentes em _solucao_sdd/
#
# Códigos de saída:
#   0 = sucesso
#   1 = _solucao_sdd ausente
#   2 = uso inválido

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SDD_DIR="$PROJECT_ROOT/_solucao_sdd"

JSON_MODE=0
TARGET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON_MODE=1; shift ;;
    --for) shift; TARGET="${1:-}"; shift ;;
    *) echo "uso invalido: $1" >&2; exit 2 ;;
  esac
done

if [ ! -d "$SDD_DIR" ]; then
  echo "erro: $SDD_DIR nao existe. rode a pipeline solucao antes." >&2
  exit 1
fi

declare -a wanted

case "$TARGET" in
  requisitos) wanted=("arquitetura.md" "dominio.md" "inventario.md") ;;
  plano)         wanted=("arquitetura.md" "c4-contexto.md" "maquina-estado.md" "dependencias.md" "analise-codigo.md") ;;
  pendencia|todo)   wanted=("arquitetura.md" "analise-codigo.md") ;;
  auditoria)    wanted=("arquitetura.md" "dominio.md") ;;
  codificacao)       wanted=("arquitetura.md" "dominio.md" "analise-codigo.md") ;;
  *)            wanted=("arquitetura.md" "c4-contexto.md" "analise-codigo.md" "confidence-report.md" "dependencias.md" "dominio.md" "inventario.md" "duvidas.md" "maquina-estado.md") ;;
esac

declare -a present
declare -a absent

for f in "${wanted[@]}"; do
  if [ -f "$SDD_DIR/$f" ]; then
    present+=("$f")
  else
    absent+=("$f")
  fi
done

emit_json() {
  printf '{'
  printf '"sdd-dir":"%s",' "$SDD_DIR"
  printf '"target":"%s",' "$TARGET"
  printf '"present":['
  local first=1
  for f in "${present[@]:-}"; do
    [ -z "$f" ] && continue
    if [ $first -eq 1 ]; then first=0; else printf ','; fi
    printf '"%s/%s"' "$SDD_DIR" "$f"
  done
  printf '],'
  printf '"absent":['
  first=1
  for f in "${absent[@]:-}"; do
    [ -z "$f" ] && continue
    if [ $first -eq 1 ]; then first=0; else printf ','; fi
    printf '"%s"' "$f"
  done
  printf ']'
  printf '}\n'
}

if [ $JSON_MODE -eq 1 ]; then
  emit_json
else
  echo "presentes:"
  for f in "${present[@]:-}"; do
    [ -n "$f" ] && echo "  $SDD_DIR/$f"
  done
  echo "ausentes:"
  for f in "${absent[@]:-}"; do
    [ -n "$f" ] && echo "  $f"
  done
fi

exit 0
