# Retrospectiva Sprint 2 — Alertas, Clasificación y Procesamiento Continuo

**Periodo:** 25 de marzo – 7 de abril de 2026  
**Equipo:** Marcos, Lucía, Diego, Gonzalo, Pablo, Íñigo, María

---

## Objetivos del sprint

- Desarrollar el motor de extracción RSS y el sistema de monitorización continua
- Implementar la lógica de definición de alertas con expansión de palabras clave mediante IA
- Implementar el proceso continuo (cron) para monitorizar alertas activas
- Construir la fase de clasificación IPTC de noticias candidatas
- Iniciar la automatización de pruebas unitarias y funcionales del backend

---

## Qué salió bien

- El motor de extracción RSS con `feedparser` quedó funcional y estable. La función fetcher nunca lanza excepciones: si un canal falla, registra el error en logs y devuelve lista vacía, garantizando que un canal caído no interrumpe la monitorización del resto.
- La integración de IA generativa con Google Gemini para expansión de palabras clave funcionó correctamente, generando entre 3 y 10 sinónimos o términos relacionados al crear una alerta, con autodetección de modelo disponible (gemini-1.5-flash, gemini-pro).
- El proceso continuo quedó operativo con APScheduler integrado en FastAPI, con expresiones cron configurables por alerta.
- Se implementó el flujo completo de verificación de email al registro: token aleatorio, expiración a 24 horas y endpoint `GET /api/v1/auth/verify-email?token=...`.
- La separación por dominios en `features/` facilitó el trabajo en paralelo sin conflictos.
- Al final del sprint había ~24 tests funcionales y ~19 tests unitarios pasando.

---

## Trabajo realizado por cada miembro

**Marcos y Lucía — Sistema de monitorización continua**

- RSS Fetcher (`features/rss_channels/fetcher.py`): función pura que descarga y normaliza noticias de un canal, tolerante a fallos.
- Keyword Matcher (`core/matcher.py`): función pura sin efectos secundarios que detecta si una noticia contiene algún descriptor de una alerta. Ubicado en `/core` para evitar dependencias circulares.
- Monitor Job (`features/alerts/monitor.py`): función orquestadora que APScheduler ejecuta en cada disparo de cron. Usa patrón get-or-create con captura de `IntegrityError` para manejar race conditions entre ejecuciones concurrentes.
- Scheduler (`core/scheduler.py`): gestión del ciclo de vida de APScheduler exponiendo `start_scheduler`, `stop_scheduler`, `register_alert_job`, `update_alert_job` y `remove_alert_job`.
- Integración en `main.py` (eventos startup/shutdown) y en `alerts/service.py` (create/update/delete de alertas).
- Nuevas dependencias: `feedparser==6.0.11` y `apscheduler==3.10.4`.

**Diego — Lógica de alertas e integración IA**

- Validación en `AlertsService` que limita la creación de alertas a un máximo de 20 por usuario.
- Nuevo endpoint `POST /api/v1/users/suggest-keywords` que usa la API de Gemini para sugerir palabras clave relacionadas.
- Gestión segura de credenciales mediante `python-dotenv` y archivo `.env` (variable `GEMINI_API_KEY`).
- Nuevos esquemas `KeywordSuggestionRequest` y `KeywordSuggestionResponse`.
- Nuevas dependencias: `google-generativeai` y `python-dotenv`.

**Gonzalo — Autenticación, verificación por email y notificaciones**

- Campos añadidos al modelo `User`: `is_verified`, `verification_token`, `verification_token_expires_at`.
- Flujo completo de verificación: generación de token, envío de correo, endpoint de verificación, expiración y limpieza del token tras uso.
- Servicio SMTP modular (`email_service.py`) para correo de verificación y correos de notificación con asunto `Actualización de <alerta> en <día/hora>`.
- Endpoints de buzón interno: `GET /api/v1/users/{user_id}/notifications` y `PATCH .../notifications/{id}/read`.
- Integración del flujo de notificación en `monitor.py`: por cada match se persiste la noticia, se crea la notificación interna y se envía el email.
- Roles iniciales en base de datos: admin, gestor, lector.
- Configuración con Gmail App Password para SMTP en producción.

**Pablo e Íñigo — QA: pruebas funcionales y unitarias**

- Reorganización de la carpeta de tests: `tests/functional/` y `tests/unit/`.
- `tests/functional/test_system_auth_alerts.py`: ~24 tests sobre health, auth y alerts (CRUD completo, casos positivos y negativos).
- `tests/unit/test_auth_service.py` y `tests/unit/test_alerts_service.py`: ~19 tests unitarios sobre lógica interna de servicios, con integraciones de IA mockeadas.
- Uso de `FakeAuthService`, `FakeAlertsService` y `dependency_overrides` para no depender de BD real.
- Actualización de `requirements.txt` con `httpx` para soporte de FastAPI TestClient en CI.

**María — Documentación y clasificador**

- Redacción de ADRs para reflejar todas las decisiones tomadas hasta el momento.
- Planteamiento del sistema clasificador de noticias.

---

## Problemas encontrados y cómo se resolvieron

- **Falsos positivos en el matching:** el sistema marcaba noticias irrelevantes. Se resolvió implementando comparación normalizada (minúsculas, sin acentos) y coincidencia de palabras completas en `matcher.py`.
- **Race conditions en monitorización concurrente:** ejecuciones paralelas del cron podían insertar la misma noticia dos veces. Se resolvió con patrón get-or-create y captura de `IntegrityError`.
- **Rate limit de la API de Gemini:** se añadió manejo de errores y fallback con los sinónimos disponibles aunque sean menos de 3.
- **Correos bloqueando el registro:** si el servidor SMTP no estaba disponible, el registro fallaba con error 500. Se refactorizó `email_service.py` para capturar la excepción SMTP y continuar el registro, registrando el error en logs.
- **Feeds RSS con formatos irregulares:** algunos canales devolvían HTML embebido, codificación incorrecta o certificados SSL problemáticos. Se añadió validación y normalización en el fetcher.

---

## Qué mejoraríamos

- Ampliar la cobertura de tests al resto de módulos (users, roles, rss_channels, notifications, stats, categories) una vez que estén estables.
- Definir desde el inicio una estrategia de QA con porcentaje mínimo de cobertura y tipos de prueba por módulo.
- Añadir pruebas de integración real con base de datos, no solo con servicios simulados.

---

## Estado al final del sprint

| Tarea                                          | Estado                                 |
| ---------------------------------------------- | -------------------------------------- |
| Motor de extracción RSS (fetcher)              | ✅ Completado                          |
| Keyword Matcher                                | ✅ Completado                          |
| Monitor Job (cron) con APScheduler             | ✅ Completado                          |
| Scheduler (ciclo de vida)                      | ✅ Completado                          |
| Lógica de alertas (máx. 20 por usuario)        | ✅ Completado                          |
| Expansión de palabras clave con Gemini         | ✅ Completado                          |
| Verificación de email con caducidad 24h        | ✅ Completado                          |
| Servicio SMTP modular                          | ✅ Completado                          |
| Buzón interno de notificaciones                | ✅ Completado                          |
| Roles iniciales en BD (admin, gestor, lector)  | ✅ Completado                          |
| Tests funcionales (health, auth, alerts)       | ✅ ~24 tests pasando                   |
| Tests unitarios (auth service, alerts service) | ✅ ~19 tests pasando                   |
| Tests del resto de módulos                     | ⚠️ Pospuesto — módulos aún no estables |

---

## Decisiones técnicas tomadas

- APScheduler integrado en FastAPI para el proceso cron (ver ADR-0007)
- Keyword Matcher ubicado en `/core` para evitar dependencias circulares
- Google Gemini con autodetección de modelo disponible para expansión de palabras clave
- Gmail App Password para autenticación SMTP en producción
