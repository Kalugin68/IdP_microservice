# Identity Provider

Identity Provider — сервис аутентификации и авторизации, реализующий OAuth.

Сервис позволяет:

* аутентифицировать пользователей;
* выдавать Authorization Code;
* обменивать Authorization Code на JWT Access Token;
* регистрировать клиентские приложения;
* централизованно выполнять вход для нескольких сервисов.
* Docker и CI/CD через Gitea Actions.

# Технологии

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Docker Compose
* JWT
* Gitea actions

# Архитектура

Сервис состоит из:

* FastAPI приложения;
* PostgreSQL базы данных;
* Docker Compose окружения.

# OAuth Flow

## 1. Получение Authorization Code (Аутентификация)

```text
Пользователь отправляет логин и пароль для аутентификации.
Idp проверяет существует ли такой пользователь в базе данных,
если да, то он генерирует код авторизации, который сохраняет
в базе данных и возвращает пользователю.
```

![Authentication Code Flow](docs/Idp_service(Authentication).drawio.png)

## 2. Получение Access Token (Авторизация)

```text
Клиент отправляет свои client_id, secret_key, которые были
получены при регистрации и также auth_code пользователя.
Idp производит проверку даннных клиента в базе данных, если всё
корректно, то после этого происходит проверка кода авторизации.
В случае если всё успешно, то Idp генерирует JWT токен, который
потом возвращает клиенту.
```

![Access Token Flow](docs/Idp_service(Authorization).drawio.png)

## 3. Регистрация клиента

```text
Клиент отправляет свой client_name.
После чего Idp генерирует client_id и secret_key.
Происходит сохранение данных в базу данных и возврат их обратно клиенту.
```

![Client Registration Flow](docs/Idp_service(Registration).drawio.png)

# Структура базы данных

## users

| Поле     | Тип     |
| -------- | ------- |
| id       | SERIAL  |
| login    | VARCHAR |
| password | VARCHAR |
| name     | VARCHAR |

## clients

| Поле          | Тип     |
| ------------- | ------- |
| id            | SERIAL  |
| client_name   | VARCHAR |
| client_id     | VARCHAR |
| client_secret | VARCHAR |

## oauth_codes

| Поле       | Тип       |
| ---------- | --------- |
| code       | UUID      |
| login      | VARCHAR   |
| expires_at | TIMESTAMP |

# API

## Авторизация пользователя

POST /oauth/authorize

Запрос:

```json
{
  "login": "admin",
  "password": "123456"
}
```

Ответ:

```json
{
  "authorization_code": "uuid"
}
```

## Получение Access Token

POST /oauth/token

Запрос:

```json
{
  "client_id": "client-id",
  "client_secret": "client-secret",
  "code": "authorization-code"
}
```

Ответ:

```json
{
  "access_token": "jwt-token",
  "token_type": "Bearer"
}
```

## Регистрация клиента

POST /clients/register

Запрос:

```json
{
  "client_name": "notifications-service"
}
```

Ответ:

```json
{
  "client_id": "uuid",
  "client_secret": "uuid"
}
```

# Healthcheck

Проверка доступности сервиса:

```http
GET /health/liveness
```

Ответ:

```json
{
  "status": "ok"
}
```

# Запуск проекта

Создать файл `.env`:

```env
JWT_SECRET=super-secret

DB_HOST=postgres
DB_PORT=5432
DB_NAME=identity_provider
DB_USER=postgres
DB_PASSWORD=postgres
```

Запуск:

```bash
docker compose up -d
```

Swagger UI:

```text
http://localhost:8004/docs
```

# CI/CD

При каждом push в ветку `main` автоматически выполняются:

1. Сборка Docker-образа.
2. Публикация образа в Docker Registry.
3. Обновление и развертывание контейнера на сервере через Docker Compose.