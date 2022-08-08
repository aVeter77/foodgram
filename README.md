# Foodgram, «Продуктовый помощник»

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

![example workflow](https://github.com/aVeter77/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Пример работы приложения [http://foodgram.aveter77.site/recipes/](http://foodgram.aveter77.site/recipes/)

Полное описание API [http://foodgram.aveter77.site/api/docs/](http://foodgram.aveter77.site/api/docs/)

Образы на Dockerhub:
- [Backend](https://hub.docker.com/r/aveter77/backend_foodgram/tags)
- [Frontend](https://hub.docker.com/r/aveter77/frontend_foodgram/tags)

## Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на эндпоинт `/api/users/` с параметрами
```
{
  "email": "mail@domain.ru",
  "username": "username",
  "first_name": "First_name",
  "last_name": "Last_name",
  "password": "password"
}
```
2. Пользователь отправляет POST-запрос на эндпоинт `/api/auth/token/login/`, с параметрами 
```
{
  "password": "string",
  "email": "string"
}
```
в ответе на запрос приходит `auth_token`, затем этот токен передаётся в заголовке `Authorizaton` каждого запроса

## Для неавторизованных пользователей
- Доступна главная страница.
- Доступна страница отдельного рецепта.
- Доступна форма авторизации.
- Доступна система восстановления пароля.
- Доступна форма регистрации.

## Для авторизованных пользователей:

- Доступна главная страница.
- Доступна страница другого пользователя.
- Доступна страница отдельного рецепта.
- Доступна страница «Мои подписки».
  1. Можно подписаться и отписаться на странице рецепта.
  2. Можно подписаться и отписаться на странице автора.
  3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
- Доступна страница «Избранное».
  1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
  2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
- Доступна страница «Список покупок».
  1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
  2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
  3. Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
  4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
- Доступна страница «Создать рецепт».
  1. Есть возможность опубликовать свой рецепт.
  2. Есть возможность отредактировать и сохранить изменения в своём рецепте.
  3. Есть возможность удалить свой рецепт.
- Доступна форма изменения пароля.
- Доступна возможность выйти из системы (разлогиниться).

## Технологии
- [Python 3.7](https://www.python.org/)
- [Django 2.2.16](https://www.djangoproject.com/)
- [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
- [PostgreSQL 13.0](https://www.postgresql.org/)
- [gunicorn 20.0.4](https://pypi.org/project/)
- [nginx 1.21.3](https://nginx.org/ru/)
- [Docker 20.10.17](https://www.docker.com/)
- [Docker Compose 1.29.2](https://docs.docker.com/compose/)

## Запуск

Установите переменные среды, как в `.env.example`.
### Docker
```
cd infra/
docker-compose up -d
```
После запуска выполните команды:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```

## Заполнение базы начальными данными
```
cd infra/
cat fixtures.json | docker-compose exec -T backend python manage.py loaddata --format=json -
docker-compose cp media_fixtures/recipes/ backend:/app/media/
```

## Примеры запросов

**Регистрация нового пользователя:**
```
POST /api/users/
```
```
{
  "email": "mail@domain.ru",
  "username": "username",
  "first_name": "First_name",
  "last_name": "Last_name",
  "password": "password"
}
```
**Получение токена:**

```
POST /api/auth/token/login/
```
```
{
  "password": "string",
  "email": "string"
}
```

**Получение списка всех пользователей:**

```
GET /api/users/
```

**Список рецептов:**

```
GET /api/recipes/
```
**Создать рецепт:**
```
POST api/recipes/
```
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

## Автор
Александр Николаев

## Лицензия

MIT
