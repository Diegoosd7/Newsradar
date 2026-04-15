# ADR-0001: Elección de lenguaje de programación para desarrollar el backend

> ESTADO: ACEPTADO
> FECHA: 2026-03-11

## Contexto
Necesitamos un lenguaje que nos permita desarrollar el backend, incluyendo 
la API REST y funcionalidades de Procesamiento del Lenguaje Natural (PLN) 
para la expansión de descriptores en alertas. El lenguaje debe ser conocido 
por el equipo, tener un ecosistema maduro para IA y facilitar la integración 
con las herramientas proporcionadas por los profesores.

## Alternativas consideradas
- **Python 3** — amplio ecosistema, familiar para el equipo, usado por los profesores
- **Java** — robusto pero más verboso y sin ventajas claras para PLN
- **Node.js** — buena opción para APIs REST pero ecosistema de IA inferior a Python

## Decisión
Usaremos Python 3 como lenguaje principal del backend.

## Consecuencias
- Todo el equipo está familiarizado con Python, lo que reduce la curva de aprendizaje.
- Amplio ecosistema de librerías para IA y PLN (spaCy, transformers, etc.).
- Fácil integración con FastAPI, SQLAlchemy y otras herramientas del stack.
- Los profesores proporcionaron código de referencia en Python, lo que facilita 
  la alineación con los requisitos del proyecto.
- Como consecuencia negativa, Python es más lento que Java o Go en rendimiento 
  puro, aunque esto no es crítico para este proyecto.
