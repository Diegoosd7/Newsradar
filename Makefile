.PHONY: all setup test build deploy clean help

COMPOSE = docker compose
PYTHON  = python3
PIP     = pip

help:
	@echo "NewsRadar - Comandos disponibles:"
	@echo "  make all      Ejecuta setup, test, build y deploy completo"
	@echo "  make setup    Crea el fichero .env desde .env.example"
	@echo "  make test     Ejecuta todos los tests del backend"
	@echo "  make build    Construye las imágenes Docker"
	@echo "  make deploy   Despliega la aplicación con Docker Compose"
	@echo "  make clean    Para y elimina los contenedores y volúmenes"

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
