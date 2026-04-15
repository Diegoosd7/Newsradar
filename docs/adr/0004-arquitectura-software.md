# ADR-0004: Arquitectura software de la aplicación

> ESTADO: ACEPTADO  
> FECHA: 2026-03-11

## Contexto
Necesitamos definir la arquitectura software de NewsRadar de forma que sea 
fácilmente modificable y extendible. El examen final consiste en una competición 
donde se medirá el tiempo en incorporar cambios en producción, por lo que la 
arquitectura debe minimizar el impacto de las modificaciones y facilitar el 
trabajo en paralelo entre los miembros del equipo.

## Alternativas consideradas
- **Arquitectura por capas (layered)** — clara separación de responsabilidades, 
  muy documentada para aplicaciones web
- **Arquitectura hexagonal (ports & adapters)** — más flexible pero más compleja 
  de implementar para el tamaño del equipo
- **Monolito sin capas** — más rápido de arrancar pero difícil de mantener y 
  escalar a medida que crece el proyecto

## Decisión
Usaremos una arquitectura por capas organizada en módulos por dominio (features), 
con separación clara entre la capa de base de datos, la lógica de negocio y 
la capa de presentación (API REST).

## Consecuencias
- Cada módulo (users, auth, alerts, rss_channels, etc.) es independiente, 
  lo que facilita el trabajo en paralelo entre miembros del equipo.
- La separación por capas minimiza los archivos que hay que tocar para modificar 
  o extender una funcionalidad, lo que es clave para la competición final.
- Es una arquitectura ampliamente documentada con muchos recursos de referencia.
- Como riesgo, si no se mantiene la coherencia entre módulos puede aparecer 
  duplicidad de lógica, algo a vigilar en los siguientes sprints.
