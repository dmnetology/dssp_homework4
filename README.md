# Homework 4 — REST API. Реализация CRUD

Дисциплина: Разработка прототипов программных решений  
Тема: REST API. Реализация CRUD.

Кратко
------
Это продолжение предыдущего задания. Реализованы:
- SQLAlchemy модель Student и миграции Alembic.
- Скрипт импорта данных из students.csv.
- CRUD-операции (Create/Read/Update/Delete).
- REST API на FastAPI с эндпоинтами для фильтрации и экспорта CSV.

Структура репозитория
- app/
  - __init__.py
  - models.py       # модели
  - db.py           # engine, SessionLocal, DATABASE_URL
  - import_csv.py   # скрипт импорта students.csv (заполняет таблицу)
  - crud.py         # функции CRUD + дополнительные запросы
  - schemas.py      # Pydantic-схемы и валидация
  - main.py         # FastAPI приложение
- alembic/          # миграции
- students.csv      # исходные данные
- requirements.txt
- README.md

Требования
- Python 3.8+
- Зависимости в requirements.txt

Установка
1. Создайте виртуальное окружение и активируйте его:
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate

2. Установите зависимости:
   pip install -r requirements.txt
   # если требуется:
   pip install fastapi uvicorn sqlalchemy alembic pydantic

Конфигурация БД
- По умолчанию используется SQLite файл: sqlite:///./students.db
- Этот URL хранится в app/db.py (переменная DATABASE_URL; можно заменить на PostgreSQL/MySQL).

Миграции (Alembic)
1. Если alembic ещё не инициализировано, выполните:
   alembic init alembic
   (в репозитории alembic уже настроен)

2. Проверьте/установите sqlalchemy.url в alembic.ini или убедитесь, что alembic/env.py читает DATABASE_URL из app/db.py,
а также target_metadata = Base.metadata.

3. Создать автогенерируемую ревизию (если нужно):
   alembic revision --autogenerate -m "create students table"

4. Применить миграции:
   alembic upgrade head

Импорт данных из CSV
- Убедитесь, что students.csv лежит в корне проекта (в кодировке UTF-8).
- Запустите импорт как модуль (из корня проекта):
   python -m app.import_csv

Проверка данных
- Быстрая проверка в интерактивном режиме:
   python -c "from app.db import SessionLocal; from app.models import Student; s=SessionLocal(); print(s.query(Student).count()); s.close()"

Запуск FastAPI
--------------
1. Установите FastAPI + Uvicorn:
   pip install fastapi uvicorn

2. Запустите приложение:
   uvicorn app.main:app --reload

3. Откройте документацию Swagger:
   http://127.0.0.1:8000/docs

Основные эндпоинты
------------------
- POST /students/ — создать студента (валидируется через Pydantic)
- GET /students/{id} — получить студента по id
- GET /students/?skip=0&limit=100 — список студентов
- PUT /students/{id} — обновить студента (поля необязательны)
- DELETE /students/{id} — удалить студента
- GET /by-faculty/{faculty} — студенты по факультету
- GET /unique-courses — список уникальных курсов
- GET /by-course/{course}/below/{threshold} — студенты на course с оценкой ниже threshold
- GET /average-grade/{faculty} — средний балл по факультету
- GET /export/csv — экспорт всех записей в CSV (в формате исходного students.csv)
