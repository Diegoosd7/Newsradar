#!/bin/bash
# Script para ejecutar análisis de SonarQube en el backend

set -e

echo "=========================================="
echo "NewsRadar Backend - SonarQube Analysis"
echo "=========================================="

# Verificar que se proporcione el token de SonarQube
if [ -z "$SONAR_TOKEN" ]; then
    echo "Error: SONAR_TOKEN no está definido"
    echo "Uso: SONAR_TOKEN=tu_token bash sonar-analyze.sh"
    exit 1
fi

SONAR_HOST_URL=${SONAR_HOST_URL:-http://localhost:9000}

echo "SonarQube Host: $SONAR_HOST_URL"
echo ""

# Paso 1: Ejecutar tests y generar reporte de cobertura
echo "[1/3] Ejecutando tests y generando reporte de cobertura..."
cd backend
pip install -r requirements-test.txt > /dev/null 2>&1
pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=html || true
cd ..

# Paso 2: Descargar SonarQube Scanner si no existe
echo "[2/3] Descargando SonarQube Scanner..."
if [ ! -d "sonar-scanner" ]; then
    wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
    unzip -q sonar-scanner-cli-5.0.1.3006-linux.zip
    rm sonar-scanner-cli-5.0.1.3006-linux.zip
    mv sonar-scanner-5.0.1.3006-linux sonar-scanner
fi

# Paso 3: Ejecutar SonarQube Scanner
echo "[3/3] Ejecutando SonarQube Scanner..."
export SONAR_SCANNER_OPTS="-Xmx2048m"
sonar-scanner/bin/sonar-scanner \
  -Dsonar.projectBaseDir=. \
  -Dsonar.login=$SONAR_TOKEN \
  -Dsonar.host.url=$SONAR_HOST_URL

echo ""
echo "=========================================="
echo "Análisis completado!"
echo "Resultados disponibles en: $SONAR_HOST_URL/projects"
echo "=========================================="
