# NewsRadar

Sistema de monitorización de noticias en medios de comunicación y fuentes 
oficiales mediante canales RSS. Permite definir alertas sobre palabras clave, 
clasificar noticias por categorías IPTC y enviar notificaciones a los usuarios.

**Universidad Carlos III de Madrid — Desarrollo y Operación de Sistemas Software**  
**Grado en Ingeniería Informática — Curso 2025/2026**

---

## Equipo

| Miembro | Rol | Responsabilidad Sprint 1 |
|---|---|---|
| Íñigo | Scrum Master / DevOps | Planificación del proyecto y estructura de documentación |
| Gonzalo | DevOps / BBDD | Pipeline CI/CD con GitHub Actions |
| Pablo | DevOps / BBDD | Contenerización con Docker |
| María | Backend | Arquitectura base y modelado de datos |
| Marcos | Backend | API REST autenticación y usuarios |
| Diego | Backend / Datos | Endpoints iniciales y estructura modular |
| Lucía | Backend / Datos | Fuentes RSS y carga inicial de canales |

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3 + FastAPI + Pydantic |
| PLN | spaCy |
| Base de datos | SQLite + SQLAlchemy |
| Frontend | Vue 3 + TypeScript |
| Contenerización | Docker + docker-compose |
| CI/CD | GitHub Actions + pytest |
| Documentación API | OpenAPI / Swagger |

---

## Política de commits y ramas

No hacer commit nunca en la rama `main` directamente. Hacer una rama del 
estilo `feature/nombre-de-la-feature` y hacer una pull request para integrar 
los cambios en `main`.

- `main` — rama estable, **nunca se hace commit directo**
- `develop` — rama de integración
- `feature/nombre` — una rama por funcionalidad

Todo cambio entra mediante **Pull Request**, nunca directamente a `main`.

---

## Arrancar el sistema

### Requisitos previos
- Docker Desktop instalado y corriendo
- Git

### Pasos

```bash
git clone https://github.com/100495839/newsradar-grupo-3
cd newsradar-grupo-3
docker compose up --build
```

El backend quedará disponible en:
- API REST: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

### Consideraciones importantes respecto al Docker

- Cada miembro del equipo debe ejecutar `docker compose up --build` en su 
  propio entorno al menos una vez para construir la imagen
- El build de Docker es local, no se comparte entre usuarios
- El backend se ejecuta en `http://localhost:8000` en cada máquina individual
- Si se realizan cambios en el `Dockerfile` o en `requirements.txt`, es 
  necesario volver a ejecutar el comando con `--build`

---

## Ejecutar los tests

```bash
docker compose run backend pytest
```

Para ver el reporte de cobertura:

```bash
docker compose run backend pytest --cov=app --cov-report=html
```
---

## Estructura del repositorio

newsradar-grupo-3/
├── .github/
│   └── workflows/          # Pipeline CI/CD con GitHub Actions
├── adr/                    # Architecture Decision Records
│   ├── 0001-lenguaje-backend.md
│   ├── 0002-framework-frontend.md
│   ├── 0003-gestor-bd.md
│   ├── 0004-arquitectura-software.md
│   ├── 0005-framework-api-rest.md
│   ├── 0006-orm.md
│   └── 0007-tests-api-rest.md
├── backend/
│   └── app/
│       ├── core/           # Módulos compartidos
│       ├── db/
│       │   ├── database.py # Inicialización del ORM
│       │   ├── models.py   # Modelos SQLAlchemy
│       │   └── dict_repository.py # Capa de acceso a datos
│       ├── features/       # Módulos por dominio
│       │   ├── alerts/
│       │   ├── auth/
│       │   ├── categories/
│       │   ├── information_sources/
│       │   ├── notifications/
│       │   ├── roles/
│       │   ├── rss_channels/
│       │   ├── stats/
│       │   ├── system/
│       │   └── users/
│       ├── main.py
│       ├── news.db
│       └── seeder.py       # Carga inicial de datos
├── docs/
│   ├── architecture/       # Diagramas de arquitectura
│   └── sprints/            # Retrospectivas de cada sprint
│       └── sprint1-retrospectiva.md
├── tests/                  # Tests automatizados
├── .gitignore
├── docker-compose.yml
└── README.md

---

## Arquitectura del backend

El backend sigue una arquitectura por capas organizada en módulos por dominio.

### Estructura de `db/`
- `database.py` — código de inicialización del ORM (SQLAlchemy). Cada clase 
  en `models.py` es una tabla de la base de datos.
- `models.py` — modelos de SQLAlchemy. Cada clase es una tabla en SQLite.

> **IMPORTANTE:** el código de `db/` puede tener aspectos a mejorar en 
> iteraciones siguientes, especialmente en relaciones entre entidades.

### Estructura de `features/`

Cada subdirectorio representa un dominio del sistema y contiene:

- `router.py` — endpoints FastAPI. Se limitan a llamar a `service`
- `schemas.py` — modelos Pydantic para validación de datos
- `service.py` — clase que hereda de `CommonService` con métodos (uno por 
  cada endpoint de `router.py`) que hacen queries a la base de datos mediante 
  SQLAlchemy en vez de diccionarios de Python

---

## Documentación

- [Retrospectiva Sprint 1](docs/sprints/sprint1-retrospectiva.md)
- [ADRs — Decisiones de arquitectura](adr/)
- [API REST — Swagger](http://localhost:8000/docs)

---

## Estado del proyecto

| Sprint | Periodo | Estado |
|---|---|---|
| Sprint 1 | 11 - 24 mar 2026 | Completado |
| Sprint 2 | 25 mar - 7 abr 2026 | En curso |
