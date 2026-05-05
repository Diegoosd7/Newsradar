# Definiciones y acrónimos

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 76%" />
</colgroup>
<thead>
<tr>
<th><strong>Término</strong></th>
<th><strong>Definición</strong></th>
</tr>
<tr>
<th><strong>RSS</strong></th>
<th>Really Simple Syndication. Formato XML estándar para la sindicación
de contenidos web.</th>
</tr>
<tr>
<th><strong>IPTC</strong></th>
<th>International Press Telecommunications Council. Organismo que define
el estándar de categorías para noticias (IPTC Media Topics).</th>
</tr>
<tr>
<th><strong>IPTC Primer Nivel</strong></th>
<th>Primera jerarquía de categorías del estándar IPTC Media Topics (ej.
Política, Economía, Deportes).</th>
</tr>
<tr>
<th><strong>Alerta</strong></th>
<th>Configuración definida por un gestor que especifica un descriptor,
sus expansiones semánticas, las fuentes a monitorizar y la periodicidad
(cron).</th>
</tr>
<tr>
<th><strong>Descriptor</strong></th>
<th>Palabra clave principal o derivada que el sistema utiliza para
detectar noticias relevantes en un feed RSS.</th>
</tr>
<tr>
<th><strong>Matching</strong></th>
<th>Proceso de comparación entre los descriptores de una alerta y el
contenido de las noticias recuperadas de los canales RSS.</th>
</tr>
<tr>
<th><strong>Gestor</strong></th>
<th>Rol de usuario con capacidad para configurar alertas y fuentes de
información.</th>
</tr>
<tr>
<th><strong>ADR</strong></th>
<th>Architecture Decision Record. Registro de decisiones de diseño
arquitectónico.</th>
</tr>
<tr>
<th><strong>CI/CD</strong></th>
<th>Continuous Integration / Continuous Deployment. Práctica de
integración y despliegue automático.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# Objetivos del sistema

- **Obj. 1 - Gestión de alertas**: Definir alertas sobre descriptores con expansión semántica por IA, asociadas a categorías IPTC y fuentes RSS, con monitorización continua mediante expresión cron.
- **Obj. 2 - Clasificación de información**: Clasificar las noticias detectadas bajo una categoría IPTC (de la alerta o de la fuente RSS), garantizando que solo se usen categorías de primer nivel.
- **Obj. 3 - Gestión de notificaciones**: Notificar al usuario por buzón interno y correo electrónico cuando se detectan noticias que coinciden con los descriptores de una alerta.
- **Obj. 4 - Gestión de fuentes RSS**: Mantener un catálogo de fuentes y canales RSS categorizados por medio y por categoría IPTC, con alta mínima de 100 canales de 10 medios distintos.
- **Obj. 5 - Gestión de usuarios**: Los usuarios pueden crear una cuenta con registro verificado por email, perfil editable y control de acceso por rol.
- **Obj. 6 - Panel de mando**: Ofrecer visualización de estadísticas globales, nubes de palabras por categoría, gestión de alertas y fuentes.

# Requisitos funcionales

## RF-01 - Gestión de Usuarios

El sistema debe permitir la gestión completa del ciclo de vida de
usuarios.

- **RF-01.1**: El sistema permite el registro de nuevos usuarios con los campos: nombre, apellidos, correo electrónico válido y organización.
- **RF-01.2**: Tras el registro, el sistema envía automáticamente un correo de verificación con un enlace con caducidad de 24 horas.
- **RF-01.3**: El usuario puede activar su cuenta accediendo al enlace de verificación no caducado.
- **RF-01.4**: El sistema proporciona mecanismo de login con email y contraseña.
- **RF-01.5**: El sistema proporciona mecanismo de recuperación de contraseña mediante correo electrónico.
- **RF-01.6**: El usuario autenticado puede editar sus datos de perfil (nombre, apellidos, organización, contraseña).
- **RF-01.7**: Existe un usuario con rol administrador inicial.
- **RF-01.8**: Cada usuario registrado recibe el rol de gestor y es capaz de acceder al panel de mando del sistema.

## RF-02 Gestión de Alertas

El sistema debe permitir a los gestores definir y administrar alertas de monitorización temática.

- **RF-02.1**: Un gestor puede crear alertas hasta un máximo de 20 por usuario. Superar este límite es rechazado por el sistema.
- **RF-02.2**: Una alerta se compone de: nombre, palabra clave principal, lista de descriptores (3–10 palabras), categoría IPTC de primer nivel y expresión cron de periodicidad.
- **RF-02.3**: El gestor puede seleccionar fuentes RSS concretas para la alerta; por defecto se usan todas las de la misma categoría.
- **RF-02.4**: El gestor puede editar todos los campos de una alerta existente.
- **RF-02.5**: El gestor puede eliminar una alerta. Al eliminarla, su job de scheduler asociado se cancela.
- **RF-02.6**: El usuario puede listar todas sus alertas activas con sus parámetros de configuración.
- **RF-02.7**: La alerta puede configurarse para enviar notificaciones al buzón interno, al correo electrónico, o a ambos.

## RF-03 Sugerencias de Palabras Clave con IA

El sistema debe asistir al gestor en la definición de descriptores
mediante inteligencia artificial generativa.

- **RF-03.1**: El gestor introduce una palabra clave. El sistema consulta la API de Google Gemini y devuelve entre 3 y 10 descriptores relacionados (sinónimos, términos afines).
- **RF-03.2**: El gestor decide qué descriptores acepta e incluye en la alerta.
- **RF-03.3**: El sistema selecciona automáticamente el modelo Gemini disponible (autodetección).
- **RF-03.4**: La clave de API de Gemini se gestiona mediante variables de entorno (`.env`) y no se incluye en el repositorio.

## RF-04 Monitorización de Canales RSS

El sistema debe leer periódicamente los canales RSS configurados y
extraer las noticias publicadas.

- **RF-04.1**: El sistema lee los feeds RSS de los canales activos según la expresión cron de cada alerta.
- **RF-04.2**: Por cada ítem RSS se extraen y persisten: URL (clave de deduplicación), título, resumen, fecha de publicación y canal de origen.
- **RF-04.3**: Si un canal falla, el sistema registra el error en logs y continúa con los demás canales sin interrumpir el proceso.
- **RF-04.4**: Las noticias ya procesadas no se vuelven a insertar (deduplicación por URL única).

## RF-05 Clasificación de Información (IPTC)

Las noticias detectadas deben clasificarse bajo una categoría IPTC Media Topics de primer nivel.

- **RF-05.1**: Todas las categorías del sistema pertenecen al estándar IPTC Media Topics de primer nivel.
- **RF-05.2**: El sistema rechaza la creación de alertas o fuentes con categorías que no pertenezcan al primer nivel IPTC.
- **RF-05.3**: La categoría de una noticia se toma de la alerta que la detectó o, en su defecto, de la categoría del canal RSS origen.
- **RF-05.4**: El seeder inicial carga todas las categorías IPTC de primer nivel en la base de datos.

## RF-06 Matching de Noticias

El sistema debe comparar el contenido de las noticias recuperadas con los descriptores de las alertas activas.

- **RF-06.1**: Por cada alerta activa, el sistema compara título y resumen de cada noticia con todos los descriptores de la alerta.
- **RF-06.2**: Si se detecta coincidencia, se registra el match indicando qué descriptor lo produjo.
- **RF-06.3**: El matcher es una función pura sin efectos secundarios, ubicada en `/core` para evitar dependencias circulares.
- **RF-06.4**: El sistema evita notificaciones duplicadas mediante restricción única (`alert_id`, `news_item_id`) en base de datos.

## RF-07 Gestión de Notificaciones

El sistema debe notificar a los usuarios de las noticias detectadas tanto de forma interna como por correo electrónico.

- **RF-07.1**: Cuando se detecta un match, el sistema crea automáticamente una notificación interna en el buzón del usuario.
- **RF-07.2**: El sistema envía un correo electrónico al usuario con el asunto: "Actualización de `<alerta>` en `<día/hora>`".
- **RF-07.3**: El cuerpo del correo incluye: origen de la noticia, medio, fecha y hora, título de la noticia y resumen del RSS.
- **RF-07.4**: El sistema no genera notificaciones duplicadas para la misma combinación alerta–noticia.
- **RF-07.5**: El usuario puede consultar su buzón interno de notificaciones.
- **RF-07.6**: El usuario puede marcar notificaciones individuales como leídas.
- **RF-07.7**: Un fallo en el envío de correo no impide la persistencia de la notificación interna ni bloquea el proceso de monitorización.

## RF-08 Panel de Estadísticas

El sistema debe ofrecer un panel de mando con métricas globales del sistema actualizadas en tiempo real.

- **RF-08.1**: El panel muestra: número total de fuentes activas, número de canales RSS, número de noticias procesadas, número de alertas activas.
- **RF-08.2**: El panel muestra la distribución de noticias por categoría IPTC.
- **RF-08.3**: El panel muestra la distribución de alertas por categoría IPTC.
- **RF-08.4**: Los datos se obtienen del backend mediante un único endpoint agregado (`/stats/dashboard`) para minimizar las peticiones del frontend.
- **RF-08.5**: Los datos son dinámicos (no hardcodeados) y reflejan el estado real de la base de datos.

## RF-09 Nube de Palabras por Categoría

El sistema debe analizar el contenido textual de las noticias y
visualizar los términos más frecuentes por categoría.

- **RF-09.1**: Para cada categoría IPTC, el sistema calcula la frecuencia de términos a partir de títulos y resúmenes de las noticias procesadas.
- **RF-09.2**: El sistema aplica limpieza de texto: decodificación de entidades HTML, eliminación de etiquetas, URLs, stopwords en español e inglés y ruido técnico de RSS.
- **RF-09.3**: La visualización representa los términos con tamaño de fuente proporcional a su frecuencia.
- **RF-09.4**: Se muestra una nube global y nubes individuales por categoría.

## RF-10 Gestión de Fuentes de Información y Canales RSS

El sistema debe mantener un catálogo de fuentes de información y canales RSS categorizados.

- **RF-10.1**: Un gestor puede añadir fuentes de información asociadas a un medio de comunicación.
- **RF-10.2**: Un gestor puede añadir canales RSS a una fuente, especificando URL y categoría IPTC de primer nivel.
- **RF-10.3**: El sistema incluye un seeder con un mínimo de 100 canales RSS de 10 medios distintos, cubriendo al menos 1 canal por categoría IPTC de primer nivel.
- **RF-10.4**: Los canales RSS se pueden filtrar por categoría en la interfaz de gestión.
- **RF-10.5**: El gestor puede eliminar fuentes y canales RSS del sistema.

# Requisitos no funcionales

## RNF-01 Arquitectura Modular

- **RNF-01.1**: El backend se organiza por features (módulos de dominio), con separación clara entre router, service, schemas y modelos de datos.
- **RNF-01.2**: El frontend se organiza en vistas, componentes, stores (Pinia) y capa de API.
- **RNF-01.3**: La lógica transversal (matcher, scheduler) reside en `/core` para evitar dependencias circulares.
- **RNF-01.4**: Cada módulo debe poder ser desarrollado, testeado y desplegado de forma independiente.

## RNF-02 Despliegue Reproducible

- **RNF-02.1**: El sistema completo (backend, frontend, base de datos) se despliega mediante docker-compose up --build en un único comando.
- **RNF-02.2**: No se requiere intervención manual adicional para construir, probar y ejecutar el sistema en una máquina limpia.
- **RNF-02.3**: Las variables sensibles (claves API, credenciales SMTP) se gestionan mediante `.env`.
- **RNF-02.4**: El sistema define los entornos de desarrollo y producción de forma diferenciada.

## RNF-03 Integración y Entrega Continua (CI/CD)

- **RNF-03.1**: El repositorio tiene configurado un pipeline de CI/CD en GitHub Actions.
- **RNF-03.2**: El pipeline ejecuta automáticamente los tests en cada push o pull request.
- **RNF-03.3**: El pipeline genera informe de cobertura de código.
- **RNF-03.4**: El pipeline verifica la calidad del código.
- **RNF-03.5**: El pipeline construye la imagen Docker y valida que el sistema arranca correctamente.
- **RNF-03.6**: El repositorio tiene ramas configuradas apropiadamente con política de merges definida.

## RNF-04 Calidad del Software (Tests)

- **RNF-04.1**: El sistema cuenta con tests unitarios de la lógica de negocio.
- **RNF-04.2**: El sistema cuenta con tests funcionales de los endpoints API.
- **RNF-04.3**: Los tests cubren tanto casos positivos como negativos.
- **RNF-04.4**: Se define una estrategia de cobertura con un porcentaje mínimo objetivo por módulo.
- **RNF-04.5**: Los tests están organizados en `/tests/unit/` y `/tests/functional/`, separando ambas categorías.
- **RNF-04.6**: Opcionalmente, se incluyen pruebas de rendimiento.

## RNF-05 API REST documentada con OpenAPI

- **RNF-05.1**: Toda la funcionalidad del sistema se expone mediante una API REST.
- **RNF-05.2**: La API se documenta automáticamente con OpenAPI (Swagger UI) accesible en `/docs`.
- **RNF-05.3**: La API sigue el contrato definido en el YAML de referencia proporcionado por el enunciado (Anexo I).
- **RNF-05.4**: Todos los endpoints están protegidos según su nivel de acceso (ver sección de API).

## RNF-06 Procesamiento Asíncrono

- **RNF-06.1**: El sistema ejecuta jobs periódicos de monitorización RSS.
- **RNF-06.2**: La periodicidad de cada alerta se configura mediante una expresión cron.
- **RNF-06.3**: El scheduler se inicia y detiene con el ciclo de vida de la aplicación.
- **RNF-06.4**: Al crear, actualizar o eliminar una alerta, el job correspondiente se registra, actualiza o cancela automáticamente en el scheduler.
- **RNF-06.5**: El sistema gestiona condiciones de carrera en escrituras concurrentes.

## RNF-07 Métricas de Calidad de Código

- **RNF-07.1**: El proyecto integra una herramienta de análisis de calidad de código.
- **RNF-07.2**: Se reportan métricas de cobertura, deuda técnica, duplicidades y vulnerabilidades.
- **RNF-07.3**: El informe de calidad es accesible para el equipo docente.

## RNF-08 Documentación Técnica y ADRs

- **RNF-08.1**: La documentación está versionada junto al código en el repositorio.
- **RNF-08.2**: Se mantienen Architecture Decision Records (ADRs) en `/docs/adr/` para las decisiones de diseño relevantes.
- **RNF-08.3**: La documentación mantiene trazabilidad con requisitos, componentes y pruebas.
- **RNF-08.4**: Se documentan los prompts de IA utilizados durante el desarrollo.
- **RNF-08.5**: La documentación se genera automáticamente cuando es posible.

# Matriz de trazabilidad

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 30%" />
<col style="width: 9%" />
<col style="width: 19%" />
<col style="width: 13%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr>
<th><strong>ID</strong></th>
<th><strong>Requisito</strong></th>
<th><strong>Objetivo</strong></th>
<th><strong>Dependencias</strong></th>
<th><strong>Sprint</strong></th>
<th><strong>Estado</strong></th>
</tr>
<tr>
<th><strong>RF-01</strong></th>
<th>Gestión de usuarios</th>
<th style="text-align: center;">Obj. 5</th>
<th>RNF-01 RNF-02</th>
<th style="text-align: center;">Sprint 1–3</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<th><strong>RF-02</strong></th>
<th>Gestión de alertas</th>
<th style="text-align: center;">Obj. 1</th>
<th>RNF-01 RNF-05</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-03</strong></th>
<th>Sugerencias IA (Gemini)</th>
<th style="text-align: center;">Obj. 1</th>
<th>RNF-04</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-04</strong></th>
<th>Monitorización RSS</th>
<th style="text-align: center;">Obj. 1 4</th>
<th>RNF-03 RNF-05</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-05</strong></th>
<th>Clasificación IPTC</th>
<th style="text-align: center;">Obj. 2</th>
<th>RNF-01</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-06</strong></th>
<th>Matching de noticias</th>
<th style="text-align: center;">Obj. 1 2</th>
<th>RNF-03 RNF-05</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-07</strong></th>
<th>Gestión de notificaciones</th>
<th style="text-align: center;">Obj. 3</th>
<th>RNF-03 RNF-05</th>
<th style="text-align: center;">Sprint 2–3</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-08</strong></th>
<th>Panel de estadísticas</th>
<th style="text-align: center;">Obj. 6b</th>
<th>RNF-01</th>
<th style="text-align: center;">Sprint 3</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-09</strong></th>
<th>Nube de palabras</th>
<th style="text-align: center;">Obj. 6a</th>
<th>RNF-01</th>
<th style="text-align: center;">Sprint 3</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RF-10</strong></th>
<th>Gestión de fuentes RSS</th>
<th style="text-align: center;">Obj. 4</th>
<th>RNF-01 RNF-05</th>
<th style="text-align: center;">Sprint 1–2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<th><strong>RNF-01</strong></th>
<th>Arquitectura modular</th>
<th style="text-align: center;">—</th>
<th>Todos los RF</th>
<th style="text-align: center;">Sprint 1</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-02</strong></th>
<th>Despliegue reproducible</th>
<th style="text-align: center;">—</th>
<th>RNF-01</th>
<th style="text-align: center;">Sprint 1</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-03</strong></th>
<th>CI/CD automatizado</th>
<th style="text-align: center;">—</th>
<th>RNF-01 RNF-04</th>
<th style="text-align: center;">Sprint 1–2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-04</strong></th>
<th>Calidad software (tests)</th>
<th style="text-align: center;">—</th>
<th>RNF-03</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-05</strong></th>
<th>API REST + OpenAPI</th>
<th style="text-align: center;">Obj. 6</th>
<th>Todos los RF</th>
<th style="text-align: center;">Sprint 1</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-06</strong></th>
<th>Procesamiento asíncrono</th>
<th style="text-align: center;">Obj. 1</th>
<th>RF-05 RF-07 RF-08</th>
<th style="text-align: center;">Sprint 2</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-07</strong></th>
<th>Métricas calidad código</th>
<th style="text-align: center;">—</th>
<th>RNF-03</th>
<th style="text-align: center;">Sprint 4</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
<tr>
<th><strong>RNF-08</strong></th>
<th>ADRs en repositorio</th>
<th style="text-align: center;">—</th>
<th>Todos los RF</th>
<th style="text-align: center;">Sprint 2-4</th>
<th style="text-align: center;"><strong>Completo</strong></th>
</tr>
</thead>
<tbody>
</tbody>
</table>
