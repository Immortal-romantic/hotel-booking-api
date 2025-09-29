# hotel-booking-service

Сервис для управления номерами отелей и бронированиями.  
Позволяет создавать, просматривать и удалять номера отелей, а также оформлять и управлять бронированиями.

# Стек технологий

Django, DRF, PostgreSQL, poetry, docker, docker compose, pytest


# Установка и запуск

1. Клонировать репозиторий

git clone https://github.com/USERNAME/hotel-booking-service.git
cd hotel-booking-service

2. Установить зависимости
poetry install

3. Запустить контейнер с базой данных
docker-compose up -d db

4. Применить миграции
poetry run python manage.py migrate

5. Запустить сервер
poetry run python manage.py runserver

# API

Номера отелей

Создать номер

POST /api/rooms/
Content-Type: application/x-www-form-urlencoded

description=Люкс&price=5000


Пример ответа:

{"room_id": 123}


Получить список номеров

GET /api/rooms/


Сортировка (пример):

GET /api/rooms/?sort_by=price&order=asc


Удалить номер

DELETE /api/rooms/{id}/


Создать бронирование

POST /api/bookings/
Content-Type: application/x-www-form-urlencoded

room_id=123&date_start=2025-01-10&date_end=2025-01-15


Пример ответа:

{"booking_id": 456}


Получить список бронирований

GET /api/bookings/


Пример ответа:

[
  {"booking_id": 456, "date_start": "2025-01-10", "date_end": "2025-01-15"}
]

Удалить бронирование

DELETE /api/bookings/{id}/

# Тесты

Запуск тестов:

poetry run pytest

Особенности реализации

Используется Django REST Framework для быстрого построения API.

Поддержка сортировки списка номеров по цене и дате создания.

Контейнеризация базы данных (PostgreSQL) с помощью docker-compose.

Управление зависимостями через poetry.

Автотесты на pytest для проверки корректности работы сервиса.

# Возможные улучшения

Добавить авторизацию пользователей.

Добавить фильтрацию бронирований по датам.

Поддержка Swagger/OpenAPI для авто-документации.


