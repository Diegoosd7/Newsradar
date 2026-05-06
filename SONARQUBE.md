# Guía de SonarQube para NewsRadar

## ¿Qué es SonarQube?

SonarQube es una plataforma de código abierto para inspeccionar código de forma continua y medir la calidad del código. Detecta bugs, vulnerabilidades, code smells y proporciona informes de cobertura de tests.

## Requisitos

- Docker & Docker Compose
- Python 3.11+ (para ejecutar tests y SonarQube Scanner)
- 2GB de RAM disponible para SonarQube
- Token de autenticación de SonarQube

## Instalación rápida

### 1. Levantar SonarQube

```bash
# Opción 1: Con Docker Compose (recomendado)
make sonar-up

# Opción 2: Manual
docker compose up -d sonarqube-db sonarqube
```

Esto levanta:
- **SonarQube Server**: http://localhost:9000
- **PostgreSQL Database**: Puerto 5432 (interno)

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin`

### 2. Generar Token de autenticación

```bash
make sonar-token
```

O manualmente:
1. Accede a http://localhost:9000
2. Inicia sesión (admin / admin)
3. Haz clic en tu avatar → "My Account"
4. Selecciona "Security" → "Generate Tokens"
5. Ingresa un nombre (ej: "newsradar-ci") y genera
6. **Copia el token** (no podrás verlo nuevamente)

### 3. Ejecutar análisis

```bash
# Con el Makefile (recomendado)
make sonar-scan SONAR_TOKEN=tu_token_aqui

# O manualmente en Windows
.\sonar-analyze.ps1 -Token "tu_token_aqui" -Host "http://localhost:9000"

# O manualmente en Linux/Mac
bash sonar-analyze.sh
```

## Flujo completo de análisis

```bash
# 1. Levantar SonarQube
make sonar-up

# 2. Obtener token y copiar
make sonar-token

# 3. Ejecutar análisis
make sonar-scan SONAR_TOKEN=<tu_token>

# 4. Ver resultados en http://localhost:9000
```

## ¿Qué se analiza?

### Backend (Python - FastAPI)

**Archivos analizados:**
- `backend/app/**/*.py` (excepto `__pycache__` y tests)

**Métricas:**
- ✅ Cobertura de tests (pytest-cov)
- 🐛 Bugs detectados
- 🔓 Vulnerabilidades de seguridad
- 💩 Code smells (malas prácticas)
- 📏 Duplicidad de código
- 🔀 Complejidad ciclomática
- 📊 Mantenibilidad

**Cobertura de tests:**
- Generada con `pytest --cov=app --cov-report=xml`
- Archivos excluidos: tests, migraciones, etc.

### Frontend (Vue 3 + TypeScript)

**Archivos analizados:**
- `frontend/src/**/*.ts`
- `frontend/src/**/*.vue`

## Reportes generados

### Reporte de cobertura local (después de `make test-cov`)

```
backend/
├── coverage.xml       ← Importado por SonarQube
├── htmlcov/          ← Reporte HTML local
│   └── index.html    ← Abre en el navegador
└── .coverage         ← Datos crudos de coverage
```

Para ver reporte local:
```bash
# Después de make test-cov, abre:
open backend/htmlcov/index.html  # Mac
xdg-open backend/htmlcov/index.html  # Linux
start backend/htmlcov/index.html  # Windows
```

### Reporte en SonarQube Dashboard

Una vez completado el análisis, accede a:
- **Dashboard principal**: http://localhost:9000/projects
- **Proyecto NewsRadar**: http://localhost:9000/projects/newsradar
- **Cobertura**: http://localhost:9000/projects/newsradar?view=coverage
- **Issues**: http://localhost:9000/projects/newsradar?view=issues

## Comandos disponibles

```bash
# Levantar SonarQube
make sonar-up

# Obtener instrucciones para generar token
make sonar-token

# Ejecutar análisis (requiere SONAR_TOKEN)
make sonar-scan SONAR_TOKEN=<token>

# Tests con reporte local
make test-cov

# Tests sin cobertura
make test
```

## Interpretación de resultados

### A-F Rating (Calidad general)

| Rating | Significado |
|--------|---|
| 🟢 A | Excelente - Código de alta calidad |
| 🟡 B | Bueno - Algunos issues menores |
| 🟠 C | Aceptable - Mejoras recomendadas |
| 🔴 D | Malo - Muchos issues |
| ⚫ E | Crítico - Refactorización necesaria |

### Tipos de Issues

| Icono | Tipo | Impacto |
|-------|------|--------|
| 🔴 | Blocker | Falla de lógica crítica |
| 🟠 | Critical | Bug que afecta funcionalidad |
| 🟡 | Major | Defecto importante |
| ⚪ | Minor | Mejora menor recomendada |
| 💬 | Info | Información/documentación |

### Métricas importantes

- **Cobertura de tests**: Objetivo > 80%
- **Complejidad ciclomática**: Objetivo < 10 por función
- **Duplicidad**: Objetivo < 5%
- **Deuda técnica**: Estimar esfuerzo para fixes

## Integración CI/CD (GitHub Actions)

Próximamente: Agregar workflow automatizado para analizar en cada push.

Ejemplo de configuración:

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis
on: [push, pull_request]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests with coverage
        run: cd backend && pytest --cov=app --cov-report=xml
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
        with:
          args: -Dsonar.login=${{ secrets.SONAR_TOKEN }}
```

## Solución de problemas

### "Connection refused" en puerto 9000

```bash
# Verificar si SonarQube está levantado
docker ps | grep sonarqube

# Ver logs
docker logs sonarqube

# Reiniciar
docker compose down sonarqube sonarqube-db
make sonar-up
```

### "Invalid token"

1. Verifica que copiaste el token completo (sin espacios)
2. Genera uno nuevo: http://localhost:9000 → My Account → Security
3. Asegúrate de pasar el token correctamente en el comando

### SonarQube tarda mucho en levantar

- Es normal (1-2 minutos)
- Revisa recursos: `docker stats sonarqube`
- Asegúrate de tener 2GB RAM libres

### "pytest: command not found"

```bash
# Instalar dependencias
cd backend && pip install -r requirements-test.txt
```

## Tips y mejores prácticas

### 1. Ejecutar análisis localmente antes de push

```bash
make test-cov  # Ver cobertura local
make sonar-scan SONAR_TOKEN=...  # Ver en SonarQube
```

### 2. Enfocarse en Blocker y Critical issues

- No ignores issues rojo/naranja
- Code smells pueden ignorarse si es intencional

### 3. Mejorar cobertura incrementalmente

```bash
# Ver qué no está cubierto
# En browser: backend/htmlcov/index.html
# Rojo = no cubierto, verde = cubierto
```

### 4. Configurar Quality Gates (opcional)

En SonarQube: Administration → Quality Gates → Crear condición:
- Coverage >= 80%
- Maintainability Rating >= A
- Bugs = 0

## Recursos adicionales

- [Documentación oficial SonarQube](https://docs.sonarqube.org/)
- [SonarQube Python Plugin](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [SonarQube TypeScript Plugin](https://docs.sonarqube.org/latest/analysis/languages/typescript-javascript/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
