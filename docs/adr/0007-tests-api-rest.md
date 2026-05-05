# ADR-0007: Elección de una herramienta de testing para la API REST

**Estado:** Aceptado  
**Fecha:** Marzo 2026
**Autores:** María, Lucía
**Sprint:** 2

---

## Contexto

Necesitamos una herramienta para hacer tests a los endpoints de la API REST
y asegurarnos de que su comportamiento es el esperado. Debe integrarse bien
con Python y con el pipeline de CI/CD en GitHub Actions.

## Decisión

Usaremos pytest + httpx

## Consecuencias

- pytest es el framework de testing estándar en Python, ampliamente documentado.
- httpx permite hacer peticiones HTTP asíncronas en los tests, compatible con FastAPI.
- Se integra directamente con GitHub Actions para ejecutar los tests automáticamente en cada push.
- El equipo ya tiene experiencia con pytest desde el Sprint 1.
