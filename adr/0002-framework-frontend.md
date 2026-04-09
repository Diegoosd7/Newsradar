# ADR-0002: Elección de framework para desarrollar el frontend

> ESTADO: ACEPTADO
> FECHA: 2026-03-11

## Contexto
Necesitamos un framework para desarrollar el frontend de NewsRadar, que debe 
integrarse con la API REST del backend y proporcionar una interfaz de usuario 
con dashboard, gestión de alertas, fuentes RSS y notificaciones. El framework 
debe permitir un desarrollo ágil y ser conocido por parte del equipo.

## Alternativas consideradas
- **Vue 3 + TypeScript** — conocido por parte del equipo, desarrollo ágil, 
  buena integración con APIs REST
- **React** — muy popular pero con mayor curva de aprendizaje para los miembros 
  menos experimentados
- **Angular** — robusto pero más complejo y con más boilerplate para un proyecto 
  de este tamaño

## Decisión
Usaremos Vue 3 + TypeScript como framework para el frontend.

## Consecuencias
- Parte del equipo ya tiene experiencia con Vue 3, lo que acelera el desarrollo.
- TypeScript añade tipado estático, lo que facilita la integración con las 
  interfaces de los endpoints de la API REST y reduce errores en tiempo de desarrollo.
- Vue 3 proporciona un sistema de componentes reactivos que encaja bien con 
  las necesidades del dashboard de NewsRadar.
- La curva de aprendizaje para los miembros sin experiencia previa en Vue es 
  moderada pero asumible.
