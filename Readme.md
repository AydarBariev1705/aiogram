# Описание проекта
Проект представляет собой телеграмм бота на фреймворке aiogram-3.
Графический интерфейс админ-панели Django и бот оформлены как два отдельных проекта,
взаимодействующих посредством базы данных, что не требует обязательной реализации API.


## Используемые инструменты
* **Python**
* **aiogram-3**
* **Docker** and **Docker Compose**
* **PostgreSQL**
* **SQLAlchemy**
* **Pandas**


## Сборка и запуск приложения
1. Переименовать .env.template в .env
2. Заполнить необходимые данные в .env файл
3. Собрать контейнер:
    ```
    docker-compose build
    ```
4. Запустить контейнер:
    ```
    docker-compose up -d
    ```
## Первый запуск приложения
1. Переименовать .env.template в .env
2. Заполнить необходимые данные в .env файл (DB_HOST указать localhost)
3. Запустить на фоне БД:
    ```
    docker-compose up postgres -d
    ```
4. Провести миграции:
   ```
   python manage.py migrate
   ```
5. Загрузить демонстрационные данные в бд:
    ```
    python manage.py loaddata users.json
    ```
    ```
    python manage.py loaddata aiogram.json
    ```
6. Остановить контейнер с БД:
    ```
    docker stop db
    ```
7. Указать в .env файле DB_HOST=DB


