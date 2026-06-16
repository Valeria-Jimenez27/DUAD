# Series API — Claude Code Context

## Proyecto

REST API personal para trackear series de TV vistas, con géneros y plataformas.
Desarrollada paso a paso como proyecto de portafolio (DUAD track, Lyfter Program).

## Stack

- **Backend:** Python 3.11 + Flask 3.1
- **ORM:** SQLAlchemy 2.0 (estilo moderno con `Mapped` y `mapped_column`)
- **Base de datos:** PostgreSQL
- **Auth:** JWT (a implementar)
- **Deploy target:** Railway

## Comandos principales

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear tablas en la DB
python main.py

# Poblar con datos de prueba
python seed.py

# Correr la API (cuando exista app.py)
flask run --debug
```

## Estructura del proyecto

```
series_api/
├── app/
│   ├── __init__.py
│   ├── database.py          # engine, SessionLocal, Base, get_db()
│   └── models/
│       ├── __init__.py      # exporta Platform, Genre, Series, UserSeries
│       ├── platform.py
│       ├── genre.py
│       ├── series.py        # incluye tabla intermedia series_genres
│       └── user_series.py
├── CLAUDE.md
├── main.py
├── seed.py
├── requirements.txt
└── .env.example
```

## Modelo de datos (resumen)

- `platforms` — plataformas de streaming (Netflix, HBO, etc.)
- `genres` — géneros (Drama, Thriller, etc.)
- `series` — datos objetivos de cada serie + FK a platform
- `series_genres` — tabla intermedia many-to-many
- `user_series` — tracking personal: status, rating, review, episodios vistos

## Convenciones de código

- SQLAlchemy 2.0 style SIEMPRE: usar `Mapped[type]` y `mapped_column()`, nunca `Column()` suelto
- IDs como `String(36)` con `uuid.uuid4()` como default (no UUID nativo de Postgres)
- Nombres de tablas en **snake_case plural** (`user_series`, `series_genres`)
- Nombres de clases en **PascalCase singular** (`UserSeries`, `Series`)
- Relaciones siempre con `back_populates`, nunca `backref`
- `__repr__` en todos los modelos
- Type hints en todas las funciones

## Reglas importantes

- NUNCA hacer commits con credenciales o el archivo `.env`
- NUNCA usar raw SQL — todo a través de SQLAlchemy ORM
- Siempre usar `db.flush()` antes de acceder a IDs dentro de una sesión
- Los endpoints públicos (GET) no requieren auth; escritura (POST/PATCH/DELETE) sí
- Validaciones de negocio van en los modelos o en una capa de servicios, no en los endpoints

## Próximos pasos (en orden)

1. [ ] Crear `app.py` con Flask y blueprint base
2. [ ] Endpoints GET públicos (`/api/v1/series`, `/api/v1/series/<id>`)
3. [ ] Filtros por género, plataforma y status
4. [ ] Endpoint de estadísticas (`/api/v1/stats`)
5. [ ] Auth con JWT (login, proteger escritura)
6. [ ] Endpoints POST, PATCH, DELETE
7. [ ] Deploy en Railway
