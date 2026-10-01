[CmdletBinding()]
param(
    [switch]$Watch
)

$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$pidFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.pid'
$outputLogFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.out.log'
$errorLogFile = Join-Path $projectRoot '.${PROJECT_ID}-backend.err.log'
$runnerJar = Join-Path $projectRoot 'target\quarkus-app\quarkus-run.jar'
$applicationDat = Join-Path $projectRoot 'target\quarkus-app\quarkus\quarkus-application.dat'
$applicationProperties = Join-Path $projectRoot 'src\main\resources\application.properties'
$mavenWrapper = Join-Path $projectRoot 'mvnw.cmd'

if (-not $env:JAVA_HOME) {
    $defaultJavaHome = 'C:\caixa\software\jdk-${JAVA_VERSION}'
    if (-not (Test-Path $defaultJavaHome)) {
        $found = Get-ChildItem 'C:\caixa\software' -Filter "jdk-${JAVA_VERSION}*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { $defaultJavaHome = $found.FullName }
    }

    if (Test-Path $defaultJavaHome) {
        $env:JAVA_HOME = $defaultJavaHome
    }
    else {
        throw "JAVA_HOME não está definido. Configure-o para um JDK ${JAVA_VERSION} antes de iniciar a aplicação."
    }
}

$javaExecutable = Join-Path $env:JAVA_HOME 'bin\java.exe'
if (-not (Test-Path $javaExecutable)) {
    throw "Executável Java não encontrado em '$javaExecutable'."
}
if (-not (Test-Path $mavenWrapper)) {
    throw "Maven Wrapper não encontrado em '$mavenWrapper'."
}

$httpPort = 8080
if (Test-Path $applicationProperties) {
    $configuredPort = Get-Content $applicationProperties |
        Where-Object { $_ -match '^\s*quarkus\.http\.port\s*=\s*\d+\s*$' } |
        Select-Object -Last 1

    if ($configuredPort -match '=\s*(\d+)\s*$') {
        $httpPort = $Matches[1]
    }
}

function Stop-Application {
    if (-not (Test-Path $pidFile)) {
        return
    }

    $existingProcessId = (Get-Content -Raw $pidFile).Trim()
    $existingProcess = Get-Process -Id $existingProcessId -ErrorAction SilentlyContinue
    if ($existingProcess) {
        Write-Host "Parando aplicação (PID $existingProcessId)..."
        Stop-Process -Id $existingProcessId -Force
        Wait-Process -Id $existingProcessId -ErrorAction SilentlyContinue
    }

    Remove-Item $pidFile -Force
}

function Invoke-Build {
    Write-Host "Executando build e testes: '.\mvnw.cmd clean package'..."
    Push-Location $projectRoot
    try {
        & $mavenWrapper clean package
        if ($LASTEXITCODE -ne 0) {
            throw "Build Maven falhou com código $LASTEXITCODE. A aplicação não será iniciada."
        }
    }
    finally {
        Pop-Location
    }

    if (-not (Test-Path $runnerJar) -or -not (Test-Path $applicationDat)) {
        throw "Build concluído sem gerar os artefatos Quarkus esperados em '$runnerJar'."
    }
}

function Start-Application {
    Stop-Application
    Invoke-Build

    Write-Host "Iniciando aplicação com o runner '$runnerJar'..."
    $process = Start-Process -FilePath $javaExecutable `
        -ArgumentList @('-jar', $runnerJar) `
        -WorkingDirectory $projectRoot `
        -RedirectStandardOutput $outputLogFile `
        -RedirectStandardError $errorLogFile `
        -PassThru

    Set-Content -Path $pidFile -Value $process.Id
    Write-Host "Aplicação iniciada com PID $($process.Id)."

    $healthUrl = "http://localhost:$httpPort/q/health/live"
    Write-Host "Aguardando endpoint de saúde responder em $healthUrl..."

    $tentativas = 30
    $sucesso = $false

    for ($i = 1; $i -le $tentativas; $i++) {
        Start-Sleep -Seconds 1

        if ($process.HasExited) {
            $erro = if (Test-Path $errorLogFile) { Get-Content $errorLogFile -Raw } else { 'Sem log de erro.' }
            throw "O processo Java encerrou prematuramente. Detalhes:`n$erro"
        }

        try {
            $resposta = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($resposta.StatusCode -eq 200) {
                $sucesso = $true
                break
            }
        }
        catch {
        }
    }

    if (-not $sucesso) {
        throw "Aplicação iniciada, mas o endpoint $healthUrl não respondeu com sucesso dentro de $tentativas segundos."
    }

    Write-Host "Aplicação pronta para uso na porta $httpPort!"
}

Start-Application
