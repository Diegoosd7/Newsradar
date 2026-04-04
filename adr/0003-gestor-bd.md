# ADR-0003: Elección de sistema gestor de base de datos

> ESTADO: ACEPTADO

## Contexto

Necesitamos un sistema gestor de base de datos para almacenar los datos generados por la aplicación que tenga el rendimiento adecuado para una aplicación web y que sea fácil de integrar con el lenguaje de nuestro backend.

## Decisión

Usaremos SQLite

## Consecuencias

- Nos sentimos más cómodos bajo el paradigma SQL frente al NoSQL y SQL nos parece una solución adecuada y simple para este tipo de aplicación.
- SQLite es conocida por ser un gestor ligero, con buena integración para aplicaciones web y múltiples lenguajes de programación.
