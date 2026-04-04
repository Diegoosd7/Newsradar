# ADR-0004: Arquitectura software de la aplicación

> ESTADO: ACEPTADO

## Contexto

Necesitamos una aplicación fácilmente modificable y extendible para poder añadir, modificar y quitar funcionalidades lo más rápido posible en el examen final.

## Decisión

Usaremos una arquitectura por capas.

## Consecuencias

- Que cada capa tenga una única responsabilidad minimiza la cantidad de archivos que hay que tocar para modificar o extender una funcionalidad.
- Este tipo de arquitectura es muy popular para las aplicaciones web y existen muchos recursos respecto a cómo implementarla.
