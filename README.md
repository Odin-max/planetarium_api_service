
# 🌌 Planetarium API

The project is a REST API for a planetarium system, supporting show listings, ticket reservations, dome and theme management, and user authentication. Built with Django and Django REST Framework.

---

## 📦 Contents

- [Local Installation](#-local-installation)
- [Docker Usage](#-docker-usage)
- [Authentication](#-authentication)
- [Available Endpoints](#-available-endpoints)
- [Swagger / Redoc Docs](#-documentation)

---

## 🔧 Local Installation

1. Clone the repository:

```bash
git clone https://github.com/Odin-max/planetarium_api_service.git
cd planetarium_api_service
```

2. Create a `.env` file:

```env
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=planetarium
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=localhost
SQL_PORT=5432
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

3. Install dependencies:

```bash
poetry install
```

4. Apply migrations:

```bash
poetry run python manage.py migrate
```

5. Run the server:

```bash
poetry run python manage.py runserver
```

---

## 🐳 Docker Usage

### ⚙️ Build & Run

```bash
docker-compose up --build
```

> Initial setup might take a few minutes.

---

## 🔐 Authentication

JWT-based authentication using `djangorestframework-simplejwt`.

### Register
`POST /api/user/register/`

### Obtain token
`POST /api/user/token/`  
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Refresh token
`POST /api/user/token/refresh/`

### Verify token
`POST /api/user/token/verify/`

### Get user info
`GET /api/user/me/`

> ⚠️ Add header: `Authorization: Bearer <your_token>`

---

## 🧪 Tests

```bash
poetry run python manage.py test
```

---

## 🌐 Available Endpoints

Base prefix: `http://localhost:8000/api/planetarium/`

| Resource      | Method | Endpoint                        | Description                          |
|---------------|--------|----------------------------------|--------------------------------------|
| Show Themes   | GET    | `/themes/`                      | List themes                          |
|               | POST   | `/themes/`                      | Create a theme                       |
|               | GET    | `/themes/{id}/`                 | Theme details                        |
|               | PUT    | `/themes/{id}/`                 | Update a theme                       |
|               | DELETE | `/themes/{id}/`                 | Delete a theme                       |
| Shows         | GET    | `/shows/`                       | List shows                           |
|               | POST   | `/shows/`                       | Create a show                        |
|               | GET    | `/shows/{id}/`                  | Show details                         |
|               | PUT    | `/shows/{id}/`                  | Update a show                        |
|               | DELETE | `/shows/{id}/`                  | Delete a show                        |
|               | POST   | `/shows/{id}/upload-image/`     | Upload image for show               |
| Domes         | GET    | `/domes/`                       | List domes                           |
| Sessions      | GET    | `/sessions/`                    | List sessions                        |
| Reservations  | GET    | `/reservations/`                | List reservations                    |
|               | POST   | `/reservations/`                | Create a reservation with tickets   |

---

## 👤 User Endpoints (`/api/user/`)

| Method | Endpoint              | Description                              |
|--------|------------------------|------------------------------------------|
| POST   | `/register/`          | Register a new user                      |
| POST   | `/token/`             | Obtain JWT token                         |
| POST   | `/token/refresh/`     | Refresh access token                     |
| POST   | `/token/verify/`      | Verify token validity                    |
| GET    | `/me/`                | Get user info (requires auth)            |
| PUT    | `/me/`                | Fully update user                        |
| PATCH  | `/me/`                | Partially update user                    |

> 🛡️ All except `/register/` and `/token/` require authorization:  
`Authorization: Bearer <your_token>`

---

## 📘 Documentation

- Swagger UI: [http://localhost:8000/api/doc/swagger/](http://localhost:8000/api/doc/swagger/)
- Redoc: [http://localhost:8000/api/doc/redoc/](http://localhost:8000/api/doc/redoc/)
