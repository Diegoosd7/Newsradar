# Script para ejecutar análisis de SonarQube en Windows
# Uso: .\sonar-analyze.ps1 -Token "tu_token_sonar" -SonarHostUrl "http://localhost:9000"

param(
    [Parameter(Mandatory=$true)]
    [string]$Token,
    
    [Parameter(Mandatory=$false)]
    [string]$SonarHostUrl = "http://localhost:9000"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "NewsRadar Backend - SonarQube Analysis" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "SonarQube Host: $SonarHostUrl" -ForegroundColor Green
Write-Host ""

# Paso 1: Ejecutar tests y generar reporte de cobertura
Write-Host "[1/3] Ejecutando tests y generando reporte de cobertura..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements-test.txt
if ($LASTEXITCODE -ne 0) {
    throw "Fallo instalando dependencias de test."
}

pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=html
if ($LASTEXITCODE -ne 0) {
    throw "Fallo ejecutando tests o generando cobertura."
}
Set-Location ..

# Paso 2: Descargar SonarQube Scanner si no existe
Write-Host "[2/3] Descargando SonarQube Scanner..." -ForegroundColor Yellow
if (!(Test-Path "sonar-scanner")) {
    $url = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-windows.zip"
    $output = "sonar-scanner.zip"
    
    Write-Host "Descargando desde: $url" -ForegroundColor Gray
    Invoke-WebRequest -Uri $url -OutFile $output -ErrorAction SilentlyContinue
    
    if (Test-Path $output) {
        Expand-Archive -Path $output -DestinationPath . | Out-Null
        Remove-Item $output
        Rename-Item "sonar-scanner-5.0.1.3006-windows" "sonar-scanner"
        Write-Host "SonarQube Scanner descargado correctamente" -ForegroundColor Green
    } else {
        Write-Host "Error descargando SonarQube Scanner. Asegúrate de tener conexión a internet." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "SonarQube Scanner ya existe" -ForegroundColor Green
}

# Paso 3: Ejecutar SonarQube Scanner
Write-Host "[3/3] Ejecutando SonarQube Scanner..." -ForegroundColor Yellow
$env:SONAR_SCANNER_OPTS = "-Xmx2048m"

$scannerArgs = @(
    "-Dsonar.projectBaseDir=.",
    "-Dsonar.login=$Token",
    "-Dsonar.host.url=$SonarHostUrl"
)

& "sonar-scanner\bin\sonar-scanner.bat" @scannerArgs
if ($LASTEXITCODE -ne 0) {
    throw "Fallo ejecutando SonarQube Scanner."
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Análisis completado!" -ForegroundColor Green
Write-Host "Resultados disponibles en: $SonarHostUrl/projects" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
