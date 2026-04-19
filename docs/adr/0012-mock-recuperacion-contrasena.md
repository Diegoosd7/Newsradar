# ADR-012: Mock del endpoint de recuperación de contraseña en el frontend

**Estado:** Aceptado (temporal)  
**Fecha:** Abril 2025  
**Autores:** Marcos, Lucia  
**Sprint:** 3

---

## Contexto

El Sprint 3 incluía la pantalla de recuperación de contraseña como parte de la gestión del perfil de usuario. Sin embargo, la implementación del endpoint de backend correspondiente era responsabilidad del equipo de Diego y Gonzalo, que no lo tenía disponible al inicio del sprint.

## Decisión

Se implementó el componente `ForgotPasswordForm.vue` con la UI completa (campo de email, botón de envío, mensajes de estado), pero simulando el comportamiento del backend mediante un `setTimeout` de 800 ms que siempre devuelve un mensaje genérico de éxito. Se dejó un comentario en el código indicando exactamente dónde debe sustituirse por la llamada real a la API.

## Razones

- El desarrollo del frontend no debe bloquearse por dependencias de backend no disponibles.
- La pantalla es funcional desde el punto de vista del usuario: recibe feedback visual correcto al interactuar con ella.
- El mensaje genérico de éxito ("Si existe una cuenta con ese email, recibirás instrucciones...") es además la respuesta correcta por motivos de seguridad, ya que no revela si un email está registrado o no.
- El comentario en el código facilita la integración futura sin necesidad de reescribir el componente.

## Consecuencias

- **Positivas:** El frontend avanza sin bloqueos. La UI está lista para cuando el backend esté disponible.
- **Negativas:** La funcionalidad real no está operativa hasta que el backend implemente el endpoint.
- **Neutras:** Cuando Diego y Gonzalo implementen el endpoint, solo será necesario sustituir el `setTimeout` por la llamada real a la API, sin modificar la estructura del componente.

## Pendiente

- Conectar con el endpoint real cuando el equipo de backend lo implemente.
- Retirar el `setTimeout` y el comentario asociado.

## Alternativas consideradas

| Opción | Motivo de descarte |
|---|---|
| No implementar la pantalla hasta que el backend esté listo | Bloquea el progreso del frontend innecesariamente |
| Mostrar un error indicando que no está disponible | Peor experiencia de usuario y no refleja el comportamiento final esperado |
