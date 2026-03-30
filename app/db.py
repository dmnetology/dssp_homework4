from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Для задания используем локальный файл DB:
DATABASE_URL = "sqlite:///./students.db"

# Создаём engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # для sqlite + многопоточности, безопасно здесь
)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)