# Foodgram - продуктовый помощник
![example workflow](https://github.com/Seniacat/Foodgram/actions/workflows/foodgram_workflow.yml/badge.svg)  

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Описание проекта
Онлайн-сервис Foodgram («Продуктовый помощник») создан для начинающих кулинаров и опытных гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать в формате .txt сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект разворачивается в Docker контейнерах: backend-приложение API, PostgreSQL-база данных, nginx-сервер и frontend-контейнер.

Реализовано CI и CD проекта. При пуше изменений в главную ветку проект автоматические тестируется на соотвествие требованиям PEP8. После успешного прохождения тестов, на git-платформе собирается образ backend-контейнера Docker и автоматически размещается в облачном хранилище DockerHub. Размещенный образ автоматически разворачивается на боевом сервере вмете с контейнером веб-сервера nginx и базой данных PostgreSQL.

[Ссылка на проект на сервере Yandex.Cloud](http://seniacat.sytes.net/)

## Системные требования
- Python 3.7+
- Docker
- Works on Linux, Windows, macOS

## Запуск проекта в dev-режиме
Клонируйте репозиторий и перейдите в него в командной строке.
Создайте и активируйте виртуальное окружение:
```
git clone https://github.com/Seniacat/Foodgram.git
cd Foodgram
```
Должен быть свободен порт 8000. PostgreSQL поднимается на 5432 порту, он тоже должен быть свободен.
Cоздать и открыть файл .env с переменными окружения:
```
cd infra
touch .env
```
Заполнить .env файл с переменными окружения по примеру (SECRET_KEY см. в файле settings.py). 
Необходимые для работы проекта переменные окружения можно найти в файле .env.example в текущей директории:
```
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres  >> .env

echo DB_HOST=db  >> .env

echo DB_PORT=5432  >> .env

echo SECRET_KEY=************ >> .env
```
Установить и запустить приложения в контейнерах (образ для контейнера web загружается из DockerHub):
```
docker-compose up -d
```
Запустить миграции, создать суперюзера, собрать статику и заполнить а БД таблицы с ингредиентами и тегами:
```
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py createsuperuser

docker-compose exec backend python manage.py collectstatic --no-input 

docker-compose exec backend python manage.py import_ings ingredients.csv

docker-compose exec backend python manage.py import_tags tags.csv
```

