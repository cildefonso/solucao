#!/usr/bin/env bash
set -u
printf '%s\n' '=== Angular migration preflight ==='
printf 'Date: '; date -Iseconds 2>/dev/null || date
printf 'Directory: '; pwd
run(){ printf '\n$ %s\n' "$*"; "$@" 2>&1 || true; }
run git status --short; run git branch --show-current; run git log -1 --oneline
run node --version; run npm --version; run npm config get registry; run npx ng version
run npm ls --depth=0; run npm outdated; run npm audit --omit=dev
printf '\n=== Relevant files ===\n'
find . -maxdepth 3 -type f \( -name 'package.json' -o -name '*lock*' -o -name 'angular.json' -o -name 'tsconfig*.json' -o -name '.npmrc' -o -name 'Dockerfile*' -o -name 'nginx.conf' -o -name '*pipeline*.yml' \) -print 2>/dev/null | sort
