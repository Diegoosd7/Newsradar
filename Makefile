.PHONY: all setup test build deploy clean help

COMPOSE = docker compose
PYTHON  = python3
PIP     = pip

help:
	@echo "NewsRadar - Comandos disponibles:"
	@echo "  make all         Ejecuta setup, test, build y deploy completo"
	@echo "  make setup       Crea el fichero .env desde .env.example"
	@echo "  make test        Ejecuta todos los tests del backend"
	@echo "  make test-cov    Ejecuta tests con reporte de cobertura"
	@echo "  make sonar-up    Levanta SonarQube (requiere docker-compose)"
	@echo "  make sonar-scan  Ejecuta análisis SonarQube (requiere SONAR_TOKEN)"
	@echo "  make build       Construye las imágenes Docker"
	@echo "  make deploy      Despliega la aplicación con Docker Compose"
	@echo "  make clean       Para y elimina los contenedores y volúmenes"

all: setup test build deploy
	@echo ""
	@echo "Despliegue completado."
	@echo "  Backend:  http://localhost:8000"
	@echo "  Frontend: http://localhost:80"
	@echo "  API docs: http://localhost:8000/docs"

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env creado desde .env.example. Edítalo si necesitas claves reales."; \
	else \
		echo ".env ya existe, no se sobreescribe."; \
	fi

test:
	@echo "Instalando dependencias de backend..."
	cd backend && $(PIP) install -q -r requirements-test.txt
	@echo "Ejecutando tests unitarios..."
	cd backend && pytest tests/unit -v --tb=short -q
	@echo "Ejecutando tests funcionales..."
	cd backend && pytest tests/functional -v --tb=short -q
	@echo "Ejecutando tests e2e..."
	cd backend && pytest tests/e2e -v --tb=short -q
	@echo "Ejecutando tests de endpoints..."
	cd backend && pytest tests/test_api_endpoints.py -v --tb=short -q

test-cov:
	@echo "Instalando dependencias de backend..."
	cd backend && $(PIP) install -q -r requirements-test.txt
	@echo "Ejecutando tests con reporte de cobertura..."
	cd backend && pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "Reportes generados:"
	@echo "  - XML: backend/coverage.xml"
	@echo "  - HTML: backend/htmlcov/index.html"
	@echo ""
	@echo "Para ver el reporte HTML, abre: $(PWD)/backend/htmlcov/index.html"

sonar-up:
	@echo "Levantando SonarQube..."
	$(COMPOSE) up -d sonarqube-db sonarqube
	@echo ""
	@echo "Esperando a que SonarQube arranque (esto puede tardar ~1 minuto)..."
	@for i in $$(seq 1 30); do \
		if curl -sf http://localhost:9000/api/system/health > /dev/null 2>&1; then \
			echo "SonarQube activo en http://localhost:9000"; \
			echo "Credenciales por defecto: admin / admin"; \
			break; \
		fi; \
		echo "  Intento $$i/30..."; \
		sleep 2; \
	done

sonar-token:
	@echo "Para obtener tu token de SonarQube:"
	@echo "1. Accede a http://localhost:9000"
	@echo "2. Inicia sesión (admin / admin)"
	@echo "3. Haz clic en tu avatar (arriba a la derecha)"
	@echo "4. Selecciona 'My Account' -> 'Security'"
	@echo "5. Genera un nuevo token"
	@echo "6. Copia el token y úsalo con: make sonar-scan SONAR_TOKEN=tu_token"

sonar-scan:
	@if [ -z "$(SONAR_TOKEN)" ]; then \
		echo "Error: SONAR_TOKEN no está definido"; \
		echo "Uso: make sonar-scan SONAR_TOKEN=tu_token"; \
		echo "Para obtener el token, ejecuta: make sonar-token"; \
		exit 1; \
	fi
	@echo "Ejecutando análisis SonarQube..."
	@echo "SONAR_TOKEN=$(SONAR_TOKEN)" | wc -c > /dev/null
	cd backend && $(PIP) install -q -r requirements-test.txt
	cd backend && pytest tests/ --cov=app --cov-report=xml:coverage.xml
	@echo "Descargando SonarQube Scanner..."
	@if [ ! -d "sonar-scanner" ]; then \
		wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip 2>/dev/null || \
		curl -s -o sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip; \
		unzip -q sonar-scanner.zip 2>/dev/null || true; \
		rm -f sonar-scanner.zip; \
		mv -f sonar-scanner-5.0.1.3006-linux sonar-scanner 2>/dev/null || true; \
	fi
	@echo "Ejecutando SonarQube Scanner..."
	export SONAR_SCANNER_OPTS="-Xmx2048m"; \
	sonar-scanner/bin/sonar-scanner \
		-Dsonar.projectBaseDir=. \
		-Dsonar.login=$(SONAR_TOKEN) \
		-Dsonar.host.url=http://localhost:9000
	@echo ""
	@echo "Análisis completado!"
	@echo "Resultados: http://localhost:9000/projects

build:
	@echo "Construyendo imágenes Docker..."
	$(COMPOSE) build

deploy:
	@echo "Desplegando con Docker Compose..."
	$(COMPOSE) up -d
	@echo "Esperando a que el backend arranque..."
	@for i in $$(seq 1 12); do \
		if curl -sf http://localhost:8000/docs > /dev/null 2>&1; then \
			echo "Backend activo en http://localhost:8000"; \
			break; \
		fi; \
		echo "  Intento $$i/12..."; \
		sleep 5; \
	done

clean:
	$(COMPOSE) down -v --remove-orphans
