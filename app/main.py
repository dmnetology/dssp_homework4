from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import csv
import io

from .db import SessionLocal
from . import crud, schemas

app = FastAPI(title="Students API")

# dependency
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# CRUD endpoints
@app.post("/students/", response_model=schemas.StudentRead)
def api_create_student(student_in: schemas.StudentCreate, session: Session = Depends(get_session)):
    student = crud.create_student(session,
                                  last_name=student_in.last_name,
                                  first_name=student_in.first_name,
                                  faculty=student_in.faculty,
                                  course=student_in.course,
                                  grade=student_in.grade)
    return student

@app.get("/students/{student_id}", response_model=schemas.StudentRead)
def api_get_student(student_id: int, session: Session = Depends(get_session)):
    student = crud.get_student(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/", response_model=List[schemas.StudentRead])
def api_list_students(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return crud.list_students(session, skip=skip, limit=limit)

@app.put("/students/{student_id}", response_model=schemas.StudentRead)
def api_update_student(student_id: int, student_in: schemas.StudentUpdate, session: Session = Depends(get_session)):
    updated = crud.update_student(session, student_id, **student_in.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}")
def api_delete_student(student_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_student(session, student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"ok": True}

# Additional endpoints per assignment
@app.get("/by-faculty/{faculty}", response_model=List[schemas.StudentRead])
def api_students_by_faculty(faculty: str, session: Session = Depends(get_session)):
    return crud.students_by_faculty(session, faculty)

@app.get("/unique-courses", response_model=List[str])
def api_unique_courses(session: Session = Depends(get_session)):
    return crud.unique_courses(session)

@app.get("/by-course/{course}/below/{threshold}", response_model=List[schemas.StudentRead])
def api_students_by_course_below(course: str, threshold: int = 30, session: Session = Depends(get_session)):
    return crud.students_by_course_below_grade(session, course, grade_threshold=threshold)

@app.get("/average-grade/{faculty}")
def api_average_grade(faculty: str, session: Session = Depends(get_session)):
    avg = crud.average_grade_by_faculty(session, faculty)
    if avg is None:
        raise HTTPException(status_code=404, detail="No students for faculty")
    return {"faculty": faculty, "average_grade": avg}

# Export CSV endpoint - returns CSV with same headers as input
@app.get("/export/csv")
def api_export_csv(session: Session = Depends(get_session)):
    students = crud.list_students(session, skip=0, limit=10_000_000)  # large limit
    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    # write header in same order as original CSV: Фамилия,Имя,Факультет,Курс,Оценка
    writer.writerow(["Фамилия", "Имя", "Факультет", "Курс", "Оценка"])
    for s in students:
        writer.writerow([s.last_name, s.first_name, s.faculty, s.course, s.grade])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=students_export.csv"})