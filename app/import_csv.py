import csv
from app.db import SessionLocal, engine
from app.models import Student, Base

# На случай, если вы хотите создать таблицы напрямую (не через alembic):
# Base.metadata.create_all(bind=engine)

def import_csv(path: str):
    """
    Импортирует CSV (с заголовком: Фамилия,Имя,Факультет,Курс,Оценка)
    в таблицу students.
    """
    session = SessionLocal()
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Если в CSV заголовки на русском, можно привести их к английским:
            # ожидаем заголовки: "Фамилия","Имя","Факультет","Курс","Оценка"
            for row in reader:
                student = Student(
                    last_name=row.get("Фамилия") or row.get("last_name"),
                    first_name=row.get("Имя") or row.get("first_name"),
                    faculty=row.get("Факультет") or row.get("faculty"),
                    course=row.get("Курс") or row.get("course"),
                    grade=int(row.get("Оценка") or row.get("grade") or 0),
                )
                session.add(student)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    import_csv("students.csv")