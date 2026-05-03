# Registro de Prompts de IA — NewsRadar

Este documento recoge los prompts utilizados con herramientas de IA generativa
durante el desarrollo del proyecto NewsRadar, cumpliendo con el requisito de
trazabilidad de la asignatura.

**Herramientas utilizadas:** ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google)

---

## Sprint 1 — Infraestructura, API Base y Fuentes RSS

| ID | Herramienta | Tarea | Prompt utilizado | Resultado / Uso |
|----|-------------|-------|------------------|-----------------|
| P-S1-01 | ChatGPT | Estructura del proyecto FastAPI | "Genera una estructura de carpetas para un proyecto FastAPI con arquitectura por dominios (features), SQLAlchemy y autenticación JWT" | Base de la estructura `backend/app/features/` |
| P-S1-02 | Claude | Modelos SQLAlchemy | "Genera los modelos SQLAlchemy para un sistema de usuarios con roles, canales RSS y categorías IPTC. Usa SQLite como base de datos" | Base de `backend/app/db/models.py` |
| P-S1-03 | ChatGPT | Docker Compose | "Crea un docker-compose.yml para un backend FastAPI con Python 3.11 y un frontend Vue 3 con Vite, incluyendo hot-reload en desarrollo" | Base de `docker-compose.yml` |
| P-S1-04 | Gemini | Canales RSS IPTC | "Lista 100 canales RSS de medios de comunicación españoles organizados por las categorías de primer nivel de IPTC Media Topics" | Datos para `backend/app/seeder.py` |
| P-S1-05 | Claude | GitHub Actions CI | "Crea un pipeline de GitHub Actions para un proyecto Python con FastAPI que ejecute pytest con cobertura y construya una imagen Docker" | Base de `.github/workflows/ci.yml` |

---

## Sprint 2 — Alertas, Clasificación y Procesamiento Continuo

| ID | Herramienta | Tarea | Prompt utilizado | Resultado / Uso |
|----|-------------|-------|------------------|-----------------|
| P-S2-01 | ChatGPT | Motor RSS con feedparser | "Implementa en Python un servicio que consuma canales RSS con feedparser, filtre noticias por palabras clave y las almacene en SQLite con SQLAlchemy" | Base del motor de extracción RSS |
| P-S2-02 | Claude | Expansión de palabras clave con IA | "Dado un término de búsqueda en español, genera entre 3 y 10 sinónimos o palabras relacionadas usando la API de OpenAI. Devuelve solo la lista en JSON" | Lógica de recomendación de descriptores en alertas |
| P-S2-03 | Gemini | Clasificación IPTC | "Dado el título y resumen de una noticia en español, clasifícala en una de las siguientes categorías IPTC de primer nivel: [lista]. Responde solo con el nombre de la categoría" | Sistema de clasificación IPTC |
| P-S2-04 | ChatGPT | Tarea cron con APScheduler | "Implementa una tarea periódica en FastAPI usando APScheduler que ejecute una función cada X minutos definido por una expresión cron almacenada en base de datos" | Proceso continuo de monitorización de alertas |
| P-S2-05 | Claude | Pruebas unitarias FastAPI | "Genera tests con pytest para los endpoints FastAPI de gestión de alertas, usando TestClient y una base de datos SQLite en memoria" | Base de `tests/test_alerts.py` |

---

## Sprint 3 — Panel de Mando y Notificaciones

| ID | Herramienta | Tarea | Prompt utilizado | Resultado / Uso |
|----|-------------|-------|------------------|-----------------|
| P-S3-01 | Claude | Composable fetch Vue 3 | "Solicitud de patrón composable Vue 3 para centralizar llamadas fetch con manejo genérico de errores" | `src/api/useApiCall.ts` |
| P-S3-02 | ChatGPT | Flujo de login en tres pasos | "Consulta sobre cómo resolver datos de usuario y rol en paralelo tras obtener el token JWT en Vue 3 con Pinia" | `src/stores/auth.ts` |
| P-S3-03 | Claude | Guardas de navegación por rol | "Implementación de guardas de ruta con control por rol en Vue Router 4, diferenciando entre GESTOR y LECTOR" | `src/router/index.ts` |
| P-S3-04 | ChatGPT | Nube de palabras con D3.js | "Genera un componente Vue 3 que muestre una nube de palabras usando D3-cloud a partir de un array de objetos {text, value}" | Componente de nube de palabras del dashboard |
| P-S3-05 | Gemini | Plantilla de correo de notificación | "Genera una plantilla HTML para un correo de notificación de alerta con el formato: Actualización de [alerta] en [día/hora], mostrando título, fuente y resumen de la noticia" | Plantilla de notificaciones por email |
| P-S3-06 | Claude | Fix backend SMTP | "Consulta sobre cómo evitar que un fallo de email detenga el registro de usuario en FastAPI — manejo de excepciones en envío SMTP" | Fix en `backend/service.py` |
| P-S3-07 | ChatGPT | Estadísticas globales API | "Genera un endpoint FastAPI que devuelva estadísticas agregadas: número de fuentes, noticias totales, noticias por categoría, alertas totales y alertas por categoría" | Endpoint `/api/v1/stats` |

---

## Sprint 4 — CI/CD, Documentación y Refinamiento

| ID | Herramienta | Tarea | Prompt utilizado | Resultado / Uso |
|----|-------------|-------|------------------|-----------------|
| P-S4-01 | Claude | Pruebas de rendimiento Locust | "Genera un locustfile.py para pruebas de carga de una API REST FastAPI que simule login, consulta de alertas y consulta de noticias con usuarios concurrentes" | `tests/locustfile.py` |
| P-S4-02 | ChatGPT | Informe de cobertura CI | "Añade al pipeline de GitHub Actions la generación de un informe de cobertura con pytest-cov y la subida del artefacto" | Mejora de `.github/workflows/ci.yml` |
| P-S4-03 | Gemini | Diagramas de arquitectura Mermaid | "Genera un diagrama de componentes en formato Mermaid para un sistema con backend FastAPI, frontend Vue 3, SQLite, motor RSS y sistema de notificaciones" | `docs/architecture/components.md` |
| P-S4-04 | Claude | Documento de trazabilidad | "Genera una tabla de trazabilidad entre requisitos del enunciado, componentes implementados, ADRs y tests para un sistema de monitorización de noticias RSS" | `docs/trazabilidad.md` |

---

## Notas

- Los prompts recogidos son representativos del uso real durante el desarrollo.
- En todos los casos el código generado fue revisado, adaptado y validado por
  el equipo antes de integrarse en el repositorio.
- El uso de IA se enmarca en la Opción 1 de la política de IA de la asignatura.
