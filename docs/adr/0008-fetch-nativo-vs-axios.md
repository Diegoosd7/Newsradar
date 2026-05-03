# ADR-008: Uso de fetch nativo en lugar de Axios

**Estado:** Aceptado  
**Fecha:** Abril 2025  
**Autores:** Marcos, Lucia  
**Sprint:** 3

---

## Contexto

Durante el Sprint 3 fue necesario implementar una capa de comunicación HTTP entre el frontend (Vue 3) y la API REST del backend (FastAPI). La decisión principal era elegir entre usar la librería Axios, ampliamente utilizada en proyectos Vue, o la API `fetch` nativa del navegador.

## Decisión

Se utilizó `fetch` nativo del navegador, centralizado en el composable `src/api/useApiCall.ts`.

## Razones

- `fetch` está disponible de forma nativa en todos los navegadores modernos, sin necesidad de instalar dependencias externas.
- Reducir el número de dependencias del proyecto disminuye el tamaño del bundle y el riesgo de vulnerabilidades.
- Para los casos de uso del proyecto (llamadas GET, POST, PUT, DELETE con JSON) `fetch` es suficiente y no requiere las funcionalidades adicionales de Axios.
- Se implementó una función genérica `handleResponse<T>` que cubre el manejo de errores de forma uniforme, extrayendo el campo `detail` del formato estándar de errores de FastAPI.

## Consecuencias

- **Positivas:** Sin dependencia adicional, bundle más ligero, código más explícito.
- **Negativas:** Se necesita más código boilerplate para interceptores globales si en el futuro fueran necesarios. Axios los proporciona de forma más directa.
- **Neutras:** El manejo de errores y los headers de autorización se centralizan en funciones auxiliares (`handleResponse`, `authHeaders`) dentro del mismo composable.

## Alternativas consideradas

| Opción | Motivo de descarte |
|---|---|
| Axios | Dependencia externa innecesaria para los casos de uso actuales |
| Librería ky | Desconocida para el equipo, curva de aprendizaje innecesaria |
