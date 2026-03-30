from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    """
    SQLAlchemy-модель для хранения данных из students.csv.

    Поля:
    - id: первичный ключ (целочисленный, автоинкремент)
    - last_name: фамилия студента
    - first_name: имя студента
    - faculty: факультет (строка)
    - course: курс/предмет (в таблице указан, например, "Теор. Механика")
    - grade: числовая оценка (целое число)

    Примечание: `course` в исходном CSV может означать предмет, поэтому тип -- String.
    При необходимости можно вынести предметы и факультеты в отдельные таблицы и связать FK.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(length=100), nullable=False, index=True)
    first_name = Column(String(length=100), nullable=False, index=True)
    faculty = Column(String(length=100), nullable=False, index=True)
    course = Column(String(length=200), nullable=False)
    grade = Column(Integer, nullable=False)