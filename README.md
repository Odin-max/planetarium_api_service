# 🌌 Planetarium API

Проєкт — API для планетарію з можливістю бронювання квитків, перегляду шоу, тем, куполу тощо. Реалізовано на Django + Django REST Framework.

---

## 📦 Вміст

- [Встановлення локально](#-встановлення-локально)
- [Запуск у Docker](#-запуск-у-docker)
- [Аутентифікація](#-аутентифікація)
- [Доступні ендпоїнти](#-доступні-ендпоїнти)
- [Документація Swagger / Redoc](#-документація)

---

## 🔧 Встановлення локально

1. Клонувати репозиторій:

```bash
git clone https://github.com/Odin-max/planetarium_api_service.git
cd planetarium_api_service
```

2. Створити `.env` файл:

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

3. Встановити залежності:

```bash
poetry install
```

4. Виконати міграції:

```bash
poetry run python manage.py migrate
```

5. Запустити сервер:

```bash
poetry run python manage.py runserver
```

---

## 🐳 Запуск у Docker

### ⚙️ Збірка та запуск

```bash
docker-compose up --build
```

> Вперше це може зайняти кілька хвилин.


## 🔐 Аутентифікація

JWT токен на основі `djangorestframework-simplejwt`.

### Реєстрація
`POST /api/user/register/`

### Отримати токен
`POST /api/user/token/`  
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Отримати оновлення токена
`POST /api/user/token/refresh/`

### Перевірка токена
`POST /api/user/token/verify/`

### Отримати дані користувача
`GET /api/user/me/`

> ⚠️ Не забудь додати `Authorization: Bearer <your_token>` у заголовок.

---

## 🧪 Тести

```bash
poetry run python manage.py test
```

---

## 🌐 Доступні ендпоїнти

Базовий префікс: `http://localhost:8000/api/planetarium/`

| Ресурс       | Метод | Endpoint                       | Опис                                |
|--------------|-------|--------------------------------|-------------------------------------|
| Show Themes  | GET   | `/themes/`                     | Перелік тем                         |
|              | POST  | `/themes/`                     | Створити тему                       |
|              | GET   | `/themes/{id}/`                | Деталі теми                         |
|              | PUT   | `/themes/{id}/`                | Оновити тему                        |
|              | DELETE| `/themes/{id}/`                | Видалити тему                       |
| Shows        | GET   | `/shows/`                      | Перелік шоу                         |
|              | POST  | `/shows/`                      | Створити шоу                        |
|              | GET   | `/shows/{id}/`                 | Деталі шоу                          |
|              | PUT   | `/shows/{id}/`                 | Оновити шоу                         |
|              | DELETE| `/shows/{id}/`                 | Видалити шоу                        |
|              | POST  | `/shows/{id}/upload-image/`    | Завантажити зображення для шоу     |
| Domes        | GET   | `/domes/`                      | Перелік куполів                     |
| Sessions     | GET   | `/sessions/`                   | Перелік сеансів                     |
| Reservations | GET   | `/reservations/`               | Перелік бронювань                   |
|              | POST  | `/reservations/`               | Створити бронювання з квитками     |

---

## 👤 Ендпоїнти користувача (`/api/user/`)

| Метод | Endpoint              | Опис                                |
|--------|------------------------|-------------------------------------|
| POST   | `/register/`          | Зареєструвати нового користувача    |
| POST   | `/token/`             | Отримати JWT токен                  |
| POST   | `/token/refresh/`     | Оновити access токен                |
| POST   | `/token/verify/`      | Перевірити валідність токена       |
| GET    | `/me/`                | Отримати інформацію про користувача (авторизовано) |
| PUT    | `/me/`                | Повністю оновити користувача        |
| PATCH  | `/me/`                | Частково оновити користувача        |

> 🛡️ Усі ендпоїнти, окрім `/register/` та `/token/`, потребують авторизації:  
`Authorization: Bearer <your_token>`

## 📘 Документація

- Swagger UI: [http://localhost:8000/api/doc/swagger/](http://localhost:8000/api/doc/swagger/)
- Redoc: [http://localhost:8000/api/doc/redoc/](http://localhost:8000/api/doc/redoc/)

---
