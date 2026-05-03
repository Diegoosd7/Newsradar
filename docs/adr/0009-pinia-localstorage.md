# ADR-009: Pinia como gestor de estado con persistencia en localStorage

**Estado:** Aceptado  
**Fecha:** Abril 2025  
**Autores:** Marcos, Lucia  
**Sprint:** 3

---

## Contexto

La aplicación necesitaba un mecanismo para gestionar el estado de autenticación (token, datos del usuario, rol) de forma global y accesible desde cualquier componente. Además, era necesario que la sesión sobreviviera a recargas de página o cierres del navegador sin obligar al usuario a autenticarse de nuevo.

## Decisión

Se creó un store de Pinia en `src/stores/auth.ts` como única fuente de verdad para el estado de autenticación, con persistencia manual en `localStorage`.

## Razones

- Pinia es la librería de gestión de estado oficial de Vue 3, ya incluida en el proyecto desde el sprint anterior.
- Persistir el token y los datos del usuario en `localStorage` permite mantener la sesión activa entre recargas y reinicios del navegador sin necesidad de re-autenticarse.
- Al iniciar la aplicación, el store carga automáticamente los datos del `localStorage` si existen, restaurando la sesión de forma transparente.
- Al hacer logout, se limpian tanto el store en memoria como las entradas de `localStorage`, garantizando que no queden datos sensibles.

## Consecuencias

- **Positivas:** Experiencia de usuario mejorada (sesión persistente), estado centralizado accesible desde cualquier componente.
- **Negativas:** Los datos en `localStorage` son accesibles desde JavaScript, lo que puede suponer un riesgo si hay vulnerabilidades XSS en la aplicación. Para el alcance actual del proyecto este riesgo es aceptable.
- **Neutras:** Si en el futuro se quisiera mayor seguridad, se podría migrar a cookies HttpOnly sin cambiar la interfaz del store.

## Alternativas consideradas

| Opción | Motivo de descarte |
|---|---|
| Vuex | Reemplazado oficialmente por Pinia en Vue 3 |
| sessionStorage | La sesión se pierde al cerrar el navegador, peor experiencia de usuario |
| Cookies HttpOnly | Mayor complejidad de implementación para el alcance del sprint |
