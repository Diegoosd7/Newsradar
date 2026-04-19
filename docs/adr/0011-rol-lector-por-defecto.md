# ADR-011: Rol LECTOR por defecto cuando el usuario no tiene roles asignados

**Estado:** Aceptado  
**Fecha:** Abril 2025  
**Autores:** Marcos, Lucia  
**Sprint:** 3

---

## Contexto

El backend almacena los roles de cada usuario como un array de IDs numéricos (`role_ids: [1, 2]`). Al registrarse, un nuevo usuario no tiene ningún rol asignado hasta que el administrador se lo otorgue. El frontend necesita determinar qué interfaz y qué rutas mostrar desde el primer acceso, incluso cuando `role_ids` está vacío.

## Decisión

Si el usuario no tiene ningún rol asignado, el store `src/stores/auth.ts` le asigna el rol LECTOR por defecto.

## Razones

- El principio de mínimo privilegio dicta que, ante la duda, se debe otorgar el nivel de acceso más restrictivo.
- Un usuario sin rol asignado no debe tener acceso a funcionalidades de GESTOR (crear alertas, gestionar fuentes RSS) que podrían afectar al sistema.
- Es la decisión más segura: si se produjera un error al resolver los roles, el usuario nunca obtendría permisos superiores a los que le corresponden.

## Consecuencias

- **Positivas:** Mayor seguridad por defecto. Los nuevos usuarios no pueden acceder a funcionalidades de administración hasta que el administrador les asigne el rol correcto.
- **Negativas:** Un nuevo usuario podría confundirse al ver la interfaz limitada hasta que el administrador le asigne su rol.
- **Neutras:** El comportamiento es consistente con el modelo de seguridad del resto del sistema, donde el acceso se otorga explícitamente.

## Alternativas consideradas

| Opción | Motivo de descarte |
|---|---|
| Rol GESTOR por defecto | Viola el principio de mínimo privilegio |
| Bloquear acceso sin rol asignado | Peor experiencia de usuario; el LECTOR ya puede usar la plataforma en modo lectura |
| Lanzar error si no hay rol | Impediría el login a usuarios recién registrados |
