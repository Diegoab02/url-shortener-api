# URL Shortener API

API REST para acortar URLs construida con FastAPI y PostgreSQL.

## Stack
- **FastAPI** — framework web
- **PostgreSQL** — base de datos
- **SQLAlchemy** — ORM
- **Docker** — contenedores
- **pytest** — tests

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/urls/shorten` | Crear URL corta |
| GET | `/urls/` | Listar todas las URLs |
| GET | `/urls/{code}` | Redirigir a URL original |
| GET | `/urls/stats/{code}` | Ver estadísticas |
| DELETE | `/urls/{code}` | Eliminar URL |

## Correr el proyecto

```bash
# 1. Clonar el repo
git clone https://github.com/Diegoab02/url-shortener-api.git
cd url-shortener-api

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar la base de datos
docker-compose up db -d

# 4. Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 5. Correr el servidor
uvicorn app.main:app --reload
```

Documentación interactiva en: http://localhost:8000/docs

## Tests

```bash
pytest tests/ -v
```