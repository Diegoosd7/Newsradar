# NewsRadar

## Commits

No hacer commit nunca en la rama main directamente. Hacer una rama del estilo `feature/nombre-de-la-feature` o similar (lo iremos viendo) y hacer una pull request para poder integrar los cambios en la rama main.

## Backend

La estructura del backend es la siguiente:

- `core`: módulos compartidos en múltiples archivos

- `db`: módulos referentes a la BBDD
  - `database`: código de inicialización del ORM (la IA me recomendó SQAlchemy pero se puede cambiar a cualquier otro que queraís si tenéis experiencia con algún otro)
  - `models`: modelos de SQLAlchemy. Cada clase es una tabla que hay que crear en por ejemplo SQLite (o cualquier otro gestor SQL que queráis si tenéis experiencia con algún otro)

IMPORTANTE: el código de `db` posiblemente tenga cosas mal en ambos archivos.

- `features`: el código original separado por funcionalidades (según el endpoint). Usa FastAPI
  - `router.py`: Endpoints. Se limitan a llamar a service
  - `schemas.py`: modelos de pydantic
  - `service.py`: Clase que hereda de CommonService con métodos (1 por cada endpoint de router.py) a rellenar para seguir el mismo comportamiento del API REST original pero esta vez haciendo queries a nuestra BBDD (usando la librería SQLAlchemy o cualquier otro ORM que queráis) en vez de diccionarios de python

### Consideraciones importantes respecto al DOCKER

- Cada miembro del equipo debe ejecutar `docker compose up --build` en su propio entorno al menos una vez para construir la imagen
- El build de Docker es local, no se comparte entre usuarios
- El backend se ejecuta en `http://localhost:8000` en cada máquina individual
- Si se realizan cambios en el Dockerfile o en `requirements.txt`, es necesario volver a ejecutar el comando con `--build`
