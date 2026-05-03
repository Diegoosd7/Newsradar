# Trazabilidad Sprint 3 — Autenticación y Panel de Mando

**Autores:** Marcos, Lucia  
**Sprint:** 3 (8 – 21 de abril)

---

## 1. Trazabilidad con requisitos del proyecto

| Requisito (enunciado) | Componente implementado | Archivo |
|---|---|---|
| Objetivo 5 — Gestión de usuarios: login | `LoginForm.vue` | `src/components/LoginForm.vue` |
| Objetivo 5 — Gestión de usuarios: registro | `RegisterForm.vue` | `src/components/RegisterForm.vue` |
| Objetivo 5 — Gestión de usuarios: recuperación de contraseña | `ForgotPasswordForm.vue` | `src/components/ForgotPasswordForm.vue` |
| Objetivo 5 — Gestión de usuarios: edición de datos personales | `PersonalInfo.vue` | `src/components/PersonalInfo.vue` |
| Objetivo 5 — Roles: GESTOR y LECTOR | Store de autenticación | `src/stores/auth.ts` |
| Objetivo 5 — Roles: LECTOR no gestiona alertas | Guardas de navegación | `src/router/index.ts` |
| Objetivo 6e — Panel de mando: perfil de usuario | `PersonalInfo.vue`, `AccountInfo.vue` | `src/components/` |

---

## 2. Trazabilidad con ADRs

| Decisión técnica | ADR | Componente afectado |
|---|---|---|
| Uso de `fetch` nativo en lugar de Axios | [ADR-0008](./adr/0008-fetch-nativo-vs-axios.md) | `src/api/useApiCall.ts` |
| Pinia con persistencia en localStorage | [ADR-0009](./adr/0009-pinia-localstorage.md) | `src/stores/auth.ts` |
| Flujo de login en tres pasos con Promise.all | [ADR-0010](./adr/0010-flujo-login-tres-pasos.md) | `src/stores/auth.ts` |
| Rol LECTOR por defecto sin rol asignado | [ADR-0011](./adr/0011-rol-lector-por-defecto.md) | `src/stores/auth.ts`, `src/router/index.ts` |
| Mock del endpoint de recuperación de contraseña | [ADR-0012](./adr/0012-mock-recuperacion-contrasena.md) | `src/components/ForgotPasswordForm.vue` |

---

## 3. Trazabilidad con componentes implementados

| Archivo | Descripción | Requisito | ADR relacionado |
|---|---|---|---|
| `vite.config.ts` | Proxy de desarrollo para evitar errores CORS | Objetivo 5 | — |
| `src/api/types.ts` | Interfaces TypeScript de contratos de la API | Objetivo 5 | — |
| `src/api/useApiCall.ts` | Composable centralizado de llamadas HTTP | Objetivo 5 | ADR-0008 |
| `src/stores/auth.ts` | Store de autenticación con Pinia y persistencia | Objetivo 5 | ADR-0009, ADR-0010, ADR-0011 |
| `src/router/index.ts` | Guardas de navegación por rol | Objetivo 5 | ADR-0011 |
| `src/components/LoginForm.vue` | Formulario de login conectado con la API | Objetivo 5 | ADR-0008 |
| `src/components/RegisterForm.vue` | Formulario de registro con todos los campos requeridos | Objetivo 5 | ADR-0008 |
| `src/components/ForgotPasswordForm.vue` | Pantalla de recuperación de contraseña (mock) | Objetivo 5 | ADR-0012 |
| `src/views/LoginView.vue` | Vista que gestiona LOGIN, REGISTRO y FORGOT_PASSWORD | Objetivo 5 | — |
| `src/components/PersonalInfo.vue` | Edición de perfil y borrado de cuenta | Objetivo 6e | ADR-0008 |
| `src/components/AccountInfo.vue` | Visualización de rol y estado de verificación real | Objetivo 5 | — |
| `src/App.vue` | Navbar condicional y logout integrado | Objetivo 6e | ADR-0009 |
| `backend/service.py` | Fix: registro sin SMTP no devuelve error 500 | Objetivo 5 | — |

---

## 4. Trazabilidad con pruebas

Las pruebas funcionales de los endpoints de autenticación y usuarios están cubiertas en:

- `backend/tests/test_api_endpoints.py` — cubre `POST /api/v1/auth/register`, `POST /api/v1/auth/login` y endpoints de usuarios (implementado por Pablo, Sprint 3).

Las pruebas de los componentes frontend (LoginForm, RegisterForm, guardas de router) están **pendientes** para el Sprint 4.

---

## 5. Trazabilidad con prompts de IA utilizados

| Tarea | Herramienta | Descripción del prompt utilizado |
|---|---|---|
| Implementación del composable `useApiCall.ts` | Claude / ChatGPT | Solicitud de patrón composable Vue 3 para centralizar llamadas fetch con manejo genérico de errores |
| Diseño del flujo de login en tres pasos | Claude / ChatGPT | Consulta sobre cómo resolver datos de usuario y rol en paralelo tras obtener el token |
| Guardas de navegación con `router.beforeEach` | Claude / ChatGPT | Solicitud de implementación de guardas de ruta con control por rol en Vue Router 4 |
| Fix del backend SMTP | Claude / ChatGPT | Consulta sobre cómo evitar que un fallo de email detenga el registro de usuario en FastAPI |
