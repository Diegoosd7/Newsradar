# ADR-010: Flujo de login en tres pasos con Promise.all

**Estado:** Aceptado  
**Fecha:** Abril 2025  
**Autores:** Marcos, Lucia  
**Sprint:** 3

---

## Contexto

El endpoint `POST /api/v1/auth/login` del backend solo devuelve un token de acceso, sin incluir los datos del usuario ni su rol. Sin embargo, el frontend necesita tanto los datos del perfil como el rol (GESTOR o LECTOR) para mostrar la interfaz correcta y aplicar las guardas de navegación desde el momento del login.

## Decisión

El proceso de login se implementó en tres pasos dentro del store `src/stores/auth.ts`:

1. `POST /api/v1/auth/login` → obtener el token de acceso.
2. `GET /api/v1/users/` → obtener la lista de usuarios y localizar al usuario actual por su email.
3. `GET /api/v1/roles` → obtener los nombres de todos los roles del sistema.

Los pasos 2 y 3 se ejecutan en paralelo usando `Promise.all` para minimizar la latencia.

## Razones

- El backend no ofrece un endpoint que devuelva token + datos de usuario en una sola llamada, por lo que es necesario realizar llamadas adicionales.
- Ejecutar los pasos 2 y 3 en paralelo con `Promise.all` evita la penalización de latencia de hacerlos secuencialmente.
- Resolver el rol en el momento del login permite que las guardas de navegación funcionen correctamente desde la primera ruta a la que accede el usuario.

## Consecuencias

- **Positivas:** El usuario tiene todos sus datos disponibles inmediatamente tras el login, sin llamadas adicionales al navegar.
- **Negativas:** El login realiza tres llamadas HTTP en lugar de una. Si el backend en el futuro ofrece un endpoint `/me` que devuelva token + datos, este flujo podría simplificarse.
- **Neutras:** Si cualquiera de los tres pasos falla, el login completo falla y se muestra el error al usuario, evitando estados inconsistentes.

## Alternativas consideradas

| Opción | Motivo de descarte |
|---|---|
| Llamadas secuenciales (paso a paso) | Mayor latencia total innecesaria |
| Endpoint `/me` propio | No disponible en la API actual del backend |
| Guardar solo el token y resolver el perfil después | El rol es necesario en la primera navegación para las guardas |
