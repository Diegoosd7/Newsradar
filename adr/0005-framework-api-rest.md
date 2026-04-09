# ADR-0005: Elección de framework para el desarrollo de la API REST

> ESTADO: ACEPTADO  
> FECHA: 2026-03-11

## Contexto
Necesitamos un framework de Python para crear y gestionar la API REST de 
NewsRadar. La API debe estar documentada con OpenAPI/Swagger según los 
requisitos del proyecto, soportar validación de datos y ser compatible con 
el resto del stack tecnológico elegido.

## Alternativas consideradas
- **FastAPI + Pydantic** — moderno, rápido, documentación OpenAPI automática, 
  validación de datos integrada con Pydantic
- **Django REST Framework** — muy completo pero más pesado y con más 
  configuración inicial de la necesaria para este proyecto
- **Flask** — ligero y flexible pero sin documentación automática ni validación 
  de datos integrada, requiere más trabajo manual

## Decisión
Usaremos FastAPI junto con Pydantic para el desarrollo de la API REST.

## Consecuencias
- FastAPI genera documentación OpenAPI/Swagger automáticamente, cumpliendo 
  directamente uno de los requisitos del proyecto.
- Pydantic proporciona validación automática de datos en los endpoints, 
  reduciendo el código de validación manual.
- Es el framework usado por los profesores en el código de referencia 
  proporcionado, lo que facilita la alineación con los requisitos.
- FastAPI tiene soporte nativo para operaciones asíncronas, lo que mejora 
  el rendimiento en operaciones de I/O como la lectura de canales RSS.
- Como consecuencia negativa, FastAPI es más reciente que Django o Flask y 
  algunos miembros del equipo han tenido que familiarizarse con su sintaxis 
  basada en anotaciones de tipo.
