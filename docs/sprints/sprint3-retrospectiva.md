# Retrospectiva Sprint 3 — Panel de Mando y Notificaciones

**Periodo:** 8 – 21 de abril de 2026  
**Equipo:** María, Marcos, Lucía, Diego, Gonzalo, Pablo, Íñigo

---

## Objetivos del sprint

- Desarrollar el esqueleto del frontend en Vue 3 con TypeScript
- Construir el panel de mando con estadísticas globales y nubes de palabras por categoría
- Implementar las pantallas de gestión de perfil de usuario (edición, recuperación de contraseña)
- Configurar el envío de notificaciones por correo electrónico y buzón de la aplicación
- Implementar el correo de verificación de cuenta con caducidad de 24 horas

---

## Qué salió bien

- La arquitectura del frontend en Vue 3 con Pinia quedó bien estructurada, facilitando el trabajo en paralelo.
- El sistema de guardas de navegación por rol (GESTOR / LECTOR) funcionó correctamente: los lectores no pueden acceder a `/alertas`, `/fuentes-y-rss` ni `/admin`.
- Las estadísticas globales del dashboard se conectaron con datos reales del backend mediante un único endpoint agregado, evitando múltiples peticiones desde el frontend.
- El flujo completo de registro, verificación de email, login y visualización del estado de verificación quedó operativo de extremo a extremo.
- La nube de palabras por categoría se implementó con análisis textual real (decodificación HTML, eliminación de stopwords en ES e inglés, normalización).
- El seeder quedó operativo para poblar la BD con categorías IPTC, fuentes y canales RSS iniciales.

---

## Trabajo realizado por cada miembro

**María — Arquitectura e interfaz inicial frontend**

- Estructura general de componentes, vistas y tipos de acuerdo a los requerimientos del sistema.
- Diseño y maquetación de la interfaz para una demostración de las funcionalidades del sistema clara y una interacción fluida.
- Implementación del router para la segmentación de la aplicación en páginas.
- Planteamiento inicial para la conexión entre frontend y endpoints del backend.

**Marcos y Lucía — Autenticación y gestión de usuario**

- Proxy de desarrollo en `vite.config.ts` para evitar errores CORS (redirige `/api` a `http://localhost:8000`).
- Capa de tipos TypeScript (`src/api/types.ts`): interfaces `LoginRequest`, `TokenResponse`, `RegisterRequest`, `UserResponse`, `UserUpdateRequest`, `RoleResponse`.
- Composable HTTP centralizado (`src/api/useApiCall.ts`) con `fetch` nativo: función genérica `handleResponse<T>` y auxiliar `authHeaders()`.
- Store de autenticación con Pinia (`src/stores/auth.ts`): persistencia en localStorage, login en tres pasos con `Promise.all` (token + usuario + rol), rol LECTOR por defecto si el usuario no tiene rol asignado.
- Guardas de navegación (`src/router/index.ts`): rutas marcadas con `meta: { public }` y `meta: { requiresGestor }`.
- `LoginForm.vue` y `RegisterForm.vue` reescritos y conectados con la API real.
- `ForgotPasswordForm.vue`: UI completa con mock de 800 ms mientras el endpoint backend no estaba disponible.
- `PersonalInfo.vue`: edición de perfil (`PUT /api/v1/users/{id}`) y borrado de cuenta (`DELETE`) con confirmación.
- `AccountInfo.vue`: muestra el rol real y el estado de verificación real desde el store.
- Fix en `App.vue`: navbar condicional y logout que limpia el store y redirige al login.

**Pablo e Íñigo — Estadísticas globales y nube de palabras**

- Nuevo endpoint agregado de estadísticas en backend: devuelve en una sola respuesta fuentes, RSS, noticias, alertas, noticias por categoría, alertas por categoría y palabras destacadas por categoría.
- Procesamiento de texto para la nube: decodificación de entidades HTML, eliminación de etiquetas HTML y URLs, filtrado de stopwords en ES e inglés, normalización de texto.
- Componentes frontend: `StatsView.vue`, `PerCategoryStat.vue`, `TotalNumberStat.vue`, `WordCloudView.vue`, `WordCloudItem.vue`.
- Corrección del `seeder.py` para que cargue correctamente categorías IPTC, fuentes y canales RSS con la estructura actual del proyecto.
- Ajuste del flujo de notificaciones para que el fallo de envío de correo no bloquee la persistencia de la notificación interna.

**Diego — Flujo de recuperación de contraseña y fix de verificación**

- Nuevo componente `ResetPasswordView.vue`: lee el token de la URL, pide la nueva contraseña y se comunica con el backend.
- Nueva ruta pública `/reset-password` añadida en `router/index.ts`.
- Fix crítico en `service.py` (función `verify_email`): se añadió `self.db.commit()` para que el cambio a `is_verified = True` sea permanente en `news.db`.
- `UserResponse` actualizado con campo `is_verified: bool = False` y `model_config = {"from_attributes": True}` para compatibilidad con SQLAlchemy.
- Endpoint de login modificado para devolver el objeto `user` completo junto con el `access_token`, eliminando la llamada secundaria a `getUsers` en el frontend.
- `AccountInfo.vue`: el badge de verificación ahora es reactivo — desaparece automáticamente al iniciar sesión tras verificar la cuenta.

---

## Problemas encontrados y cómo se resolvieron

- **Errores CORS en desarrollo:** las llamadas del frontend al backend fallaban. Se resolvió configurando un proxy en `vite.config.ts` y añadiendo los headers CORS correctos en FastAPI.
- **Fallo SMTP bloqueando el registro:** si el servidor SMTP no estaba disponible, el endpoint de registro devolvía error 500. Se refactorizó el servicio para capturar la excepción y continuar el registro con un warning en logs.
- **Pérdida de sesión al recargar la página:** el store de Pinia perdía el token. Se resolvió con persistencia en localStorage mediante `pinia-plugin-persistedstate` (ver ADR-0009).
- **Endpoint de recuperación de contraseña no implementado:** se implementó un mock en el frontend con comentario indicando dónde conectar la llamada real (ver ADR-0012).
- **Desincronización del estado de verificación:** el frontend sobreescribía `is_verified` con una llamada secundaria que no traía ese campo. Se resolvió devolviendo el usuario completo en la respuesta del login y extrayendo `is_verified` directamente en el store de Pinia.
- **`verify_email` no persistía el cambio en BD:** faltaba `db.commit()` tras actualizar `is_verified`. Corregido por Diego.
- **Calidad del texto en la nube de palabras:** los feeds RSS incluían HTML embebido, entidades y ruido técnico. Se añadió una pipeline de limpieza antes de la tokenización.

---

## Qué mejoraríamos

- Acordar antes del sprint el contrato de la API entre frontend y backend para evitar bloqueos por desincronización.
- Empezar antes con las pruebas de componentes Vue — quedaron pendientes para el Sprint 4.
- Completar el endpoint real de recuperación de contraseña en el backend.
- Mejorar la nube de palabras con lematización (spaCy) y ponderación TF-IDF.

---

## Estado al final del sprint

| Tarea                                    | Estado                                                    |
| ---------------------------------------- | --------------------------------------------------------- |
| Esqueleto frontend Vue 3 con Pinia       | ✅ Completado                                             |
| Panel de mando con estadísticas globales | ✅ Completado                                             |
| Nube de palabras por categoría           | ✅ Completado                                             |
| Gestión de perfil de usuario             | ✅ Completado                                             |
| Recuperación de contraseña               | ⚠️ Mock funcional en frontend, endpoint backend pendiente |
| Notificaciones por email                 | ✅ Completado                                             |
| Buzón de notificaciones en app           | ✅ Completado                                             |
| Correo de verificación con caducidad 24h | ✅ Completado                                             |
| Fix verificación email (db.commit)       | ✅ Corregido                                              |
| Seeder operativo                         | ✅ Completado                                             |
| Pruebas de componentes frontend          | ❌ Pospuesto al Sprint 4                                  |

---

## Decisiones técnicas tomadas

- Fetch nativo en lugar de Axios para llamadas HTTP (ver ADR-0008)
- Pinia con persistencia en localStorage para mantener sesión (ver ADR-0009)
- Login en tres pasos con `Promise.all` para resolver token, usuario y rol en paralelo (ver ADR-0010)
- Rol LECTOR asignado por defecto a usuarios sin rol explícito (ver ADR-0011)
- Mock del endpoint de recuperación de contraseña en frontend hasta implementación backend (ver ADR-0012)
