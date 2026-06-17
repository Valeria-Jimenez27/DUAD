# Series API

REST API personal para trackear series de TV. Permite registrar qué series viste, en qué estado están, tu rating y reseña personal.

**Live:** https://duad-4uwl.onrender.com

---

## Stack

- **Python 3.12** + **Flask 3.1**
- **SQLAlchemy 2.0** (ORM moderno con `Mapped` y `mapped_column`)
- **PostgreSQL** como base de datos
- **JWT** para autenticación
- **Deploy:** Render

---

## Modelo de datos

```
platforms ──< series >── series_genres ──< genres
                │
            user_series
```

- `platforms` — plataformas de streaming (Netflix, HBO, etc.)
- `genres` — géneros con slug
- `series` — datos de cada serie + FK a platform + relación many-to-many a genres
- `user_series` — tracking personal: status, rating, reseña, episodios vistos

---

## Endpoints

### Públicos (sin token)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/series` | Lista todas las series |
| GET | `/api/v1/series/<id>` | Detalle de una serie |
| GET | `/api/v1/stats` | Estadísticas generales |
| GET | `/api/v1/platforms` | Lista todas las plataformas |
| GET | `/api/v1/genres` | Lista todos los géneros |

**Filtros disponibles en `GET /series`:**
```
?status=completed
?genre=drama
?platform=netflix
?page=1&per_page=10
```

**Ejemplo de respuesta `GET /series`:**
```json
{
  "data": [
    {
      "id": "uuid",
      "title": "Breaking Bad",
      "year_start": 2008,
      "year_end": 2013,
      "total_seasons": 5,
      "platform": { "id": "uuid", "name": "Netflix" },
      "genres": [
        { "id": "uuid", "name": "Drama", "slug": "drama" }
      ],
      "tracking": {
        "status": "completed",
        "seasons_watched": 5,
        "episodes_watched": 62,
        "rating": 5,
        "review": "Una obra maestra."
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 4,
    "pages": 1
  }
}
```

**Ejemplo de respuesta `GET /stats`:**
```json
{
  "total_series": 10,
  "completed": 6,
  "watching": 2,
  "dropped": 1,
  "on_hold": 0,
  "plan_to_watch": 1,
  "average_rating": 4.5,
  "top_genre": "Drama",
  "top_platform": "Netflix"
}
```

---

### Protegidos (requieren token JWT)

Primero obtené el token:

```
POST /api/v1/auth/login
```
```json
{ "username": "tu_usuario", "password": "tu_password" }
```

Usá el token en el header de cada request protegido:
```
Authorization: Bearer <token>
```

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/series` | Crear serie |
| PATCH | `/api/v1/series/<id>` | Editar serie |
| PATCH | `/api/v1/series/<id>/tracking` | Actualizar tracking (upsert) |
| DELETE | `/api/v1/series/<id>` | Eliminar serie |
| POST | `/api/v1/platforms` | Crear plataforma |
| PATCH | `/api/v1/platforms/<id>` | Editar plataforma |
| DELETE | `/api/v1/platforms/<id>` | Eliminar plataforma |
| POST | `/api/v1/genres` | Crear género |
| PATCH | `/api/v1/genres/<id>` | Editar género |
| DELETE | `/api/v1/genres/<id>` | Eliminar género |

**Ejemplo `POST /series`:**
```json
{
  "title": "Severance",
  "year_start": 2022,
  "total_seasons": 2,
  "platform_id": "uuid-de-la-plataforma",
  "genre_ids": ["uuid-drama", "uuid-thriller"],
  "tracking": {
    "status": "watching",
    "seasons_watched": 2,
    "episodes_watched": 19,
    "rating": 5,
    "review": "Adictiva y perturbadora."
  }
}
```

Valores válidos para `status`: `completed` · `watching` · `dropped` · `on_hold` · `plan_to_watch`

`rating`: entero del 1 al 5

---

## Correr localmente

**1. Clonar el repositorio**
```bash
git clone https://github.com/Valeria-Jimenez27/DUAD.git
cd DUAD/series_api
```

**2. Crear entorno virtual e instalar dependencias**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configurar variables de entorno**
```bash
cp .env.example .env
# Editá .env con tus credenciales de PostgreSQL
```

`.env` requerido:
```
DATABASE_URL=postgresql://user:password@localhost:5432/series_api
FLASK_APP=main.py
FLASK_DEBUG=1
ADMIN_USERNAME=tu_usuario
ADMIN_PASSWORD=tu_password
JWT_SECRET_KEY=clave_larga_y_aleatoria
```

**4. Crear tablas y cargar datos de prueba**
```bash
python seed.py
```

**5. Correr la API**
```bash
flask run --debug
# o
python main.py
```

La API queda disponible en `http://localhost:5000`.

---

## Estructura del proyecto

```
series_api/
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── auth.py            # JWT: create_token, require_auth decorator
│   ├── database.py        # Base, SessionLocal, get_db()
│   ├── schemas.py         # Funciones de serialización a dict
│   ├── models/
│   │   ├── platform.py
│   │   ├── genre.py
│   │   ├── series.py      # Incluye tabla intermedia series_genres
│   │   └── user_series.py
│   └── routes/
│       ├── auth.py        # POST /auth/login
│       ├── series.py      # CRUD series + tracking + stats
│       ├── platforms.py   # CRUD plataformas
│       └── genres.py      # CRUD géneros
├── main.py                # Entry point
├── seed.py                # Datos de prueba
├── requirements.txt
├── Procfile               # Para deploy en Render
├── render.yaml            # Configuración de Render
└── .env.example
```
