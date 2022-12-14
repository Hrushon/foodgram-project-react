![Workflow](https://github.com/Hrushon/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.7.0-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-2.2.19-red?style=for-the-badge&logo=django&logoColor=blue)
![Postgres](https://img.shields.io/badge/Postgres-13.0-blueviolet?style=for-the-badge&logo=postgresql&logoColor=yellow)
![Nginx](https://img.shields.io/badge/NGINX-1.19.3-orange?style=for-the-badge&logo=nginx&logoColor=green)
![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-inactive?style=for-the-badge&logo=gunicorn&logoColor=white)

# FOODGRAM
## Продуктовый помощник

Проект предоставляет возможность пользователям просматривать кулинарные рецепты в общей базе, публиковать свои рецепты, добавлять других пользователей в подписки, сохранять понравившиеся рецепты в "Избранное" или в "Список покупок". "Список покупок" при необходимости можно скачать в формате PDF, файл которого будет содержать все необходимые для приготовления выбранных блюд ингредиенты и их количество. Используется система тегов для быстрого поиска рецептов.

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
# секретный ключ для Django
SECRET_KEY=jhvsklhglsgvnnuefc
# указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql
# указываем имя базы данных
DB_NAME=postgres
# логин для подключения к базе данных
POSTGRES_USER=postgres
# пароль для подключения к БД
POSTGRES_PASSWORD=postgres
# название сервиса (контейнера) для БД
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
Загружаем данные ингредиентов в базу данных:
```
sudo docker-compose exec web python manage.py loaddata dump.json
```

## Эндпоинты приложения

### Список пользователей, регистрация нового пользователя
```
/api/users/     метод: GET, POST
```
### Профиль пользователя и собственный профиль пользователя
```
/api/users/{id}/     метод: GET
```
```
/api/users/me/     метод: GET
```
### Изменение пароля пользователя
```
/api/users/set_password/     метод: POST
```
### Получение и удаление токена авторизации
```
/api/auth/token/login/    метод: POST
```
```
/api/auth/token/logout/    метод: POST
```
### Получение, создание рецептов, их обновление и удаление
```
/api/recipes/   методы: GET, POST
```
```
/api/recipes/{id}/   метод: GET, PATCH, DEL
```
### Добавление понравившегося рецепта в "Избранное" и удаление его
```
/api/recipes/{id}/favorite/    методы: POST, DELETE
```
### Добавление рецепта в "Список покупок" и удаление его из списка
```
/api/recipes/{id}/shopping_cart/    методы: POST, DELETE
```
### Скачивание файла в формате PDF с ингредиентами рецептов из списка покупок
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
