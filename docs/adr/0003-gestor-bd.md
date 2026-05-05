# ADR-0003: Elección de sistema gestor de base de datos

**Estado:** Aceptado  
**Fecha:** Marzo 2026
**Autores:** María, Lucía
**Sprint:** 2

---

## Contexto

Necesitamos un sistema gestor de base de datos para almacenar las entidades
del sistema: usuarios, alertas, fuentes RSS, canales, notificaciones y noticias
capturadas. Debe tener buen rendimiento para una aplicación web, integrarse
bien con Python y SQLAlchemy, y permitir un desarrollo ágil durante los primeros
sprints.

## Alternativas consideradas

- **SQLite** — ligero, sin servidor, integración nativa con SQLAlchemy, ideal
  para desarrollo
- **PostgreSQL** — robusto y escalable, pero requiere más configuración y
  infraestructura adicional
- **MongoDB** — flexible para datos no estructurados, pero el equipo se siente
  más cómodo con el paradigma relacional
- **ElasticSearch** — muy potente para búsqueda de texto, pero excesivo como
  base de datos principal

## Decisión

Usaremos SQLite para el entorno de desarrollo, con la previsión de migrar a
PostgreSQL en producción.

## Consecuencias

- SQLite no requiere servidor, lo que simplifica la configuración del entorno
  de desarrollo y el contenedor Docker.
- El equipo está más cómodo con el paradigma relacional (SQL) frente a NoSQL.
- SQLAlchemy abstrae el motor de base de datos, lo que facilitará la migración
  a PostgreSQL cuando sea necesario.
- Como limitación, SQLite no es escalable para producción ni soporta conexiones
  concurrentes de forma robusta, por lo que la migración a PostgreSQL es una
  deuda técnica asumida conscientemente.
