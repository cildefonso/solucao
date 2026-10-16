#!/usr/bin/env bash
set -euo pipefail
[ -f package.json ] || { echo 'package.json not found' >&2; exit 2; }
has(){ node -e "const p=require('./package.json');process.exit(p.scripts&&p.scripts['$1']?0:1)"; }
run(){ if has "$1"; then echo "==> npm run $1 ${2:-}"; [ -n "${2:-}" ] && npm run "$1" -- $2 || npm run "$1"; else echo "==> skipped: $1"; fi; }
npm ci
run lint
run test '--watch=false'
run test:coverage
run build
has build && npm run build -- --configuration production
run test:e2e
run build:ssr
