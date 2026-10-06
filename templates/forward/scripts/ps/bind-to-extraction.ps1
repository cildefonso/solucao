# bind-to-extraction.ps1
# Helper que lê _solucao_sdd/ e devolve um JSON com as fontes canônicas que os skills forward devem consultar.
#
# Uso:
#   bind-to-extraction.ps1 [-Json] [-For <comando>]
#
# -For requisitos   architecture, dominio, inventario
# -For plano           architecture, c4-contexto, maquina-estado, dependencies, code-analysis
# -For pendencia          architecture, code-analysis
# -For auditoria          architecture, dominio
# -For codificacao         architecture, dominio, code-analysis
# sem -For            todos os arquivos do _solucao_sdd
#
# Códigos de saída: 0 ok, 1 _solucao_sdd ausente, 2 uso inválido.

[CmdletBinding()]
param(
  [switch]$Json,
  [string]$For = ''
)

$ErrorActionPreference = 'Stop'

$scriptDir   = Split-Path -Parent $PSCommandPath
$projectRoot = (Resolve-Path (Join-Path $scriptDir '..\..')).Path
$sddDir      = Join-Path $projectRoot '_solucao_sdd'

if (-not (Test-Path -LiteralPath $sddDir -PathType Container)) {
  Write-Error "$sddDir nao existe. rode a pipeline solucao antes."
  exit 1
}

$wanted = switch ($For) {
  'requisitos' { @('arquitetura.md','dominio.md','inventario.md') }
  'plano'         { @('arquitetura.md','c4-contexto.md','maquina-estado.md','dependencias.md','analise-codigo.md') }
  'pendencia'        { @('arquitetura.md','analise-codigo.md') }
  'todo'         { @('arquitetura.md','analise-codigo.md') }
  'auditoria'        { @('arquitetura.md','dominio.md') }
  'codificacao'       { @('arquitetura.md','dominio.md','analise-codigo.md') }
  default        { @('arquitetura.md','c4-contexto.md','analise-codigo.md','confidence-report.md','dependencias.md','dominio.md','inventario.md','duvidas.md','maquina-estado.md') }
}

$present = New-Object System.Collections.Generic.List[string]
$absent  = New-Object System.Collections.Generic.List[string]

foreach ($f in $wanted) {
  $full = Join-Path $sddDir $f
  if (Test-Path -LiteralPath $full) {
    $present.Add($full) | Out-Null
  } else {
    $absent.Add($f) | Out-Null
  }
}

$result = [ordered]@{
  'sdd-dir' = $sddDir
  'target'  = $For
  'present' = @($present)
  'absent'  = @($absent)
}

if ($Json) {
  $result | ConvertTo-Json -Compress -Depth 4 | Write-Output
} else {
  Write-Output 'presentes:'
  foreach ($p in $present) { Write-Output "  $p" }
  Write-Output 'ausentes:'
  foreach ($a in $absent) { Write-Output "  $a" }
}

exit 0
