![Workflow](https://github.com/Hrushon/yamdb_final/actions/workflows/foodgram_workflow.yml/badge.svg)

# FOODGRAM
## Продуктовый помощник

Проект предоставляет возможность пользователям просматривать кулинарные рецепты в общей базе, публиковать свои рецепты, добавлять других пользователей в подписки, сохранять понравившиеся рецепты в "Избранное" или в "Список покупок". "Список покупок" при необходимости можно скачать в формате PDF, файл которого будет содержать все необходимые для приготовления выбранных блюд ингредиенты и их количество. В приложении используется система тегов для быстрого поиска рецептов.

В приложении реализована система авторизации и аутентификации по Token.

## Порядок установки проекта

Клонируем репозиторий и переходим в директорию infra:
```
git clone https://github.com/Hrushon/foodgram-project-react.git
```
```
cd ./foodgram-project-react/infra/
```

### Структура env-файла:

Создаем и открываем для редактирования файл .env:
```
sudo nano .env
```
В файл вносим следующие данные:
```
# указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql
# указываем имя базы данных
DB_NAME=postgres
# указываем логин для подключения к базе данных
POSTGRES_USER=postgres
# указываем пароль для подключения к БД
POSTGRES_PASSWORD=postgres
# указываем название сервиса (контейнера)
DB_HOST=db
# указываем порт для подключения к БД
DB_PORT=5432
```

### Развертывание с использованием Docker:

Разворачиваем контейнеры в фоновом режиме:
```
sudo docker-compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker-compose exec web python manage.py migrate
```
При первом запуске собираем статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Загружаем демонстрационные данные в базу данных:
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```


## В проекте есть такие эндпоинты

### Регистрация нового пользователя
```
/api/v1/     метод: POST
```
### Получение JWT-токена
```
/api/v1/auth/token/    метод: POST
```
### Получение, создание рецептов, их обновление и удаление
```
/api/recipes/   методы: GET, POST
```
```
/api/recipes/{id}/   метод: PATCH, DEL
```
### Добавление понравившегося рецепта в "Избранное" и удаление его из списка
```
/api/recipes/{id}/favorite/    методы: POST, DELETE
```
### Добавление рецепта в "Список покупок" и удаление его из списка
```
/api/recipes/{id}/shopping_cart/    методы: POST, DELETE
```
### Скачивание файла в формате PDF с ингредиентами рецептов из списка покупок.
```
/api/recipes/download_shopping_cart/     метод: GET
```
### Просмотр доступных тегов
```
/api/tags/     метод: GET
```
```
/api/tags/{id}     метод: GET
```
### Просмотр доступных ингредиентов
```
/api/ingredients/     метод: GET
```
```
/api/ingredients/{id}/    метод: GET
```
### Получение, создание, редактирование и удаление комментариев к отзывам
```
/api/v1/titles/{titles_id}/reviews/     методы: GET, POST
```
```
/api/v1/titles/{titles_id}/reviews/{reviews_id}/    методы: GET, PATCH, DEL
```
### Получение, создание, редактирование и удаление пользователей
```
/api/v1/users/     методы: GET, POST
```
```
/api/v1/users/{username}/     методы: GET, PATCH, DEL
```
### Получение и редактирование своей учетной записи
```
/api/v1/users/me/     методы: GET, PATCH
```
### Стек:
+ frontend: React
+ backend: DJANGO + Django Rest Framework
+ db: PostgreSQL
+ container: Docker
+ servers: nginx, Gunicorn

