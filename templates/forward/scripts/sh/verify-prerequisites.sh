#!/usr/bin/env bash
#
# verify-prerequisites.sh
# Helper genérico de pré-condições, chamado pelos skills forward do Solucao.
#
# Saída padrão JSON em uma única linha. O agente lê e age conforme os campos.
# Sem dependências externas além de bash, jq opcional.
#
# Uso:
#   verify-prerequisites.sh [--json] [--require <campo>] [--require <campo>] ...
#
# Campos suportados em --require:
#   active-requisitos   Exige que .solucao/active-requisitos.json exista.
#   feature-dir           Exige que a pasta apontada por active-requisitos exista.
#   requisitos          Exige feature-dir/requisitos.md.
#   roadmap               Exige feature-dir/roadmap.md.
#   actions               Exige feature-dir/actions.md.
#   sdd                   Exige _solucao_sdd/ presente.
#   principios            Exige .solucao/principios.md.
#
# Códigos de saída:
#   0 = todos os requisitos batem
#   1 = pelo menos um requisito faltou (detalhes no JSON)
#   2 = uso inválido

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SOLUCAO_DIR="$PROJECT_ROOT/.solucao"
SDD_DIR="$PROJECT_ROOT/_solucao_sdd"
FORWARD_DIR="$PROJECT_ROOT/_solucao_forward"
ACTIVE="$SOLUCAO_DIR/active-requisitos.json"

JSON_MODE=0
REQUIRES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON_MODE=1; shift ;;
    --require) shift; REQUIRES+=("${1:-}"); shift ;;
    *) echo "uso invalido: $1" >&2; exit 2 ;;
  esac
done

missing=()
feature_dir=""

if [ -f "$ACTIVE" ]; then
  feature_dir_rel="$(grep -o '"feature-dir"[[:space:]]*:[[:space:]]*"[^"]*"' "$ACTIVE" | sed 's/.*"\([^"]*\)"$/\1/' | head -n 1)"
  if [ -n "$feature_dir_rel" ]; then
    feature_dir="$PROJECT_ROOT/$feature_dir_rel"
  fi
fi

check_one() {
  local name="$1"
  case "$name" in
    active-requisitos)
      [ -f "$ACTIVE" ] || missing+=("active-requisitos")
      ;;
    feature-dir)
      if [ -z "$feature_dir" ] || [ ! -d "$feature_dir" ]; then
        missing+=("feature-dir")
      fi
      ;;
    requisitos)
      [ -n "$feature_dir" ] && [ -f "$feature_dir/requisitos.md" ] || missing+=("requisitos")
      ;;
    roadmap)
      [ -n "$feature_dir" ] && [ -f "$feature_dir/roadmap.md" ] || missing+=("roadmap")
      ;;
    actions)
      [ -n "$feature_dir" ] && [ -f "$feature_dir/actions.md" ] || missing+=("actions")
      ;;
    sdd)
      [ -d "$SDD_DIR" ] || missing+=("sdd")
      ;;
    principios)
      [ -f "$SOLUCAO_DIR/principios.md" ] || missing+=("principios")
      ;;
    *)
      missing+=("desconhecido:$name")
      ;;
  esac
}

for r in "${REQUIRES[@]}"; do
  [ -n "$r" ] && check_one "$r"
done

emit_json() {
  printf '{'
  printf '"project-root":"%s",' "$PROJECT_ROOT"
  printf '"solucao-dir":"%s",' "$SOLUCAO_DIR"
  printf '"sdd-dir":"%s",' "$SDD_DIR"
  printf '"forward-dir":"%s",' "$FORWARD_DIR"
  printf '"active-requisitos":"%s",' "$ACTIVE"
  printf '"feature-dir":"%s",' "$feature_dir"
  printf '"missing":['
  local first=1
  for m in "${missing[@]:-}"; do
    if [ -z "$m" ]; then continue; fi
    if [ $first -eq 1 ]; then first=0; else printf ','; fi
    printf '"%s"' "$m"
  done
  printf ']}'
  printf '\n'
}

if [ $JSON_MODE -eq 1 ]; then
  emit_json
else
  if [ ${#missing[@]} -eq 0 ]; then
    echo "ok"
  else
    echo "faltando: ${missing[*]}"
  fi
fi

if [ ${#missing[@]} -eq 0 ]; then
  exit 0
else
  exit 1
fi
