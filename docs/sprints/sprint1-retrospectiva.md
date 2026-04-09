# Retrospectiva Sprint 1 — Infraestructura, API Base y Fuentes RSS

**Periodo:** 11 - 24 de marzo de 2026  
**Equipo:** Íñigo, Gonzalo, Pablo, María, Marcos, Diego, Lucía

---

## Resumen del sprint

El objetivo principal del Sprint 1 era disponer de una base funcional sobre la 
que iterar en siguientes sprints. Este objetivo se ha cumplido: el backend arranca, 
la base de datos es operativa y los primeros endpoints están implementados. Sin 
embargo, la base construida es válida para desarrollo pero aún no es una 
arquitectura sólida.

---

## Trabajo realizado por cada miembro

### Íñigo — Scrum Master / DevOps
Planificación inicial del proyecto y preparación de la estructura base del 
repositorio. Durante este sprint la planificación se documentó fuera de GitHub, 
lo cual se identifica como una deuda a corregir en el Sprint 2.

### María y Marcos — Backend
Se definió la arquitectura base del backend con FastAPI, estableciendo la 
separación por módulos (features) y la carpeta específica para base de datos. 
Modeló las entidades iniciales en `models.py` y configuró la conexión con SQLite 
en `database.py`. También planteó una capa de acceso a datos mediante 
`dict_repository.py` siguiendo el patrón repository, aunque su integración con 
el ORM queda pendiente de consolidar.

### Diego y Lucía — Backend / Datos
Se implementó los endpoints iniciales dentro de la estructura modular por 
dominios: `users`, `auth`, `alerts`, `rss_channels`, `notifications`, entre otros. 
Implementó el endpoint `/health` en `system/router.py` como punto de validación 
del sistema, e integró el `seeder.py` para poblar la base de datos con datos 
iniciales, lo que facilita el desarrollo y las pruebas.

### Pablo y Gonzalo — DevOps
Se configuró la contenerización del backend mediante `Dockerfile` y 
`docker-compose.yml`. El sistema arranca de forma consistente en cualquier 
entorno con un único comando (`docker-compose up --build`) y el servicio queda 
expuesto en `localhost:8000`.
Se configuró el pipeline de CI/CD en GitHub Actions para la automatización de 
pruebas con pytest. Actualizó `requirements.txt` con las dependencias necesarias, 
creó la carpeta `tests/` con una prueba básica de validación del flujo de trabajo 
y resolvió el error `docker-compose: command not found` en el entorno de CI.

---

## Qué salió bien

- Arquitectura modular clara y escalable desde el primer sprint
- Backend funcional con base de datos operativa
- Entorno reproducible con Docker, reduciendo problemas de configuración entre 
  desarrolladores
- Pipeline CI/CD operativo desde el inicio del proyecto
- Seeder para poblar datos iniciales, acelerando el desarrollo

---

## Problemas detectados

- **Modelo de datos incompleto:** no hay relaciones definidas entre entidades 
  (`relationship()`), lo que supone un riesgo alto de inconsistencia al escalar
- **Sin migraciones:** no existe ningún mecanismo de control de esquemas 
  (Alembic u similar), lo que dificulta la evolución de la base de datos
- **SQLite no escalable:** válida para desarrollo pero no para producción
- **Patrón de acceso a datos inconsistente:** no está claro si se usa ORM o 
  repositorio, lo que puede generar duplicidad de lógica entre módulos
- **Planificación fuera de GitHub:** los sprints e issues no se reflejaron en 
  GitHub durante este sprint, algo que el equipo reconoce como un error a corregir
- **Sin diagramas de arquitectura:** falta el diagrama entidad-relación y el 
  diagrama de componentes
- **Sin ADRs documentados:** las decisiones de diseño no están registradas formalmente

---

## Acciones para Sprint 2

- [ ] Registrar toda la planificación en GitHub Projects desde el inicio
- [ ] Crear ADRs con las decisiones de diseño tomadas en Sprint 1
- [ ] Elaborar diagrama entidad-relación y diagrama de componentes
- [ ] Consolidar modelos de datos y definir relaciones entre entidades
- [ ] Establecer estrategia de migraciones con Alembic
- [ ] Aclarar y estandarizar el patrón de acceso a datos
- [ ] Mejorar la integración de IA generativa
