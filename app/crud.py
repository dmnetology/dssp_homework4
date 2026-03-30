from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .models import Student

# CRUD
def create_student(session: Session, *, last_name: str, first_name: str,
                   faculty: str, course: str, grade: int) -> Student:
    """
    Создать студента и сохранить в БД.

    Если запись уже существует (по уникальному ограничению) — бросаем IntegrityError,
    который в коде вызывающем можно перевести в HTTP 409 Conflict.
    """
    student = Student(
        last_name=last_name,
        first_name=first_name,
        faculty=faculty,
        course=course,
        grade=grade,
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_student(session: Session, student_id: int) -> Optional[Student]:
    return session.get(Student, student_id)

def list_students(session: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    stmt = select(Student).offset(skip).limit(limit)
    return session.execute(stmt).scalars().all()

def update_student(session: Session, student_id: int, **fields) -> Optional[Student]:
    student = session.get(Student, student_id)
    if not student:
        return None
    for key, value in fields.items():
        if value is not None and hasattr(student, key):
            setattr(student, key, value)
    session.commit()
    session.refresh(student)
    return student

def delete_student(session: Session, student_id: int) -> bool:
    student = session.get(Student, student_id)
    if not student:
        return False
    session.delete(student)
    session.commit()
    return True

# Дополнительные запросы
def students_by_faculty(session: Session, faculty: str) -> List[Student]:
    stmt = select(Student).where(Student.faculty == faculty)
    return session.execute(stmt).scalars().all()

def unique_courses(session: Session) -> List[str]:
    stmt = select(func.distinct(Student.course))
    rows = session.execute(stmt).scalars().all()
    return rows

def students_by_course_below_grade(session: Session, course: str, grade_threshold: int = 30) -> List[Student]:
    stmt = select(Student).where(Student.course == course, Student.grade < grade_threshold)
    return session.execute(stmt).scalars().all()

def average_grade_by_faculty(session: Session, faculty: str) -> Optional[float]:
    stmt = select(func.avg(Student.grade)).where(Student.faculty == faculty)
    avg = session.execute(stmt).scalar_one_or_none()
    # scalar_one_or_none может вернуть None if no rows
    return float(avg) if avg is not None else None