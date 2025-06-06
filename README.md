# 🔐 FastAPI JWT Protected Authentication

## 📌 Описание

Задание 5 практики: реализация системы регистрации, входа и защиты эндпоинтов с использованием JWT-токенов.  
Пользователь получает токен при входе, и этот токен используется для доступа к защищённым маршрутам.

---

## 🚀 Технологии

- FastAPI
- Uvicorn
- PostgreSQL
- SQLModel (async)
- Pydantic
- python-jose
- passlib[bcrypt]
- dotenv

---

## 🧩 Установка

```bash
git clone https://github.com/dunanhub/auth_jwt_protected_api.git
cd auth_jwt_protected_api
```

```bash
# Создание и активация виртуального окружения
python -m venv .venv
source .venv/bin/activate       # для Linux/macOS
.venv\Scripts\activate        # для Windows
```

```bash
# Установка зависимостей
pip install -r requirements.txt
```

---

## 🛠 Настройки

Создайте `.env` или переменные в конфиге:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/auth_jwt_protected_api
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 📂 Структура проекта

```
fastapi_jwt_protected_authentication/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── auth.py
├── .env
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📡 Эндпоинты

- `POST /register` — регистрация пользователя
- `POST /login` — вход, получение JWT токена
- `GET /users/me` — получение текущего пользователя (требуется токен)

---

## 🔐 JWT Генерация

JWT создаётся функцией `create_access_token()` в `auth.py`.
Она кодирует `sub` (username) и `exp` (время действия) с использованием `HS256` и `SECRET_KEY`.

---

## 🧪 Тестирование (Postman)

1. `POST /register`
   Body → `x-www-form-urlencoded`:
   `username`: your_username
   `password`: your_password

2. `POST /login`
   Body → `x-www-form-urlencoded`:
   `username`: your_username
   `password`: your_password

3. Убедитесь, что вы получили токен:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

4. `GET /users/me`:
   Headers → `Authorization: Bearer <access_token>`

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. [LICENSE](./LICENSE).
